from pathlib import Path

from devdocs_ai.ingestion.pdf_loader import load_pdf

pdf_files = Path("data/raw").glob("*.pdf")

for pdf_file in pdf_files:
    print(f"pdf_file: {pdf_file}")

    pages = load_pdf(pdf_file)

    print(f"Document: {pdf_file.name}")
    print(f"Total extracted pages: {len(pages)}")

    if pages:
        print(f"First page: {pages[0]['page']}")
        print(f"Extracted text:\n{pages[0]['text'][:300]}")
