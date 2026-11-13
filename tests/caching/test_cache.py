import time

from devdocs_ai.caching.cache import QueryCache


def main():
    cache = QueryCache(
        max_size=2,
        ttl_seconds=2,
    )

    print("Initial lookup:", cache.get("query-1"))

    cache.set(
        "query-1",
        {"answer": "FastAPI uses Python type hints."},
    )

    # Test cache hit
    print("Cached lookup:", cache.get("query-1"))

    # Test LRU eviction
    cache.set("query-2", {"answer": "Answer 2"})
    cache.get("query-1")  # Mark query-1 as recently used
    cache.set("query-3", {"answer": "Answer 3"})

    print("Query 1 after eviction:", cache.get("query-1"))
    print("Query 2 after eviction:", cache.get("query-2"))
    print("Query 3 after eviction:", cache.get("query-3"))

    # Test expiration
    time.sleep(2.1)

    print("Query 3 after expiration:", cache.get("query-3"))


if __name__ == "__main__":
    main()
