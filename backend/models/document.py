from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
)

from backend.database.database import Base


class Document(Base):

    __tablename__ = "documents"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    filename = Column(
        String,
        nullable=False
    )


    status = Column(
        String,
        default="processing",
        nullable=False
    )


    overall_confidence = Column(
        Float,
        default=0.0
    )


    extracted_json = Column(
        Text,
        nullable=True
    )


    reviewed_json = Column(
        Text,
        nullable=True
    )


    watermarked_path = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )