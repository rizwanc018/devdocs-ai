import re
from pathlib import Path


def build_chunk_metadata(
    file_path: str | Path,
    chunk_index: int,
    metadata: dict,
) -> dict:

    file_path = Path(file_path)

    if chunk_index < 0:
        raise ValueError("chunk_index cannot be negative")

    # Create a normalized document identifier
    document_id = re.sub(
        r"[^a-z0-9]+",
        "-",
        file_path.stem.lower(),
    ).strip("-")

    if not document_id:
        raise ValueError("Could not generate document ID")

    return {
        "chunk_id": f"{document_id}-{chunk_index:04d}",
        "document_id": document_id,
        "source": file_path.name,
        "page_start": metadata.get("page_start"),
        "page_end": metadata.get("page_end"),
        "section_id": metadata.get("section_id"),
        "section_path": metadata.get("section_path") or [],
        "token_count": metadata.get("token_count"),
        "types": metadata.get("types") or [],
    }
