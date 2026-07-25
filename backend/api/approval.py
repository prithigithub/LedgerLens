from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import json

from backend.database.database import get_db
from backend.models.document import Document
from backend.models.review import ReviewQueue
from backend.services.metrics import ACTIVE_REVIEWS

router = APIRouter(prefix="/approve", tags=["Approval"])


@router.post("/")
def approve_invoice(request: dict, db: Session = Depends(get_db)):
    document_id = request.get("document_id")
    reviewed_data = request.get("reviewed_data")

    if not document_id:
        raise HTTPException(status_code=400, detail="document_id is required")

    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.status = "approved"
    if reviewed_data is not None:
        document.reviewed_json = json.dumps(reviewed_data)

    review = (
        db.query(ReviewQueue)
        .filter(
            ReviewQueue.document_id == document.id,
            ReviewQueue.status == "pending",
        )
        .first()
    )
    if review:
        review.status = "approved"
        ACTIVE_REVIEWS.dec()

    db.commit()
    db.refresh(document)

    return {
        "message": "Invoice approved",
        "document_id": document.id,
        "status": document.status,
    }
