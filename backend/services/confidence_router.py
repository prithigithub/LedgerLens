from backend.config import settings


def evaluate_confidence(invoice: dict):
    review_fields = []

    for field, value in invoice.items():
        if field == "overall_confidence":
            continue

        if isinstance(value, dict):
            confidence = value.get("confidence")
            if confidence is not None and confidence < settings.CONFIDENCE_THRESHOLD:
                review_fields.append(
                    {
                        "field": field,
                        "confidence": confidence,
                        "value": value.get("value"),
                    }
                )

    return {
        "status": "review_required" if review_fields else "approved",
        "fields": review_fields,
    }
