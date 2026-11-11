from pathlib import Path

from pymupdf import pymupdf


def load_pdf(file_path: str | Path) -> list[dict]:
    file_path = Path(file_path)
    documents = []

    with pymupdf.open(file_path) as pdf:
        page_chunks = pdf.to_markdown(page_chunks=True)

        for chunk in page_chunks:
            text = chunk["text"]
            print(text)
            if not text.strip():
                continue

            documents.append(
                {
                    "source": file_path.name,
                    "page": chunk["metadata"]["page_number"],
                    "text": text,
                }
            )

    return documents
