import re


def normalize_text(text: str) -> str:

    # Replace non-breaking spaces with regular spaces
    text = text.replace("\u00a0", " ")

    # Normalize Windows and old Mac line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in text.split("\n")]

    text = "\n".join(lines)

    # Replace 3 or more consecutive newlines with 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
