from typing import List

from pydantic import BaseModel, Field


class FieldValue(BaseModel):
    value: str = ""
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class LineItem(BaseModel):
    description: str = ""
    quantity: int = 0
    unit_price: str = ""
    amount: str = ""
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class LineItemsField(BaseModel):
    value: List[LineItem] = Field(
        default_factory=list
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class InvoiceSchema(BaseModel):
    vendor: FieldValue
    invoice_number: FieldValue
    date: FieldValue
    currency: FieldValue
    subtotal: FieldValue
    tax: FieldValue
    total: FieldValue
    line_items: LineItemsField
    overall_confidence: float = Field(
        ge=0.0,
        le=1.0,
    )