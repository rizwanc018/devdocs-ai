from pathlib import Path

import lancedb
import numpy as np
import pyarrow as pa

from devdocs_ai.config.path import LANCE_DB_DIR


def connect_to_db(db_path: str | Path = LANCE_DB_DIR):
    db_path = Path(db_path)
    db_path.mkdir(parents=True, exist_ok=True)

    return lancedb.connect(str(db_path))


def prepare_records(chunks: list[dict], embeddings: np.ndarray) -> list[dict]:
    embeddings = np.asarray(embeddings, dtype=np.float32)

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match")

    records = []

    for chunk, embedding in zip(chunks, embeddings):
        records.append(
            {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "text": chunk["text"],
                "source": chunk["source"],
                "page_start": chunk.get("page_start"),
                "page_end": chunk.get("page_end"),
                "section_id": (
                    str(chunk["section_id"])
                    if chunk.get("section_id") is not None
                    else None
                ),
                "section_path": chunk.get("section_path") or [],
                "token_count": chunk.get("token_count"),
                "types": chunk.get("types") or [],
                "vector": embedding.tolist(),
            }
        )

    return records


TABLE_NAME = "document_chunks"
VECTOR_DIMENSION = 768


def create_vector_table(db, records: list[dict], table_name: str = TABLE_NAME):

    if not records:
        raise ValueError("Cannot create a table without records")

    schema = pa.schema(
        [
            pa.field("chunk_id", pa.string()),
            pa.field("document_id", pa.string()),
            pa.field("text", pa.string()),
            pa.field("source", pa.string()),
            pa.field("page_start", pa.int64()),
            pa.field("page_end", pa.int64()),
            pa.field("section_id", pa.string()),
            pa.field("section_path", pa.list_(pa.string())),
            pa.field("token_count", pa.int64()),
            pa.field("types", pa.list_(pa.string())),
            pa.field(
                "vector",
                pa.list_(pa.float32(), VECTOR_DIMENSION),
            ),
        ]
    )

    arrow_table = pa.Table.from_pylist(
        records,
        schema=schema,
    )

    table = db.create_table(
        table_name,
        schema=schema,
        mode="overwrite",
    )

    table.add(arrow_table)

    return table
