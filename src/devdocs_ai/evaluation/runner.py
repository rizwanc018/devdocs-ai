import json
from pathlib import Path

from devdocs_ai.evaluation.judge import evaluate_answer
from devdocs_ai.generation.pipeline import answer_question
from devdocs_ai.retrieval.reranked_retrieval import reranked_retriever


def run_answer_evaluation(
    dataset_path: str,
    output_path: str,
    embedding_model,
    table,
    bm25,
    reranker,
    client,
):
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)

    with dataset_path.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    evaluation_results = []

    for index, test_case in enumerate(test_cases, start=1):
        query = test_case["question"]
        expected_points = test_case.get("expected_answer_points", [])
        should_abstain = test_case.get("should_abstain", False)

        print(f"\n[{index}/{len(test_cases)}] Evaluating: {query}")

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

        # 3. Evaluate the generated answer
        evaluation = evaluate_answer(
            query=query,
            expected_answer_points=expected_points,
            should_abstain=should_abstain,
            chunks=chunks,
            result=result,
            client=client,
        )

        # 4. Store the answer and evaluation
        evaluation_results.append(
            {
                "question": query,
                "should_abstain": should_abstain,
                "answer": result["answer"],
                "sources": result["sources"],
                "retrieved_chunk_ids": [chunk["chunk_id"] for chunk in chunks],
                "evaluation": evaluation.model_dump(),
            }
        )

        print("Faithfulness:", evaluation.faithfulness)
        print("Answer relevance:", evaluation.answer_relevance)
        print("Citation correctness:", evaluation.citation_correctness)
        print("Context relevance:", evaluation.context_relevance)
        print(
            "Abstention handled correctly:",
            evaluation.abstention_handling_correct,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            evaluation_results,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\nEvaluation completed.")
    print(f"Results saved to: {output_path}")

    return evaluation_results
