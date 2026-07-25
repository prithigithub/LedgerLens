from backend.config import settings


def calculate_chat_cost(usage) -> float:
    """Estimate GPT-4o cost from prompt and completion token usage."""
    if usage is None:
        return 0.0

    prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
    completion_tokens = getattr(usage, "completion_tokens", 0) or 0

    return (
        (prompt_tokens / 1000) * settings.GPT4O_INPUT_COST_PER_1K
        + (completion_tokens / 1000) * settings.GPT4O_OUTPUT_COST_PER_1K
    )


def calculate_cost(model: str) -> float:
    """Backward-compatible fixed estimate for non-tokenized calls."""
    return {
        "moderation": 0.001,
    }.get(model, 0.0)
