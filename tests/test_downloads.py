import io
from unittest import mock

import pytest

import requests
from requests.downloads import download


def _response(body, status=200):
    response = requests.Response()
    response.status_code = status
    response.raw = io.BytesIO(body)
    return response


def test_download_writes_file(tmp_path):
    target = tmp_path / "out.bin"

    with mock.patch.object(
        requests.Session, "get", return_value=_response(b"hello world")
    ):
        assert download("http://example.com/f", str(target), chunk_size=4) == 11

    assert target.read_bytes() == b"hello world"


def test_download_http_error_leaves_no_file(tmp_path):
    target = tmp_path / "out.bin"

    with mock.patch.object(
        requests.Session, "get", return_value=_response(b"", status=404)
    ):
        with pytest.raises(requests.HTTPError):
            download("http://example.com/f", str(target))

    assert list(tmp_path.iterdir()) == []
