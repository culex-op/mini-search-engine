import re

def tokenize(text: str) -> list[str]:
    """
    Convert raw text into normalized tokens.
    """

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    return tokens
