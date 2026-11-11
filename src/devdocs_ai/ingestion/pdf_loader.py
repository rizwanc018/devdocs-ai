from pathlib import Path

from pymupdf import pymupdf


def load_pdf(
    file_path: str | Path,
    max_tokens: int = 400,
) -> list[dict]:
    file_path = Path(file_path)
    documents = []

    with pymupdf.open(file_path) as pdf:
        chunked_document = pdf.to_chunks(max_tokens=max_tokens)

        for chunk in chunked_document:
            metadata = chunk.metadata

            documents.append(
                {
                    "text": chunk.text,
                    "page_start": metadata.page_start,
                    "page_end": metadata.page_end,
                    "section_id": metadata.section_id,
                    "section_path": metadata.section_path,
                    "token_count": metadata.token_count,
                    "types": metadata.types,
                }
            )

    return documents
