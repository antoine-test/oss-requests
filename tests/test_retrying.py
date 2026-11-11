from unittest import mock

import pytest

import requests
from requests.exceptions import ConnectionError
from requests.retrying import RetryingSession


def _response(status):
    response = requests.Response()
    response.status_code = status
    return response


def test_returns_first_success():
    session = RetryingSession(delay=0)

    with mock.patch.object(
        requests.Session, "request", return_value=_response(200)
    ) as request:
        assert session.request("GET", "http://example.com").status_code == 200

    assert request.call_count == 1


def test_retries_on_server_error():
    session = RetryingSession(retries=3, delay=0)
    responses = [_response(503), _response(200)]

    with mock.patch.object(requests.Session, "request", side_effect=responses):
        assert session.request("GET", "http://example.com").status_code == 200


def test_gives_up_after_connection_errors():
    session = RetryingSession(retries=2, delay=0)

    with mock.patch.object(
        requests.Session, "request", side_effect=ConnectionError("boom")
    ):
        with pytest.raises(ConnectionError):
            session.request("GET", "http://example.com")
