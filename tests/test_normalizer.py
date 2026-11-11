from devdocs_ai.config.path import RAW_DATA_DIR
from devdocs_ai.ingestion.normalizer import normalize_text
from devdocs_ai.ingestion.pdf_loader import load_pdf

# pdf_file = Path("data/raw/First Steps - FastAPI.pdf")
pdf_file = RAW_DATA_DIR / "First Steps - FastAPI.pdf"

pages = load_pdf(pdf_file)

for page in pages[:2]:
    normalized_text = normalize_text(page["text"])

    print(f"\nPage: {page['page']}")
    print(f"Original length: {len(page['text'])}")
    print(f"Normalized length: {len(normalized_text)}")

    print("\nNormalized text:")
    print(normalized_text[:500])
