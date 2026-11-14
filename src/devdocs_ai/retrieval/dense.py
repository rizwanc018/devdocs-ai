from uuid import UUID

from sentence_transformers import SentenceTransformer

from devdocs_ai.retrieval.embeddings import (
    embed_query,
    normalize_embeddings,
)


def dense_search(
    query: str, model: SentenceTransformer, table, owner_id: str, top_k: int = 5
) -> list[dict]:

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    if not owner_id:
        raise ValueError("owner_id is required")

    owner_id = str(UUID(owner_id))

    query_embedding = embed_query(query, model)
    query_embedding = normalize_embeddings(query_embedding.reshape(1, -1))

    results = (
        table.search(query_embedding[0])
        .where(f"owner_id = '{owner_id}'", prefilter=True)
        .metric("cosine")
        .limit(top_k)
        .to_list()
    )

    for result in results:
        distance = result.pop("_distance", None)
        result.pop("vector", None)

        if distance is not None:
            result["similarity_score"] = 1.0 - distance

    return results
