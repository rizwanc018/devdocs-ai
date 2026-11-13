from devdocs_ai.retrieval.hybrid import hybrid_retriever
from devdocs_ai.retrieval.reranker import rerank_results


def reranked_retriever(
    query: str,
    model,
    table,
    bm25,
    reranker,
    top_k: int = 5,
    dense_candidates: int = 20,
    bm25_candidates: int = 20,
    rrf_k: int = 60,
    metadata_filters: dict | None = None,
) -> list[dict]:

    candidates = hybrid_retriever(
        query=query,
        model=model,
        table=table,
        bm25=bm25,
        top_k=dense_candidates + bm25_candidates,
        dense_candidates=dense_candidates,
        bm25_candidates=bm25_candidates,
        rrf_k=rrf_k,
        metadata_filters=metadata_filters,
    )

    results = rerank_results(
        query=query,
        chunks=candidates,
        reranker=reranker,
        top_k=top_k,
    )

    return results
