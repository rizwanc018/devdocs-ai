from pydantic import BaseModel, Field


class QueryMetadata(BaseModel):
    source: list[str] = Field(
        description="Document filenames explicitly requested by the user"
    )

    topic: list[str] = Field(
        description="Document topics explicitly requested by the user"
    )
