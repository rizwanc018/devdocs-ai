from pprint import pprint

from devdocs_ai.evaluation.judge import evaluate_answer
from devdocs_ai.generation.generator import load_llm_client
from devdocs_ai.generation.pipeline import answer_question

client = load_llm_client()

query = "How can I define query parameters in FastAPI?"

chunks = [
    {
        "chunk_id": "query-parameters-fastapi-0001",
        "source": "Query Parameters - FastAPI.pdf",
        "page_start": 2,
        "page_end": 3,
        "section_path": ["Query Parameters"],
        "text": """
        When you declare other function parameters that are
        not part of the path parameters, they are automatically
        interpreted as query parameters.

        You can define default values such as skip=0 and limit=10.
        """,
    },
    {
        "chunk_id": "query-parameters-fastapi-0003",
        "source": "Query Parameters - FastAPI.pdf",
        "page_start": 4,
        "page_end": 4,
        "section_path": ["Query Parameters", "Optional parameters"],
        "text": """
        You can declare optional query parameters by setting
        their default to None.
        """,
    },
]

result = answer_question(
    query=query,
    chunks=chunks,
    client=client,
)

print("GENERATED ANSWER:")
pprint(result)

evaluation = evaluate_answer(
    query=query,
    expected_answer_points=[
        "Non-path function parameters are interpreted as query parameters",
        "Query parameters can have default values",
        "Optional parameters can use None as their default",
    ],
    should_abstain=False,
    chunks=chunks,
    result=result,
    client=client,
)

print("\nEVALUATION:")
pprint(evaluation.model_dump())
