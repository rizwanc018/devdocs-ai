import bm25s
from opentelemetry import trace

from devdocs_ai.retrieval.bm25 import bm25_retriever
from devdocs_ai.retrieval.dense import dense_search
from devdocs_ai.retrieval.metadata_filter import filter_chunks
from devdocs_ai.retrieval.rrf import reciprocal_rank_fusion

tracer = trace.get_tracer(__name__)


def hybrid_retriever(
    query: str,
    model,
    table,
    bm25: bm25s.BM25,
    owner_id: str,
    top_k: int = 5,
    dense_candidates: int = 10,
    bm25_candidates: int = 10,
    rrf_k: int = 60,
    metadata_filters: dict | None = None,
) -> list[dict]:

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    with tracer.start_as_current_span("dense_retrieval") as span:
        dense_results = dense_search(
            query=query,
            model=model,
            table=table,
            owner_id=owner_id,
            top_k=dense_candidates,
        )
        span.set_attribute("rag.query", query)
        span.set_attribute("rag.result_count", len(dense_results))
        span.set_attribute(
            "rag.chunk_ids",
            [chunk["chunk_id"] for chunk in dense_results],
        )
    with tracer.start_as_current_span("bm25_retrieval") as span:
        bm25_results = bm25_retriever(
            query=query, retriever=bm25, owner_id=owner_id, top_k=bm25_candidates
        )
        span.set_attribute("rag.query", query)
        span.set_attribute("rag.result_count", len(bm25_results))
        span.set_attribute(
            "rag.chunk_ids",
            [chunk["chunk_id"] for chunk in bm25_results],
        )

    if not dense_results and not bm25_results:
        return []

    candidate_count = len(dense_results) + len(bm25_results)

    with tracer.start_as_current_span("rrf_fusion") as span:
        hybrid_results = reciprocal_rank_fusion(
            dense_results=dense_results,
            bm25_results=bm25_results,
            top_k=candidate_count,
            k=rrf_k,
        )
        span.set_attribute("rag.result_count", len(hybrid_results))
        span.set_attribute(
            "rag.chunk_ids",
            [chunk["chunk_id"] for chunk in hybrid_results],
        )
        span.set_attribute(
            "rag.rrf_scores",
            [float(chunk["rrf_score"]) for chunk in hybrid_results],
        )

    if metadata_filters:
        hybrid_results = filter_chunks(
            chunks=hybrid_results,
            metadata_filters=metadata_filters,
        )

    return hybrid_results[:top_k]
