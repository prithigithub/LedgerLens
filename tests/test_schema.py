from backend.schemas.invoice import InvoiceSchema


def test_invoice_schema():
    invoice = InvoiceSchema(
        vendor={
            "value": "ABC Company",
            "confidence": 0.98,
        },
        invoice_number={
            "value": "INV-100",
            "confidence": 0.95,
        },
        date={
            "value": "2026-01-01",
            "confidence": 0.90,
        },
        currency={
            "value": "USD",
            "confidence": 0.99,
        },
        subtotal={
            "value": "1000",
            "confidence": 0.90,
        },
        tax={
            "value": "100",
            "confidence": 0.85,
        },
        total={
            "value": "1100",
            "confidence": 0.95,
        },
        payment_method={
            "value": "Bank Transfer",
            "confidence": 0.88,
        },
        line_items={
            "value": [],
            "confidence": 0.90,
        },
        overall_confidence=0.93,
    )

    assert invoice.vendor.value == "ABC Company"
    assert invoice.overall_confidence > 0.9