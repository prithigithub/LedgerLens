from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import json

from backend.database.database import get_db
from backend.models.document import Document
from backend.models.review import ReviewQueue

router = APIRouter(prefix="/review", tags=["Human Review"])


@router.get("/")
def get_review_queue(db: Session = Depends(get_db)):
    reviews = (
        db.query(ReviewQueue, Document)
        .join(Document, ReviewQueue.document_id == Document.id)
        .filter(ReviewQueue.status == "pending")
        .all()
    )

    results = []
    for review, document in reviews:
        results.append(
            {
                "id": document.id,
                "review_id": review.id,
                "filename": document.filename,
                "status": document.status,
                "confidence": document.overall_confidence,
                "invoice_data": json.loads(document.extracted_json) if document.extracted_json else None,
                "review_fields": json.loads(review.fields) if review.fields else [],
                "created_at": document.created_at,
            }
        )

    return results
