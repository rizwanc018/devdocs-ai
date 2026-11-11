import re


def normalize_text(text: str) -> str:

    # Replace non-breaking spaces with regular spaces
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove null characters
    text = text.replace("\x00", "")

    # Remove trailing whitespace from each line
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    # Collapse excessive consecutive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
