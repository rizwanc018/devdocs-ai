from devdocs_ai.retrieval.bm25 import bm25_retriever
from devdocs_ai.retrieval.dense import dense_search
from devdocs_ai.retrieval.metadata_filter import filter_chunks
from devdocs_ai.retrieval.rrf import reciprocal_rank_fusion


def hybrid_retriever(
    query: str,
    model,
    table,
    bm25,
    top_k: int = 5,
    dense_candidates: int = 10,
    bm25_candidates: int = 10,
    rrf_k: int = 60,
    metadata_filters: dict | None = None,
) -> list[dict]:

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    dense_results = dense_search(
        query=query, model=model, table=table, top_k=dense_candidates
    )

    bm25_results = bm25_retriever(query=query, retriever=bm25, top_k=bm25_candidates)

    candidate_count = len(dense_results) + len(bm25_results)

    hybrid_results = reciprocal_rank_fusion(
        dense_results=dense_results,
        bm25_results=bm25_results,
        top_k=candidate_count,
        k=rrf_k,
    )

    if metadata_filters:
        hybrid_results = filter_chunks(
            chunks=hybrid_results,
            metadata_filters=metadata_filters,
        )

    return hybrid_results[:top_k]
