from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from openai import (
    OpenAI,
    RateLimitError,
    APIError,
)

from sqlalchemy.orm import Session

import json
import logging
import os
import shutil
import time
import uuid

from backend.database.database import get_db
from backend.models.document import Document
from backend.models.review import ReviewQueue
from backend.schemas.invoice import InvoiceSchema
from backend.services.confidence_router import evaluate_confidence
from backend.services.image_processor import preprocess_image
from backend.services.invoice_detector import is_invoice
from backend.services.metrics import (
    ACTIVE_REVIEWS,
    CONFIDENCE_SCORE,
    DOCUMENTS_PROCESSED,
    EXTRACTION_TIME,
    MODERATION_TIME,
    MODERATION_VERDICTS,
    PROCESSING_TIME,
    REVIEW_REQUIRED,
)
from backend.services.moderation import moderate_image
from backend.services.pii import redact_pii
from backend.services.watermark import add_watermark


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/ingest",
    tags=["Invoice Processing"],
)


UPLOAD_DIR = "uploads"


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_invoice(image_data: str):

    try:

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": """
Extract all visible invoice information from this image.

Return ONLY valid JSON.

Use exactly this structure:

{
  "vendor": {
    "value": "",
    "confidence": 0.0
  },
  "invoice_number": {
    "value": "",
    "confidence": 0.0
  },
  "date": {
    "value": "",
    "confidence": 0.0
  },
  "currency": {
    "value": "",
    "confidence": 0.0
  },
  "subtotal": {
    "value": "",
    "confidence": 0.0
  },
  "tax": {
    "value": "",
    "confidence": 0.0
  },
  "total": {
    "value": "",
    "confidence": 0.0
  },
  "line_items": {
    "value": [],
    "confidence": 0.0
  },
  "overall_confidence": 0.0
}

Each line item must contain:

{
  "description": "",
  "quantity": 0,
  "unit_price": "",
  "amount": "",
  "confidence": 0.0
}

Rules:
- Do not invent missing information.
- If a field is missing, use an empty string.
- Use 0.0 confidence for missing fields.
- Confidence must be between 0.0 and 1.0.
- Return JSON only.
- Do not return Markdown.
- Do not return explanations.
""",
                        },
                        {
                            "type": "input_image",
                            "image_url": (
                                "data:image/jpeg;base64,"
                                f"{image_data}"
                            ),
                        },
                    ],
                }
            ],
        )

        extracted_text = response.output_text

        logger.info(
            "RAW OPENAI RESPONSE: %r",
            extracted_text,
        )

        if not extracted_text:

            raise ValueError(
                "OpenAI returned an empty response."
            )

        extracted_text = (
            extracted_text
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

        extracted_data = json.loads(
            extracted_text
        )

        invoice = InvoiceSchema.model_validate(
            extracted_data
        )

        return invoice, 0.0

    except Exception as exc:

        logger.exception(
            "Invoice extraction failed: %s",
            str(exc),
        )

        raise


@router.post("/")
async def ingest_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    start_time = time.time()

    temp_path = None
    final_path = None

    if (
        not file.content_type
        or not file.content_type.startswith("image/")
    ):

        raise HTTPException(
            status_code=400,
            detail="Only image uploads are supported.",
        )

    try:

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True,
        )

        safe_filename = os.path.basename(
            file.filename or "upload.jpg"
        )

        temp_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4()}_temp_{safe_filename}",
        )

        with open(
            temp_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        image_data = preprocess_image(
            temp_path
        )

        image_data_uri = (
            "data:image/jpeg;base64,"
            f"{image_data}"
        )

        moderation_start = time.time()

        moderation = moderate_image(
            image_data_uri
        )

        MODERATION_TIME.observe(
            time.time()
            - moderation_start
        )

        MODERATION_VERDICTS.labels(
            verdict=moderation["verdict"]
        ).inc()

        if moderation["verdict"] == "BLOCK":

            raise HTTPException(
                status_code=422,
                detail={
                    "message": (
                        "Image blocked by moderation."
                    ),
                    "verdict": (
                        moderation["verdict"]
                    ),
                    "categories": (
                        moderation["categories"]
                    ),
                },
            )

        invoice_check = is_invoice(
            image_data
        )

        if not invoice_check["is_invoice"]:

            raise HTTPException(
                status_code=400,
                detail=invoice_check.get(
                    "reason",
                    "Uploaded document is not an invoice.",
                ),
            )

        extraction_start = time.time()

        invoice, extraction_cost = (
            extract_invoice(
                image_data
            )
        )

        EXTRACTION_TIME.observe(
            time.time()
            - extraction_start
        )

        CONFIDENCE_SCORE.observe(
            invoice.overall_confidence
        )

        decision = evaluate_confidence(
            invoice.model_dump()
        )

        status = decision["status"]

        final_filename = (
            f"{uuid.uuid4()}_{safe_filename}"
        )

        final_path = os.path.join(
            UPLOAD_DIR,
            final_filename,
        )

        shutil.copy(
            temp_path,
            final_path,
        )

        add_watermark(
            final_path
        )

        document = Document(
            filename=safe_filename,
            status=status,
            overall_confidence=(
                invoice.overall_confidence
            ),
            extracted_json=json.dumps(
                invoice.model_dump()
            ),
            watermarked_path=final_path,
        )

        db.add(
            document
        )

        db.flush()

        if status == "review_required":

            review = ReviewQueue(
                document_id=document.id,
                reason=(
                    "One or more extracted fields "
                    "are below the confidence threshold."
                ),
                fields=json.dumps(
                    decision["fields"]
                ),
                status="pending",
            )

            db.add(
                review
            )

            REVIEW_REQUIRED.inc()

            ACTIVE_REVIEWS.inc()

        db.commit()

        db.refresh(
            document
        )

        DOCUMENTS_PROCESSED.inc()

        PROCESSING_TIME.observe(
            time.time()
            - start_time
        )

        logger.info(
            "Document %s processed successfully "
            "with status=%s",
            document.id,
            status,
        )

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            os.remove(
                temp_path
            )

        return {
            "document_id": document.id,
            "status": status,
            "invoice": invoice.model_dump(),
            "review_fields": (
                decision["fields"]
            ),
            "moderation_verdict": (
                moderation["verdict"]
            ),
            "estimated_extraction_cost_usd": (
                extraction_cost
            ),
            "watermarked_file": final_path,
        }

    except RateLimitError:

        db.rollback()

        raise HTTPException(
            status_code=429,
            detail=(
                "OpenAI API quota exceeded."
            ),
        )

    except APIError as exc:

        db.rollback()

        logger.exception(
            "OpenAI API error: %s",
            str(exc),
        )

        for path in (
            temp_path,
            final_path,
        ):

            if (
                path
                and os.path.exists(path)
            ):

                os.remove(
                    path
                )

        raise HTTPException(
            status_code=502,
            detail=(
                "OpenAI API error while "
                "processing the invoice image."
            ),
        )

    except HTTPException:

        db.rollback()

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            os.remove(
                temp_path
            )

        raise

    except Exception as exc:

        db.rollback()

        logger.exception(
            "Invoice ingestion failed: %s",
            redact_pii(
                str(exc)
            ),
        )

        for path in (
            temp_path,
            final_path,
        ):

            if (
                path
                and os.path.exists(path)
            ):

                os.remove(
                    path
                )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Ingestion failed: {str(exc)}"
            ),
        )