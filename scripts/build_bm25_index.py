from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.storage import load_chunks
from devdocs_ai.retrieval.bm25 import build_bm25_index

CHUNKS_PATH = PROCESSED_DATA_DIR / "chunks.jsonl"


def main():
    chunks = load_chunks(CHUNKS_PATH)

    retriever = build_bm25_index(chunks)

    print("BM25 index created successfully!")
    print(f"Total chunks indexed: {len(chunks)}")


if __name__ == "__main__":
    main()
