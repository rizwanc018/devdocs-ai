from devdocs_ai.retrieval.bm25 import bm25_retriever
from devdocs_ai.retrieval.dense import dense_search
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
) -> list[dict]:

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    dense_results = dense_search(
        query=query, model=model, table=table, top_k=dense_candidates
    )

    bm25_results = bm25_retriever(query=query, retriever=bm25, top_k=bm25_candidates)

    hybrid_results = reciprocal_rank_fusion(
        dense_results=dense_results, bm25_results=bm25_results, top_k=top_k, k=rrf_k
    )

    return hybrid_results
