from dotenv import load_dotenv
from openai import OpenAI

from devdocs_ai.observability.tracing import setup_tracing


def main():
    load_dotenv()

    tracer_provider = setup_tracing()

    try:
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Explain what a Python function is in one sentence.",
                }
            ],
        )

        print(response.choices[0].message.content)

    finally:
        tracer_provider.shutdown()


if __name__ == "__main__":
    main()
