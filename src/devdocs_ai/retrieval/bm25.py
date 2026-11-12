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
