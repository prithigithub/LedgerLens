from openai import OpenAI

from backend.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def is_invoice(image_data: str) -> dict:
    image_data_uri = f"data:image/jpeg;base64,{image_data}"

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Analyze this image carefully. "
                            "Determine whether it contains an invoice or receipt. "
                            "An invoice or receipt may contain a business name, "
                            "invoice number, date, customer information, "
                            "line items, prices, taxes, subtotal, or total. "
                            "Respond with exactly one word: YES or NO."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_uri,
                    },
                ],
            }
        ],
    )

    result = response.output_text.strip().upper()

    print(f"Invoice detection result: {result}")

    if "YES" in result:
        return {
            "is_invoice": True,
            "reason": "Invoice or receipt detected.",
        }

    return {
        "is_invoice": False,
        "reason": "Uploaded image is not an invoice or receipt.",
    }