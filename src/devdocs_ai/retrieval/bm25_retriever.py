import bm25s


def bm25_retriever(query: str, retriever: bm25s.BM25, top_k: int = 5) -> list[dict]:
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    query_tokens = bm25s.tokenize(query, stopwords="en")

    results, scores = retriever.retrieve(query_tokens, k=top_k)

    retrieved_chunks = []

    for chunk, score in zip(results[0], scores[0]):
        score = float(score)
        if score <= 0:
            continue

        retrieved_chunks.append(
            {
                **chunk,
                "bm25_score": float(score),
            }
        )

    return retrieved_chunks
