from collections import Counter

from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.storage import load_chunks

chunks = load_chunks(PROCESSED_DATA_DIR / "chunks.jsonl")

print("Total chunks:", len(chunks))

print("\nDocuments:")
for source, count in Counter(c["source"] for c in chunks).items():
    print(f"{source}: {count} chunks")

print("\nEmpty chunks:", sum(not c["text"].strip() for c in chunks))

print(
    "Missing chunk IDs:",
    sum(not c.get("chunk_id") for c in chunks),
)

print(
    "Missing sources:",
    sum(not c.get("source") for c in chunks),
)
