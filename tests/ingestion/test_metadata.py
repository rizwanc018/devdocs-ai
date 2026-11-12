from pathlib import Path

from devdocs_ai.ingestion.metadata import build_chunk_metadata

file_path = Path("data/raw/First Steps - FastAPI.pdf")

sample_metadata = {
    "page_start": 1,
    "page_end": 2,
    "section_id": None,
    "section_path": [],
    "token_count": 120,
    "types": ["paragraph"],
}

result = build_chunk_metadata(
    file_path=file_path,
    chunk_index=0,
    metadata=sample_metadata,
)

print(result)
