import json
import os

from openai import OpenAI

from devdocs_ai.schema.answer_evaluation import AnswerEvaluation

JUDGE_SYSTEM_PROMPT = """
You are an evaluator for a documentation-based RAG system.

Evaluate the generated answer using only the supplied question,
expected answer points, retrieved documentation, and citations.

Do not use outside knowledge to establish factual correctness.

Score each dimension from 1 to 5.

1. Faithfulness:
   Are the answer's factual claims supported by the retrieved context?

2. Answer relevance:
   Does the answer address the user's question and cover the
   expected answer points where applicable?

3. Citation correctness:
   Do the cited chunks actually support the claims they are
   associated with? Do not consider an ID valid merely because
   it exists.

4. Context relevance:
   Is the retrieved documentation relevant and sufficient to
   answer the question?

Abstention handling:
- If the question should be answerable, the assistant should
  provide a supported answer.
- If the question should be unanswerable, the assistant should
  clearly say the available documentation is insufficient.
- Set abstention_handling_correct to true when the assistant
  handles this appropriately.

Important:
- Do not reward unsupported claims.
- Do not assume a citation supports a claim without checking
  its actual text.
- A correct refusal for an unanswerable question is not a
  faithfulness failure.
- If the context is insufficient, explain that in your reasoning.
"""


def evaluate_answer(
    query: str,
    expected_answer_points: list[str],
    should_abstain: bool,
    chunks: list[dict],
    result: dict,
    client: OpenAI,
    model: str | None = None,
) -> AnswerEvaluation:

    if not query.strip():
        raise ValueError("Query cannot be empty")

    model = model or os.getenv(
        "OPENAI_EVAL_MODEL",
        "gpt-4.1-mini",
    )

    evaluation_input = {
        "question": query,
        "expected_answer_points": expected_answer_points,
        "should_abstain": should_abstain,
        "retrieved_chunks": chunks,
        "generated_answer": result["answer"],
        "citations": result["sources"],
    }

    response = client.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": JUDGE_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(
                    evaluation_input,
                    ensure_ascii=False,
                ),
            },
        ],
        response_format=AnswerEvaluation,
    )

    message = response.choices[0].message

    if message.refusal:
        raise RuntimeError(f"Evaluation judge refused: {message.refusal}")

    if message.parsed is None:
        raise RuntimeError("Evaluation judge returned no structured result")

    return message.parsed
