import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-base-en-v1.5"


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_documents(
    texts: list[str], model: SentenceTransformer, batch_size: int = 32
) -> np.ndarray:
    if not texts:
        raise ValueError("Texts cannot be empty.")

    embeddings = model.encode(
        texts, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=True
    )

    return np.asarray(embeddings, dtype=np.float32)


def embed_query(query: str, model: SentenceTransformer) -> np.ndarray:
    if not query.strip():
        raise ValueError("query cannot be empty")

    embedding = model.encode(
        query,
        convert_to_numpy=True,
    )

    return np.asarray(embedding, dtype=np.float32)


def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    embeddings = np.asarray(embeddings, dtype=np.float32)

    if embeddings.ndim != 2:
        raise ValueError("Expected a 2D embedding matrix")

    if not np.isfinite(embeddings).all():
        raise ValueError("Embeddings contain invalid values")

    norms = np.linalg.norm(embeddings, axis=1, keepdims=2)

    if np.any(norms == 0):
        raise ValueError("Cannot normalize zero vectors")

    return embeddings / norms
