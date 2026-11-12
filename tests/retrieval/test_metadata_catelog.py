from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.metadata_catalog import build_metadata_catalog
from devdocs_ai.ingestion.storage import load_chunks


def main():
    chunks = load_chunks(PROCESSED_DATA_DIR / "chunks.jsonl")

    catalog = build_metadata_catalog(chunks)

    for field, values in catalog.items():
        print(f"\n{field}:")
        print(f"Total values: {len(values)}")
        print(values[:20])


if __name__ == "__main__":
    main()
