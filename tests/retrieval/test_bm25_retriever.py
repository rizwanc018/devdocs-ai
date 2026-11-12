from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.bm25_retriever import bm25_retriever


def main():
    retriever = load_bm25_index()

    query = "How can I define query parameters in FastAPI?"

    results = bm25_retriever(
        query=query,
        retriever=retriever,
        top_k=5,
    )

    print(f"\nQuery: {query}")
    print(f"Retrieved chunks: {len(results)}")

    for rank, chunk in enumerate(results, start=1):
        print("\n" + "=" * 70)
        print(f"Rank: {rank}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Source: {chunk['source']}")
        print(f"Page: {chunk['page_start']}")
        print(f"BM25 Score: {chunk['bm25_score']:.4f}")
        print(f"Text: {chunk['text']}")


if __name__ == "__main__":
    main()
