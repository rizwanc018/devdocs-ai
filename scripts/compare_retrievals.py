from devdocs_ai.retrieval.bm25 import (
    load_bm25_index,
)
from devdocs_ai.retrieval.bm25_retriever import bm25_retriever
from devdocs_ai.retrieval.dense_retriever import dense_search
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.vector_store import (
    TABLE_NAME,
    connect_to_db,
)

QUERIES = [
    "How can I define query parameters in FastAPI?",
    "HTTPException",
    "OAuth2PasswordBearer",
    "How does middleware process requests and responses?",
    "How do I define a request body?",
]


def main():
    # Load both retrieval systems
    model = load_embedding_model()

    db = connect_to_db()
    table = db.open_table(TABLE_NAME)

    bm25 = load_bm25_index()

    for query in QUERIES:
        print("\n" + "=" * 90)
        print(f"QUERY: {query}")
        print("=" * 90)

        dense_results = dense_search(
            query=query,
            model=model,
            table=table,
            top_k=5,
        )

        bm25_results = bm25_retriever(
            query=query,
            retriever=bm25,
            top_k=5,
        )

        print("\nDENSE RETRIEVAL")
        for rank, chunk in enumerate(dense_results, start=1):
            print(
                f"{rank}. {chunk['chunk_id']} | Score: {chunk['similarity_score']:.4f}"
            )

        print("\nBM25 RETRIEVAL")
        for rank, chunk in enumerate(bm25_results, start=1):
            print(f"{rank}. {chunk['chunk_id']} | Score: {chunk['bm25_score']:.4f}")


if __name__ == "__main__":
    main()
