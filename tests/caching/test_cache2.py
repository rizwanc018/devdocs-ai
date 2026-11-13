import time

from devdocs_ai.caching.cache import QueryCache


def test_ttl_expiration():
    print("\nTEST 1: TTL EXPIRATION")

    cache = QueryCache(max_size=10, ttl_seconds=1)

    cache.set("query-1", {"answer": "Hello"})

    print("Before expiration:", cache.get("query-1"))

    time.sleep(1.1)

    result = cache.get("query-1")

    print("After expiration:", result)

    assert result is None

    print("TTL expiration passed!")


def test_lru_eviction():
    print("\nTEST 2: LRU EVICTION")

    cache = QueryCache(max_size=2, ttl_seconds=60)

    cache.set("query-1", {"answer": "Answer 1"})
    cache.set("query-2", {"answer": "Answer 2"})

    # Access query-1, making it recently used.
    cache.get("query-1")

    # Cache is full, so query-2 should be evicted.
    cache.set("query-3", {"answer": "Answer 3"})

    print("Query 1:", cache.get("query-1"))
    print("Query 2:", cache.get("query-2"))
    print("Query 3:", cache.get("query-3"))

    assert cache.get("query-1") is not None
    assert cache.get("query-2") is None
    assert cache.get("query-3") is not None

    print("LRU eviction passed!")


def test_cache_isolation():
    print("\nTEST 3: CACHE ISOLATION")

    cache = QueryCache(max_size=10, ttl_seconds=60)

    original_result = {
        "answer": "Original answer",
        "sources": [{"chunk_id": "chunk-001"}],
    }

    cache.set("query-1", original_result)

    # Modify the original object after storing it.
    original_result["answer"] = "Modified outside cache"

    # Retrieve the cached result.
    cached_result = cache.get("query-1")

    print("Cached answer:", cached_result["answer"])

    # Modify the retrieved object.
    cached_result["sources"][0]["chunk_id"] = "modified-id"

    # Retrieve it again.
    second_result = cache.get("query-1")

    print("Cached chunk ID:", second_result["sources"][0]["chunk_id"])

    assert second_result["answer"] == "Original answer"
    assert second_result["sources"][0]["chunk_id"] == "chunk-001"

    print("Cache isolation passed!")


def main():
    test_ttl_expiration()
    test_lru_eviction()
    test_cache_isolation()

    print("\nAll cache behaviour tests passed!")


if __name__ == "__main__":
    main()
