import time
from collections import OrderedDict
from copy import deepcopy
from threading import Lock


class QueryCache:
    def __init__(self, max_size: int = 100, ttl_seconds: int = 3000):
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")

        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

        self.cache = OrderedDict()

        self.lock = Lock()

    def get(self, key: str):
        with self.lock:
            entry = self.cache.get(key)

            if entry is None:
                return None

            value, expires_at = entry

            if time.monotonic() >= expires_at:
                self.cache.pop(key)
                return None

            self.cache.move_to_end(key)

            return deepcopy(value)

    def set(self, key: str, value):
        with self.lock:
            expires_at = time.monotonic() + self.ttl_seconds

            self.cache.pop(key, None)

            self.cache[key] = (
                deepcopy(value),
                expires_at,
            )

            # Remove least recently used entries
            while len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

    def clear(self):
        with self.lock:
            self.cache.clear()

    def __len__(self):
        with self.lock:
            return len(self.cache)
