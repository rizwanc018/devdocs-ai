from dotenv import load_dotenv

from devdocs_ai.observability.tracing import setup_tracing
from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.reranked_retrieval import reranked_retriever
from devdocs_ai.retrieval.reranker import load_reranker
from devdocs_ai.retrieval.vector_store import connect_to_db


def main():
    load_dotenv()

    tracer_provider = setup_tracing()

    try:
        embedding_model = load_embedding_model()
        bm25 = load_bm25_index()
        reranker = load_reranker()

        db = connect_to_db()
        table = db.open_table("document_chunks")

        results = reranked_retriever(
            query="How can I define query parameters in FastAPI?",
            model=embedding_model,
            table=table,
            bm25=bm25,
            reranker=reranker,
            top_k=5,
            dense_candidates=15,
            bm25_candidates=15,
        )

        for rank, chunk in enumerate(results, start=1):
            print(
                rank,
                chunk["chunk_id"],
                chunk["reranker_score"],
            )

    finally:
        tracer_provider.shutdown()


if __name__ == "__main__":
    main()
