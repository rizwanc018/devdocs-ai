from devdocs_ai.generation.generator import (
    generate_answer,
    load_llm_client,
)

chunks = [
    {
        "chunk_id": "query-parameters-fastapi-0001",
        "source": "Query Parameters - FastAPI.pdf",
        "page_start": 2,
        "page_end": 3,
        "text": """
        When you declare other function parameters that are
        not part of the path parameters, they are automatically
        interpreted as query parameters.

        For example:

        @app.get("/items/")
        async def read_item(skip: int = 0, limit: int = 10):
            return fake_items_db[skip : skip + limit]
        """,
    }
]

query = "How can I define query parameters in FastAPI?"

client = load_llm_client()

result = generate_answer(
    query=query,
    chunks=chunks,
    client=client,
)

print("ANSWER:")
print(result.answer)

print("\nCITED CHUNK IDS:")
print(result.cited_chunk_ids)

print("\nFULL RESPONSE:")
print(result.model_dump())
