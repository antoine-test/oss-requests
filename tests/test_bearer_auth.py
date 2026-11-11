import time

import requests
from requests.auth import BearerTokenAuth


def test_bearer_token_header():
    request = requests.Request(
        "GET", "http://example.com", auth=BearerTokenAuth("abc")
    ).prepare()
    assert request.headers["Authorization"] == "Bearer abc"


def test_token_is_refreshed_when_expired():
    auth = BearerTokenAuth("old", refresh=lambda: "new", expires_at=time.time() - 10)
    request = requests.Request("GET", "http://example.com", auth=auth).prepare()
    assert request.headers["Authorization"] == "Bearer new"


def test_token_is_kept_when_valid():
    auth = BearerTokenAuth("old", refresh=lambda: "new", expires_at=time.time() + 60)
    request = requests.Request("GET", "http://example.com", auth=auth).prepare()
    assert request.headers["Authorization"] == "Bearer old"
