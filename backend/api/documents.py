from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import json

from backend.database.database import get_db
from backend.models.document import Document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


print("🔥 LOADED DOCUMENTS API")


@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
):

    print("🔥 FETCHING DOCUMENTS")


    documents = (
        db.query(Document)
        .order_by(
            Document.created_at.desc()
        )
        .all()
    )


    result = []


    for document in documents:

        extracted_data = None


        if document.extracted_json:

            try:

                extracted_data = json.loads(
                    document.extracted_json
                )

            except Exception:

                extracted_data = None



        result.append(

            {
                "id": document.id,

                "filename": document.filename,

                "status": document.status,

                "confidence": (
                    document.overall_confidence
                ),

                "watermarked_file": (
                    document.watermarked_path
                ),

                "invoice_data": (
                    extracted_data
                ),

                "reviewed_data": (
                    json.loads(
                        document.reviewed_json
                    )
                    if document.reviewed_json
                    else None
                ),

                "created_at": (
                    document.created_at
                ),

            }

        )


    return result