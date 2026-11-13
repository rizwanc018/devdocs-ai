from pydantic import BaseModel, Field


class GeneratedAnswer(BaseModel):
    answer: str = Field(description="Answer grounded in the retrieved documentation")

    cited_chunk_ids: list[str] = Field(
        description="IDs of retrieved chunks that support the answer"
    )
