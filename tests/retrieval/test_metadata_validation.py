from devdocs_ai.ingestion.metadata_catalog import (
    load_metadata_catalog,
)
from devdocs_ai.retrieval.validate_metadata import validate_metadata


def main():
    catalog = load_metadata_catalog()

    extracted_metadata = {
        "technology": ["FastAPI", "Redis"],
        "document_type": ["pdf"],
        "source": [
            "Middleware - FastAPI.pdf",
            "Redis Documentation",
        ],
        "topic": [
            "Create a middleware",
            "Unknown topic",
        ],
        "page": [2, 100],
        "author": ["John"],
    }

    validated = validate_metadata(
        extracted_metadata,
        catalog,
    )

    print("Validated metadata:")
    print(validated)


if __name__ == "__main__":
    main()
