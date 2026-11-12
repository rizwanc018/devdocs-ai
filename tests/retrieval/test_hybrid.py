from devdocs_ai.ingestion.metadata_catalog import load_metadata_catalog
from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.hybrid import hybrid_retriever
from devdocs_ai.retrieval.metadata_extraction import extract_metadata
from devdocs_ai.retrieval.validate_metadata import validate_metadata
from devdocs_ai.retrieval.vector_store import (
    TABLE_NAME,
    connect_to_db,
)

QUERIES = [
    "How can I define query parameters in FastAPI?",
    "HTTPException",
    # "OAuth2PasswordBearer",
    # "How does middleware process requests and responses?",
    "How do I define a request body?",
]


def main():
    model = load_embedding_model()

    db = connect_to_db()
    table = db.open_table(TABLE_NAME)

    bm25 = load_bm25_index()
    catalog = load_metadata_catalog()

    for query in QUERIES:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)

        extracted_metadata = extract_metadata(query, catalog)
        metadata_filters = validate_metadata(extracted_metadata.model_dump(), catalog)
        print("Metadata filters:", metadata_filters)

        results = hybrid_retriever(
            query=query,
            model=model,
            table=table,
            bm25=bm25,
            top_k=5,
            dense_candidates=10,
            bm25_candidates=10,
        )

        for rank, chunk in enumerate(results, start=1):
            print("\n" + "-" * 60)
            # print(f"Rank: {rank}")
            print(f"Chunk ID: {chunk['chunk_id']}")
            print(f"Source: {chunk['source']}")
            # print(f"Page: {chunk['page_start']}")
            print(f"RRF Score: {chunk['rrf_score']:.6f}")
            print(f"Retrieved by: {chunk['retrieved_by']}")
            # print(f"Dense rank: {chunk['dense_rank']}")
            # print(f"BM25 rank: {chunk['bm25_rank']}")
            # print(f"Text: {chunk['text'][:400]}")


if __name__ == "__main__":
    main()
