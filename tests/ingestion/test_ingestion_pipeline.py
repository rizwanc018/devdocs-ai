from pathlib import Path

from devdocs_ai.config.path import RAW_DATA_DIR
from devdocs_ai.ingestion.pipeline import process_pdf

pdf_path = Path(RAW_DATA_DIR / "First Steps - FastAPI.pdf")

chunks = process_pdf(pdf_path)

print(f"Total processed chunks: {len(chunks)}")

for chunk in chunks[:3]:
    print("=" * 70)
    print("Chunk ID:", chunk["chunk_id"])
    print("Source:", chunk["source"])
    print("Pages:", chunk["page_start"], "-", chunk["page_end"])
    print("Tokens:", chunk["token_count"])
    print("Text:", chunk["text"])
