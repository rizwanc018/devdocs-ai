import json
from statistics import mean

from devdocs_ai.config.path import EVAL_DATASET_DIR

RESULTS_PATH = EVAL_DATASET_DIR / "answer_evaluation_results.json"

SCORE_FIELDS = [
    "faithfulness",
    "answer_relevance",
    "citation_correctness",
    "context_relevance",
]


def main():
    with RESULTS_PATH.open("r", encoding="utf-8") as file:
        results = json.load(file)

    if not results:
        print("No evaluation results found.")
        return

    print("\nANSWER EVALUATION REPORT")
    print("=" * 45)

    print(f"Total questions: {len(results)}")

    print("\nAVERAGE SCORES")
    print("-" * 45)

    for field in SCORE_FIELDS:
        scores = [item["evaluation"][field] for item in results]

        print(f"{field}: {mean(scores):.2f}/5")

    correct_abstentions = sum(
        item["evaluation"]["abstention_handling_correct"] for item in results
    )

    print("\nABSTENTION HANDLING")
    print("-" * 45)

    print(f"Correct decisions: {correct_abstentions}/{len(results)}")

    print(f"Accuracy: {correct_abstentions / len(results) * 100:.2f}%")


if __name__ == "__main__":
    main()
