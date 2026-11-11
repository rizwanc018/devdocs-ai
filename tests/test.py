from devdocs_ai.ingestion.normalizer import normalize_text

sample = """
    # FastAPI

    Hello World.


    def greet():
        print("Hello")
"""

normalized = normalize_text(sample)

print(normalized)
