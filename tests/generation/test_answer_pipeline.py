from pprint import pprint

from devdocs_ai.generation.generator import load_llm_client
from devdocs_ai.generation.pipeline import answer_question

chunks = [
    {
        "chunk_id": "query-parameters-fastapi-0001",
        "source": "Query Parameters - FastAPI.pdf",
        "page_start": 2,
        "page_end": 3,
        "section_path": ["Query Parameters"],
        "text": """
        When you declare other function parameters that are
        not part of the path parameters, they are automatically
        interpreted as query parameters.

        Example:

        @app.get("/items/")
        async def read_item(skip: int = 0, limit: int = 10):
            return fake_items_db[skip : skip + limit]
        """,
    },
    {
        "chunk_id": "query-parameters-fastapi-0003",
        "source": "Query Parameters - FastAPI.pdf",
        "page_start": 4,
        "page_end": 4,
        "section_path": ["Query Parameters", "Optional parameters"],
        "text": """
        You can declare optional query parameters by setting
        their default to None.
        """,
    },
]

query = "How does PostgreSQL handle database transactions?"
client = load_llm_client()

result = answer_question(
    query=query,
    chunks=chunks,
    client=client,
)

pprint(result)
