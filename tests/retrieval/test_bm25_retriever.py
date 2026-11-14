from devdocs_ai.auth.database import get_connection
from devdocs_ai.retrieval.bm25 import (
    bm25_retriever,
    load_bm25_index,
)

with get_connection() as connection:
    user = connection.execute("SELECT id FROM users LIMIT 1").fetchone()

owner_id = user["id"]
retriever = load_bm25_index()

query = "How can I define query parameters in FastAPI?"
owner_results = bm25_retriever(
    query=query,
    retriever=retriever,
    owner_id=owner_id,
    top_k=5,
)

assert owner_results, "Owner should retrieve their documents."
assert all(chunk["owner_id"] == owner_id for chunk in owner_results)

print("Owner BM25 retrieval passed!")

other_user_id = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
other_results = bm25_retriever(
    query=query,
    retriever=retriever,
    owner_id=other_user_id,
    top_k=5,
)

assert len(other_results) == 0

print("Cross-user BM25 isolation passed!")
print("All BM25 authorization tests passed!")
