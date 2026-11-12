from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.metadata_catalog import load_metadata_catalog
from devdocs_ai.ingestion.storage import load_chunks
from devdocs_ai.retrieval.metadata_pipeline import apply_metadata_filters


def main():
    chunks = load_chunks(PROCESSED_DATA_DIR / "chunks.jsonl")
    catalog = load_metadata_catalog()

    queries = [
        "Explain middleware",
        "How can I define query parameters in FastAPI?",
        "Explain OAuth2PasswordBearer.",
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print("QUERY:", query)

        filtered_chunks = apply_metadata_filters(
            query=query,
            chunks=chunks,
            catalog=catalog,
        )

        print(f"\nOriginal chunks: {len(chunks)}")
        print(f"Filtered chunks: {len(filtered_chunks)}")

        for chunk in filtered_chunks[:5]:
            print("\nChunk ID:", chunk["chunk_id"])
            print("Source:", chunk["source"])
            print("Section:", chunk["section_path"])
            print("Text:", chunk["text"][:200])


if __name__ == "__main__":
    main()
