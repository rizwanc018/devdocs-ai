from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.hybrid import hybrid_retriever
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
    # Load retrieval components once
    model = load_embedding_model()

    db = connect_to_db()
    table = db.open_table(TABLE_NAME)

    bm25 = load_bm25_index()

    for query in QUERIES:
        print("\n" + "=" * 90)
        print(f"QUERY: {query}")
        print("=" * 90)

        results = hybrid_retriever(
            query=query,
            model=model,
            table=table,
            bm25=bm25,
            top_k=5,
            dense_candidates=10,
            bm25_candidates=10,
        )

        print(f"\nHYBRID RESULTS: {len(results)}")

        for rank, chunk in enumerate(results, start=1):
            print("\n" + "-" * 70)
            print(f"Rank: {rank}")
            print(f"Chunk ID: {chunk['chunk_id']}")
            print(f"Source: {chunk['source']}")
            print(f"Page: {chunk['page_start']}")
            print(f"RRF Score: {chunk['rrf_score']:.6f}")
            print(f"Retrieved by: {chunk['retrieved_by']}")
            print(f"Dense rank: {chunk['dense_rank']}")
            print(f"BM25 rank: {chunk['bm25_rank']}")
            print(f"Text: {chunk['text'][:400]}")


if __name__ == "__main__":
    main()
