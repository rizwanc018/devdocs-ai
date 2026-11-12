from devdocs_ai.ingestion.metadata_catalog import load_metadata_catalog
from devdocs_ai.retrieval.metadata_extraction import extract_metadata


def main():
    catalog = load_metadata_catalog()

    queries = [
        "Explain middleware",
        "How can I define query parameters in FastAPI?",
        "Explain OAuth2PasswordBearer",
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print("QUERY:", query)

        metadata = extract_metadata(query, catalog)

        print("EXTRACTED METADATA:")
        print(metadata)


if __name__ == "__main__":
    main()
