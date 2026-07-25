from backend.services.confidence_router import evaluate_confidence


def test_low_confidence_requires_review():
    invoice = {
        "tax": {"value": "10.00", "confidence": 0.50},
        "overall_confidence": 0.50,
    }

    result = evaluate_confidence(invoice)

    assert result["status"] == "review_required"
    assert result["fields"][0]["field"] == "tax"


def test_high_confidence_auto_approval():
    invoice = {
        "vendor": {"value": "Acme", "confidence": 0.95},
        "overall_confidence": 0.95,
    }

    result = evaluate_confidence(invoice)

    assert result["status"] == "approved"
