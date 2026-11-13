from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from devdocs_ai.generation.generator import load_llm_client
from devdocs_ai.generation.pipeline import answer_question
from devdocs_ai.observability.tracing import setup_tracing
from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.reranked_retrieval import reranked_retriever
from devdocs_ai.retrieval.reranker import load_reranker
from devdocs_ai.retrieval.vector_store import TABLE_NAME, connect_to_db

tracer = trace.get_tracer(__name__)

embedding_model = load_embedding_model()
reranker = load_reranker()

db = connect_to_db()
table = db.open_table(TABLE_NAME)

bm25 = load_bm25_index()

client = load_llm_client()


def ask_question(query: str):
    with tracer.start_as_current_span("rag_request") as span:
        span.set_attribute("input.value", query)

        try:
            chunks = reranked_retriever(
                query=query,
                model=embedding_model,
                table=table,
                bm25=bm25,
                reranker=reranker,
                top_k=5,
                dense_candidates=15,
                bm25_candidates=15,
            )

            result = answer_question(
                query=query,
                chunks=chunks,
                client=client,
            )

            span.set_attribute("output.value", result["answer"])
            span.set_attribute("rag.source_count", len(result["sources"]))

            return result
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            raise


if __name__ == "__main__":
    query = input("Ask a question: ")
    tracer_provider = setup_tracing()
    try:
        result = ask_question(query)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(f"- {source['source']}")
            print(f"  Pages: {source['page_start']} - {source['page_end']}")
            print(f"  Chunk: {source['chunk_id']}")
    finally:
        tracer_provider.shutdown()
