from devdocs_ai.ingestion.metadata_catalog import load_metadata_catalog
from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.hybrid import hybrid_retriever
from devdocs_ai.retrieval.metadata_extraction import extract_metadata
from devdocs_ai.retrieval.reranker import (
    load_reranker,
    rerank_results,
)
from devdocs_ai.retrieval.validate_metadata import validate_metadata
from devdocs_ai.retrieval.vector_store import TABLE_NAME, connect_to_db

model = load_embedding_model()
db = connect_to_db()
table = db.open_table(TABLE_NAME)
bm25 = load_bm25_index()
catalog = load_metadata_catalog()


def print_results(title, results, score_key):
    print(f"\n{title}")

    for rank, chunk in enumerate(results[:5], start=1):
        print(f"\nRank: {rank}")
        print("Chunk:", chunk["chunk_id"])
        print("Score:", chunk[score_key])
        print("Text:", chunk["text"][:700])


def main():
    query = "How can I define query parameters in FastAPI?"

    extracted_metadata = extract_metadata(query, catalog)
    metadata_filters = validate_metadata(extracted_metadata.model_dump(), catalog)

    candidates = hybrid_retriever(
        query=query,
        model=model,
        table=table,
        bm25=bm25,
        top_k=30,
        dense_candidates=30,
        bm25_candidates=30,
        metadata_filters=metadata_filters,
    )

    reranker = load_reranker()

    reranked = rerank_results(
        query=query,
        chunks=candidates,
        reranker=reranker,
        top_k=5,
    )

    print("\nHYBRID RESULTS")

    for rank, chunk in enumerate(candidates[:5], start=1):
        print(
            rank,
            chunk["chunk_id"],
            chunk["rrf_score"],
        )

    print("\nRERANKED RESULTS")

    for rank, chunk in enumerate(reranked, start=1):
        print(
            rank,
            chunk["chunk_id"],
            chunk["reranker_score"],
        )

    print_results("HYBRID RESULTS", candidates, "rrf_score")
    print_results("RERANKED RESULTS", reranked, "reranker_score")


if __name__ == "__main__":
    main()
