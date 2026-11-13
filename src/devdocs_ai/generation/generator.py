import os

from dotenv import load_dotenv
from openai import OpenAI
from opentelemetry import trace

from devdocs_ai.generation.prompt import SYSTEM_PROMPT, build_user_prompt
from devdocs_ai.schema.answer import GeneratedAnswer

load_dotenv()

tracer = trace.get_tracer(__name__)


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

    with tracer.start_as_current_span("answer_generation") as span:
        span.set_attribute("rag.query", query)
        span.set_attribute("llm.model", model)
        span.set_attribute("rag.input_chunk_count", len(chunks))

        user_prompt = build_user_prompt(
            query=query,
            chunks=chunks,
        )

        response = client.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format=GeneratedAnswer,
        )

        message = response.choices[0].message

        if message.refusal:
            span.set_attribute("llm.refusal", True)
            raise RuntimeError(f"LLM refused to answer: {message.refusal}")

        if message.parsed is None:
            raise RuntimeError("LLM returned no structured answer")

        generated = message.parsed

        span.set_attribute("output.value", generated.answer)
        span.set_attribute(
            "rag.cited_chunk_ids",
            generated.cited_chunk_ids,
        )

        return generated
