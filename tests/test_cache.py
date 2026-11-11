import requests
from requests.cache import DiskCache, cache_key


def _response(body):
    response = requests.Response()
    response.status_code = 200
    response._content = body
    return response


def test_roundtrip(tmp_path):
    cache = DiskCache(str(tmp_path))
    cache.set("abc", _response(b"hello"))
    assert cache.get("abc").content == b"hello"


def test_missing_key_returns_none(tmp_path):
    assert DiskCache(str(tmp_path)).get("missing") is None


def test_cache_key_depends_on_url():
    first = requests.Request("GET", "http://example.com/a").prepare()
    second = requests.Request("GET", "http://example.com/b").prepare()
    assert cache_key(first) != cache_key(second)
