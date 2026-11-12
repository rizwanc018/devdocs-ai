from pathlib import Path

from devdocs_ai.config.path import RAW_DATA_DIR
from devdocs_ai.ingestion.pdf_loader import load_pdf

for pdf_file in Path(RAW_DATA_DIR).glob("*.pdf"):
    chunks = load_pdf(pdf_file)

    print(f"\n{'=' * 70}")
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:5]:
        print("=" * 60)
        print(chunk)
