from devdocs_ai.generation.citation import validate_citations

chunks = [
    {
        "chunk_id": "query-parameters-fastapi-0001",
        "source": "Query Parameters - FastAPI.pdf",
        "page_start": 2,
        "page_end": 3,
        "section_path": ["Query Parameters"],
        "text": "Other function parameters are query parameters.",
    },
    {
        "chunk_id": "query-parameters-fastapi-0003",
        "source": "Query Parameters - FastAPI.pdf",
        "page_start": 4,
        "page_end": 4,
        "section_path": ["Query Parameters", "Optional parameters"],
        "text": "Optional parameters can have a default value of None.",
    },
]

cited_chunk_ids = [
    "query-parameters-fastapi-0001",
    "nonexistent-chunk-9999",
    "query-parameters-fastapi-0003",
    "query-parameters-fastapi-0001",
]

sources = validate_citations(
    cited_chunk_ids=cited_chunk_ids,
    chunks=chunks,
)

print(sources)
