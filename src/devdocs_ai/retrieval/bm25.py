import bm25s
import numpy as np

from devdocs_ai.config.path import BM25_INDEXES_DIR


def build_bm25_index(chunks: list[dict]):

    if not chunks:
        raise ValueError("Cannot build BM25 index from empty chunks.")

    texts = []
    for chunk in chunks:
        owner_id = chunk.get("owner_id")

        if not isinstance(owner_id, str):
            raise TypeError(
                f"Chunk {chunk.get('chunk_id')} owner_id must be a string, "
                f"got {type(owner_id).__name__}."
            )

        if not owner_id.strip():
            raise ValueError(f"Chunk {chunk.get('chunk_id')} has no valid owner_id.")

        texts.append(chunk["text"])

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


def bm25_retriever(
    query: str, retriever: bm25s.BM25, owner_id: str, top_k: int = 5
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    if not owner_id:
        raise ValueError("owner id is required.")

    # Loading corpus because ownership is stored in its records.
    corpus = retriever.corpus

    if corpus is None:
        raise ValueError("BM25 corpus must be loaded.")

    for chunk in corpus:
        weight_mask = np.array(
            [chunk["owner_id"] == owner_id for chunk in corpus], dtype=np.float32
        )

    if not np.any(weight_mask):
        return []

    query_tokens = bm25s.tokenize(query, stopwords="en")
    k = min(top_k, len(corpus))

    results, scores = retriever.retrieve(query_tokens, k=k, weight_mask=weight_mask)

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
