from openai import OpenAI

from backend.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def _to_dict(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "__dict__"):
        return value.__dict__
    return value


def moderate_image(image_url: str) -> dict:
    """Moderate an image data URI before any other LLM processing."""
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=[
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            }
        ],
    )

    result = response.results[0]
    categories = _to_dict(result.categories) or {}
    category_scores = _to_dict(result.category_scores) or {}

    max_score = max(category_scores.values(), default=0.0)

    if result.flagged or max_score >= settings.MODERATION_BLOCK_THRESHOLD:
        verdict = "BLOCK"
    elif max_score >= settings.MODERATION_REVIEW_THRESHOLD:
        verdict = "HUMAN_REVIEW"
    else:
        verdict = "ALLOW"

    return {
        "verdict": verdict,
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": category_scores,
        "max_score": max_score,
    }


def is_safe(image_url: str) -> dict:
    result = moderate_image(image_url)
    return {
        "allowed": result["verdict"] == "ALLOW",
        "verdict": result["verdict"],
        "reason": result["categories"] if result["verdict"] != "ALLOW" else None,
        "category_scores": result["category_scores"],
    }
