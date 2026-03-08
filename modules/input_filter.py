BLOCK_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "reveal hidden instructions",
    "bypass security",
]


def validate_input(user_query: str):

    lower = user_query.lower()

    for pattern in BLOCK_PATTERNS:

        if pattern in lower:
            raise ValueError("Prompt injection detected")

    return True