import bm25s

from devdocs_ai.config.path import BM25_INDEXES_DIR


def build_bm25_index(chunks: list[dict]):
    if not chunks:
        raise ValueError("Cannot build BM25 index from empty chunks.")

    texts = [chunk["text"] for chunk in chunks]

    corpus_tokens = bm25s.tokenize(texts, stopwords="en")
    retriever = bm25s.BM25(corpus=chunks)
    retriever.index(corpus_tokens)  # Build the index

    BM25_INDEXES_DIR.mkdir(parents=True, exist_ok=True)
    retriever.save(
        str(BM25_INDEXES_DIR),
        corpus=chunks,
    )

    return retriever


def load_bm25_index():
    return bm25s.BM25.load(
        str(BM25_INDEXES_DIR),
        load_corpus=True,
    )


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
