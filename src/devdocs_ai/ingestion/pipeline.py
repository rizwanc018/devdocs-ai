from pathlib import Path

from devdocs_ai.ingestion.metadata import build_chunk_metadata
from devdocs_ai.ingestion.normalizer import normalize_text
from devdocs_ai.ingestion.pdf_loader import load_pdf
from devdocs_ai.ingestion.validation import validate_chunk


def process_pdf(
    file_path: str | Path,
    max_tokens: int = 400,
) -> list[dict]:
    """Extract, normalize, enrich and validate PDF chunks."""

    file_path = Path(file_path)

    raw_chunks = load_pdf(
        file_path=file_path,
        max_tokens=max_tokens,
    )

    processed_chunks = []

    for index, raw_chunk in enumerate(raw_chunks):
        # Normalize extracted text
        text = normalize_text(raw_chunk["text"])

        # Skip empty chunks
        if not text:
            continue

        # Build standardized metadata
        chunk_metadata = build_chunk_metadata(
            file_path=file_path,
            chunk_index=index,
            metadata=raw_chunk,
        )

        # Combine text and metadata
        chunk = {
            "text": text,
            **chunk_metadata,
        }

        # Validate the final chunk
        validate_chunk(chunk)

        processed_chunks.append(chunk)

    return processed_chunks
