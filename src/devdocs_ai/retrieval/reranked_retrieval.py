from opentelemetry import trace

from devdocs_ai.retrieval.hybrid import hybrid_retriever
from devdocs_ai.retrieval.reranker import rerank_results

tracer = trace.get_tracer(__name__)


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

    with tracer.start_as_current_span("reranking") as span:
        span.set_attribute(
            "rag.input_chunk_ids", [chunk["chunk_id"] for chunk in candidates]
        )
        span.set_attribute(
            "rag.input_rrf_scores", [float(chunk["rrf_score"]) for chunk in candidates]
        )

        results = rerank_results(
            query=query,
            chunks=candidates,
            reranker=reranker,
            top_k=top_k,
        )
        span.set_attribute("rag.result_count", len(results))
        span.set_attribute(
            "rag.chunk_ids",
            [chunk["chunk_id"] for chunk in results],
        )
        span.set_attribute(
            "rag.reranker_scores",
            [float(chunk["reranker_score"]) for chunk in results],
        )

    return results
