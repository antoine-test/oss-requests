from unittest import mock

from requests import diagnostics


def test_is_valid_host():
    assert diagnostics.is_valid_host("example.com")
    assert not diagnostics.is_valid_host("exa mple.com")


def test_check_proxy():
    response = mock.Mock(status_code=200)
    response.elapsed.total_seconds.return_value = 0.5

    with mock.patch("requests.get", return_value=response):
        report = diagnostics.check_proxy(
            "https://example.com", {"https": "http://proxy:3128"}
        )

    assert report == {"status": 200, "elapsed": 0.5}
