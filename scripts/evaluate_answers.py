from dotenv import load_dotenv

from devdocs_ai.config.path import EVAL_DATASET_DIR
from devdocs_ai.evaluation.runner import run_answer_evaluation
from devdocs_ai.generation.generator import load_llm_client
from devdocs_ai.retrieval.bm25 import load_bm25_index
from devdocs_ai.retrieval.embeddings import load_embedding_model
from devdocs_ai.retrieval.reranker import load_reranker
from devdocs_ai.retrieval.vector_store import connect_to_db


def main():
    load_dotenv()

    print("Loading embedding model...")
    embedding_model = load_embedding_model()

    print("Loading reranker...")
    reranker = load_reranker()

    print("Loading BM25 index...")
    bm25 = load_bm25_index()

    print("Connecting to LanceDB...")
    db = connect_to_db()
    table = db.open_table("document_chunks")

    print("Loading OpenAI client...")
    client = load_llm_client()

    dataset_path = EVAL_DATASET_DIR / "answer_evaluation.json"
    output_path = EVAL_DATASET_DIR / "answer_evaluation_results.json"

    run_answer_evaluation(
        dataset_path=dataset_path,
        output_path=output_path,
        embedding_model=embedding_model,
        table=table,
        bm25=bm25,
        reranker=reranker,
        client=client,
    )


if __name__ == "__main__":
    main()
