from devdocs_ai.auth.database import get_connection
from devdocs_ai.retrieval.dense import dense_search
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.vector_store import (
    TABLE_NAME,
    connect_to_db,
)

with get_connection() as connection:
    user = connection.execute("SELECT id FROM users LIMIT 1").fetchone()


owner_id = user["id"]

db = connect_to_db()
table = db.open_table(TABLE_NAME)
model = load_embedding_model()

query = "How can I define query parameters in FastAPI?"

# Search as the document owner.
owner_results = dense_search(
    query=query,
    model=model,
    table=table,
    owner_id=owner_id,
    top_k=5,
)

assert owner_results, "Owner should retrieve their documents."

assert all(chunk["owner_id"] == owner_id for chunk in owner_results)

print("Owner retrieval passed!")

# Search as another user.
other_user_id = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"

other_results = dense_search(
    query=query,
    model=model,
    table=table,
    owner_id=other_user_id,
    top_k=5,
)

assert len(other_results) == 0

print("Cross-user isolation passed!")
print("All dense authorization tests passed!")
