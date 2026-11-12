import json

from devdocs_ai.config.path import PROCESSED_DATA_DIR

CATALOG_PATH = PROCESSED_DATA_DIR / "metadata_catalog.json"


def build_metadata_catalog(chunks: list[dict]) -> dict:
    sources = set()
    topics = set()
    pages = set()

    for chunk in chunks:
        if chunk.get("source"):
            sources.add(chunk["source"])

        for section in chunk.get("section_path") or []:
            if section.strip():
                topics.add(section.strip())

        start = chunk.get("page_start")
        end = chunk.get("page_end")

        if start is not None and end is not None:
            pages.update(range(start, end + 1))

    return {
        "technology": ["FastAPI"],
        "document_type": ["pdf"],
        "source": sorted(sources),
        "topic": sorted(topics),
        "page": sorted(pages),
    }


def save_metadata_catalog(catalog: dict):
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CATALOG_PATH.open("w", encoding="utf-8") as file:
        json.dump(catalog, file, indent=4, ensure_ascii=False)


def load_metadata_catalog() -> dict:
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Metadata catalog not found: {CATALOG_PATH}")

    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)
