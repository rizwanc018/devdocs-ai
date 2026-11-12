from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.storage import load_chunks, save_chunks

sample_chunks = [
    {
        "chunk_id": "fastapi-0001",
        "document_id": "fastapi",
        "text": "FastAPI is a Python framework.",
        "source": "First Steps - FastAPI.pdf",
        "page_start": 1,
        "page_end": 1,
        "section_id": None,
        "section_path": [],
        "token_count": 10,
        "types": ["paragraph"],
    }
]

output_path = PROCESSED_DATA_DIR / "test.jsonl"

save_chunks(sample_chunks, output_path)

loaded_chunks = load_chunks(output_path)

print("Saved:", len(sample_chunks))
print("Loaded:", len(loaded_chunks))
print("Data matches:", sample_chunks == loaded_chunks)
