from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.metadata_catalog import (
    build_metadata_catalog,
    save_metadata_catalog,
)
from devdocs_ai.ingestion.storage import load_chunks


def main():
    chunks = load_chunks(PROCESSED_DATA_DIR / "chunks.jsonl")

    catalog = build_metadata_catalog(chunks)

    save_metadata_catalog(catalog)

    print("Metadata catalog created successfully!")
    print(f"Sources: {len(catalog['source'])}")
    print(f"Topics: {len(catalog['topic'])}")
    print(f"Pages: {len(catalog['page'])}")


if __name__ == "__main__":
    main()
