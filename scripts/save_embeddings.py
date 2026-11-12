from devdocs_ai.config.path import PROCESSED_DATA_DIR
from devdocs_ai.ingestion.storage import load_chunks
from devdocs_ai.retrieval.embeddings import (
    embed_documents,
    load_embedding_model,
    normalize_embeddings,
)
from devdocs_ai.retrieval.vector_store import (
    connect_to_db,
    create_vector_table,
    prepare_records,
)

chunks = load_chunks(PROCESSED_DATA_DIR / "chunks.jsonl")
print("Loaded chunks:", len(chunks))


model = load_embedding_model()


texts = [chunk["text"] for chunk in chunks]
embeddings = embed_documents(texts, model)


embeddings = normalize_embeddings(embeddings)
print("Embedding shape:", embeddings.shape)


records = prepare_records(chunks, embeddings)
print("Prepared records:", len(records))


db = connect_to_db()
table = create_vector_table(db, records)


print("Table created:", table.name)
print("Total records:", table.count_rows())
print("Table schema:")
print(table.schema)
