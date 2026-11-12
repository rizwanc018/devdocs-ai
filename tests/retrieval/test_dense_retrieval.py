from devdocs_ai.retrieval.dense_retriever import dense_search
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.vector_store import (
    TABLE_NAME,
    connect_to_db,
)

model = load_embedding_model()

db = connect_to_db()
table = db.open_table(TABLE_NAME)

query = "How can I define query parameters in FastAPI?"

results = dense_search(
    query=query,
    model=model,
    table=table,
    top_k=5,
)

print(f"\nQuery: {query}")
print(f"Retrieved chunks: {len(results)}")

for index, result in enumerate(results, start=1):
    print("\n" + "=" * 70)

    print(f"Rank: {index}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Source: {result['source']}")
    print(f"Pages: {result['page_start']} - {result['page_end']}")
    print(f"Similarity: {result['similarity_score']:.4f}")

    print("\nContent:")
    print(result["text"][:500])
