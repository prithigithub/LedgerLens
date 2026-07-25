from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    document_id: int
    corrections: dict


class DocumentResponse(BaseModel):
    id: int
    filename: str
    status: str
    confidence: float

    class Config:
        from_attributes = True