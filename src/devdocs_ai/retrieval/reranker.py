from sentence_transformers import CrossEncoder

MODEL_NAME = "BAAI/bge-reranker-base"


def load_reranker():
    return CrossEncoder(
        MODEL_NAME,
        max_length=512,
    )


def rerank_results(
    query: str,
    chunks: list[dict],
    reranker,
    top_k: int = 5,
) -> list[dict]:

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    if not chunks:
        return []

    pairs = [(query, chunk["text"]) for chunk in chunks]

    scores = reranker.predict(pairs)

    reranked_chunks = []

    for chunk, score in zip(chunks, scores):
        reranked_chunks.append({**chunk, "reranker_score": float(score)})

    reranked_chunks.sort(
        key=lambda chunk: chunk["reranker_score"],
        reverse=True,
    )

    return reranked_chunks[:top_k]
