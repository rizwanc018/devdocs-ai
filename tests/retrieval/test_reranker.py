from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.storage import load_chunks
from devdocs_ai.retrieval.reranker import (
    load_reranker,
    rerank_results,
)


def main():
    query = "How can I define query parameters in FastAPI?"

    chunks = load_chunks(PROCESSED_DATA_DIR / "chunks.jsonl")

    candidates = [
        chunk for chunk in chunks if chunk["source"] == "Query Parameters - FastAPI.pdf"
    ][:10]

    reranker = load_reranker()

    results = rerank_results(
        query=query,
        chunks=candidates,
        reranker=reranker,
        top_k=5,
    )

    print("\nRERANKED RESULTS")

    for rank, chunk in enumerate(results, start=1):
        print("\nRank:", rank)
        print("Chunk ID:", chunk["chunk_id"])
        print("Reranker score:", f"{chunk['reranker_score']:.4f}")
        print("Text:", chunk["text"][:300])


if __name__ == "__main__":
    main()
