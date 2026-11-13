from devdocs_ai.generation.generator import load_llm_client
from devdocs_ai.generation.pipeline import answer_question
from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.reranked_retrieval import reranked_retriever
from devdocs_ai.retrieval.reranker import load_reranker
from devdocs_ai.retrieval.vector_store import TABLE_NAME, connect_to_db

embedding_model = load_embedding_model()
reranker = load_reranker()

db = connect_to_db()
table = db.open_table(TABLE_NAME)

bm25 = load_bm25_index()

client = load_llm_client()


def ask_question(query: str):
    chunks = reranked_retriever(
        query=query,
        model=embedding_model,
        table=table,
        bm25=bm25,
        reranker=reranker,
        top_k=5,
        dense_candidates=30,
        bm25_candidates=30,
    )

    result = answer_question(
        query=query,
        chunks=chunks,
        client=client,
    )

    return result


if __name__ == "__main__":
    query = input("Ask a question: ")

    result = ask_question(query)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(f"- {source['source']}")
        print(f"  Pages: {source['page_start']} - {source['page_end']}")
        print(f"  Chunk: {source['chunk_id']}")
