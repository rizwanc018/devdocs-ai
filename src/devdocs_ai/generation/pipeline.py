from devdocs_ai.generation.citation import validate_citations
from devdocs_ai.generation.generator import generate_answer


def answer_question(
    query: str,
    chunks: list[dict],
    client,
    model: str | None = None,
) -> dict:

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if not chunks:
        return {
            "answer": "I couldn't find relevant documentation to answer this question.",
            "sources": [],
        }

    generated = generate_answer(
        query=query,
        chunks=chunks,
        client=client,
        model=model,
    )

    sources = validate_citations(
        cited_chunk_ids=generated.cited_chunk_ids, chunks=chunks
    )

    return {"answer": generated.answer, "sources": sources}
