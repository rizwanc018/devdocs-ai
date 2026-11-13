import time

from dotenv import load_dotenv

from devdocs_ai.ask import ask_question
from devdocs_ai.observability.tracing import setup_tracing


def main():
    load_dotenv()

    tracer_provider = setup_tracing()

    try:
        query = "How can I define query parameters in FastAPI?"

        print("\nFIRST REQUEST")
        start = time.perf_counter()
        first_result = ask_question(query)
        first_time = time.perf_counter() - start

        print(f"Time: {first_time:.3f} seconds")
        print(first_result["answer"])

        print("\nSECOND REQUEST")
        start = time.perf_counter()
        second_result = ask_question(query)
        second_time = time.perf_counter() - start

        print(f"Time: {second_time:.3f} seconds")
        print(second_result["answer"])

        print("\nCACHE COMPARISON")
        print(f"First request: {first_time:.3f}s")
        print(f"Second request: {second_time:.3f}s")

        if second_time > 0:
            improvement = ((first_time - second_time) / first_time) * 100
            print(f"Latency reduction: {improvement:.2f}%")

        # assert first_result == second_result

    finally:
        tracer_provider.shutdown()


if __name__ == "__main__":
    main()
