from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.database.database import Base


class ReviewQueue(Base):
    __tablename__ = "review_queue"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False, index=True)
    reason = Column(String, nullable=False)
    fields = Column(Text, nullable=True)
    status = Column(String, default="pending", nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
