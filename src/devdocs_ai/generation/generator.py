import os

from dotenv import load_dotenv
from openai import OpenAI

from devdocs_ai.generation.prompt import SYSTEM_PROMPT, build_user_prompt
from devdocs_ai.schema.answer import GeneratedAnswer

load_dotenv()


def load_llm_client():
    return OpenAI()


def generate_answer(
    query: str,
    chunks: list[dict],
    client: OpenAI,
    model: str | None = None,
) -> GeneratedAnswer:

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if not chunks:
        return GeneratedAnswer(
            answer="I couldn't find relevant documentation to answer this question.",
            cited_chunk_ids=[],
        )

    model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    user_prompt = build_user_prompt(
        query=query,
        chunks=chunks,
    )

    response = client.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        response_format=GeneratedAnswer,
    )

    message = response.choices[0].message

    if message.refusal:
        raise RuntimeError(f"LLM refused to answer: {message.refusal}")

    if message.parsed is None:
        raise RuntimeError("LLM returned no structured answer")

    return message.parsed
