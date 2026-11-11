from devdocs_ai.ingestion.normalizer import normalize_chunks


def test_remove_document_title():
    chunks = [
        {
            "chunk_id": "c0",
            "text": "FastAPI Learn Tutorial - User Guide",
            "section_path": [],
        },
        {
            "chunk_id": "c1",
            "text": "# Query Parameters\n\nSome documentation.",
            "section_path": ["Query Parameters"],
        },
    ]

    result = normalize_chunks(chunks)

    assert len(result) == 1
    assert result[0]["chunk_id"] == "c1"


def test_preserve_meaningful_content_without_section():
    chunks = [
        {
            "chunk_id": "c0",
            "text": "Welcome to this documentation.",
            "section_path": [],
        }
    ]

    result = normalize_chunks(chunks)

    assert len(result) == 1


def test_remove_empty_chunks():
    chunks = [
        {
            "chunk_id": "c0",
            "text": "   \n\n  ",
            "section_path": [],
        }
    ]

    assert normalize_chunks(chunks) == []
