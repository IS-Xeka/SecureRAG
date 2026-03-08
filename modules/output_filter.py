BLOCK_OUTPUT = [
    "password",
    "secret",
    "private key"
]


def validate_output(answer: str):

    lower = answer.lower()

    for pattern in BLOCK_OUTPUT:

        if pattern in lower:
            return "Output blocked due to security policy"

    return answer