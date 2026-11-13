from pydantic import BaseModel, Field


class AnswerEvaluation(BaseModel):
    faithfulness: int = Field(
        ge=1,
        le=5,
        description="How well the answer is supported by the retrieved context",
    )

    answer_relevance: int = Field(
        ge=1, le=5, description="How well the answer addresses the user's question"
    )

    citation_correctness: int = Field(
        ge=1, le=5, description="How accurately citations support the answer's claims"
    )

    context_relevance: int = Field(
        ge=1, le=5, description="How relevant the retrieved context is to the question"
    )
    reasoning: str = Field(description="Brief explanation for the assigned scores")

    abstention_handling_correct: bool = Field(
        description=(
            "Whether the assistant answered when sufficient context was available, and abstained when it was insufficient"
        )
    )
