from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.storage import load_chunks
from devdocs_ai.retrieval.embeddings import (
    embed_documents,
    embed_query,
    load_embedding_model,
    normalize_embeddings,
)

chunks = load_chunks(PROCESSED_DATA_DIR / "chunks.jsonl")
texts = [chunk["text"] for chunk in chunks]
print("Total documents:", len(texts))

model = load_embedding_model()
embeddings = embed_documents(texts, model)
print("Embedding shape:", embeddings.shape)

# Normalize document embeddings
normalized = normalize_embeddings(embeddings)
print("Normalized shape:", normalized.shape)

# Generate query embedding
query = "How do I define query parameters in FastAPI?"
query_embedding = embed_query(query, model)
print("Query shape:", query_embedding.shape)


# Normalize query embedding
query_embedding = normalize_embeddings(query_embedding.reshape(1, -1))
print("Query embedding shape:", query_embedding.shape)

# Verify normalization
print(
    "Document vector norm:",
    normalized[0].dot(normalized[0]) ** 0.5,
)

print(
    "Query vector norm:",
    query_embedding[0].dot(query_embedding[0]) ** 0.5,
)
