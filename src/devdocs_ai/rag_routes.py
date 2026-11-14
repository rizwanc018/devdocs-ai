from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from devdocs_ai.ask import ask_question
from devdocs_ai.auth.routes import get_current_user

router = APIRouter(tags=["RAG"])


class AskRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)


@router.post("/ask")
def ask(request: AskRequest, curr_user: dict = Depends(get_current_user)):  # noqa: B008
    try:
        return ask_question(query=request.query, owner_id=curr_user["id"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
