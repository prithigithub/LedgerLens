from openai import OpenAI, RateLimitError

import json
import logging
import re

from backend.config import settings
from backend.schemas.invoice import InvoiceSchema
from backend.services.cost_tracker import calculate_chat_cost
from backend.services.metrics import API_COST
from backend.services.pii import redact_pii

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def clean_json_response(content: str) -> str:
    content = content.strip()
    content = re.sub(r"```json", "", content, flags=re.IGNORECASE)
    content = re.sub(r"```", "", content)
    return content.strip()


def normalize_invoice_json(invoice_json: dict):
    line_items = invoice_json.get("line_items")

    if isinstance(line_items, list):
        invoice_json["line_items"] = {"value": line_items, "confidence": 0.95}
    elif isinstance(line_items, dict):
        if "value" not in line_items:
            invoice_json["line_items"] = {"value": [], "confidence": 0.0}
    else:
        invoice_json["line_items"] = {"value": [], "confidence": 0.0}

    for item in invoice_json["line_items"]["value"]:
        if "quantity" not in item and "qty" in item:
            item["quantity"] = item.pop("qty")
        if "confidence" not in item:
            item["confidence"] = 0.95

    return invoice_json


def extract_invoice(image_base64: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an invoice extraction AI.
Extract invoice information from the invoice image and return ONLY valid JSON.
Every normal field must be {"value": "data", "confidence": 0.99}.
line_items must be {"value": [{"description": "", "quantity": 1, "unit_price": "", "amount": "", "confidence": 0.99}], "confidence": 0.99}.
Required fields: vendor, invoice_number, date, currency, subtotal, tax, total, payment_method, line_items, overall_confidence.
Do not use markdown.
""",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract invoice details."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content or "{}"
        logger.info("Raw extraction response: %s", redact_pii(content))

        invoice_json = normalize_invoice_json(json.loads(clean_json_response(content)))
        invoice = InvoiceSchema(**invoice_json)

        cost = calculate_chat_cost(getattr(response, "usage", None))
        API_COST.inc(cost)

        logger.info(
            "Invoice extraction validated with confidence=%s",
            invoice.overall_confidence,
        )

        return invoice, cost

    except RateLimitError:
        logger.error("OpenAI quota exceeded during invoice extraction")
        raise
    except Exception:
        logger.exception("Invoice extraction failed")
        raise
