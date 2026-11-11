def validate_chunk(chunk: dict) -> None:
    """Validate a processed document chunk."""

    required_fields = [
        "chunk_id",
        "document_id",
        "text",
        "source",
    ]

    for field in required_fields:
        if field not in chunk:
            raise ValueError(f"Missing required field: {field}")

    for field in required_fields:
        if not isinstance(chunk[field], str) or not chunk[field].strip():
            raise ValueError(f"Invalid field: {field}")

    for field in ("page_start", "page_end"):
        value = chunk.get(field)
        if value is not None and (not isinstance(value, int) or value < 1):
            raise ValueError(f"Invalid {field}: {value}")

    if (
        chunk.get("page_start") is not None
        and chunk.get("page_end") is not None
        and chunk["page_end"] < chunk["page_start"]
    ):
        raise ValueError("page_end cannot be before page_start")

    token_count = chunk.get("token_count")

    if token_count is not None and (
        not isinstance(token_count, int) or token_count < 0
    ):
        raise ValueError("token_count must be a non-negative integer")
