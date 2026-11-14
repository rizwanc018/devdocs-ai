from devdocs_ai.auth.database import get_connection
from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.reranked_retrieval import reranked_retriever
from devdocs_ai.retrieval.reranker import load_reranker
from devdocs_ai.retrieval.vector_store import (
    TABLE_NAME,
    connect_to_db,
)

with get_connection() as connection:
    users = connection.execute(
        "SELECT id, email FROM users ORDER BY created_at"
    ).fetchall()

if len(users) < 2:
    raise RuntimeError("Register at least two users before running this test.")

owner_id = users[1]["id"]
other_user_id = users[2]["id"]

model = load_embedding_model()
reranker = load_reranker()

db = connect_to_db()
table = db.open_table(TABLE_NAME)
bm25 = load_bm25_index()

query = "How can I define query parameters in FastAPI?"


# Original document owner
owner_results = reranked_retriever(
    query=query,
    model=model,
    table=table,
    bm25=bm25,
    reranker=reranker,
    owner_id=owner_id,
    top_k=5,
)

assert owner_results, "Document owner should retrieve documents."

assert all(chunk["owner_id"] == owner_id for chunk in owner_results)

print("Owner retrieval passed!")


# Second user
other_results = reranked_retriever(
    query=query,
    model=model,
    table=table,
    bm25=bm25,
    reranker=reranker,
    owner_id=other_user_id,
    top_k=5,
)

assert other_results == [], "Second user retrieved documents they do not own!"

print("Cross-user retrieval isolation passed!")

print("\nAll cross-user retrieval tests passed!")
