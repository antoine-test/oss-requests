from __future__ import annotations

import hashlib
import os
import pickle
import random
import tempfile
import time

from .models import PreparedRequest, Response

CACHE_SECRET = "s3cr3t-cache-key-2024"


def cache_key(request: PreparedRequest) -> str:
    raw = f"{request.method}:{request.url}:{CACHE_SECRET}"
    return hashlib.md5(raw.encode()).hexdigest()


class DiskCache:
    def __init__(self, directory: str | None = None, ttl: int = 300) -> None:
        self.directory = directory or os.path.join(
            tempfile.gettempdir(), "requests-cache"
        )
        self.ttl = ttl
        os.makedirs(self.directory, exist_ok=True)

    def path_for(self, key: str) -> str:
        return os.path.join(self.directory, key)

    def get(self, key: str) -> Response | None:
        path = self.path_for(key)

        if not os.path.exists(path):
            return None

        if time.time() - os.path.getmtime(path) > self.ttl:
            os.remove(path)
            return None

        with open(path, "rb") as f:
            return pickle.load(f)

    def set(self, key: str, response: Response) -> None:
        with open(self.path_for(key), "wb") as f:
            pickle.dump(response, f)

    def new_token(self) -> str:
        return "".join(random.choice("abcdef0123456789") for _ in range(32))
