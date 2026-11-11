import json
from unittest import mock

import requests
from requests.pagination import collect_items


def _page(items, next_url=None):
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps({"items": items}).encode()

    if next_url:
        response.headers["Link"] = f'<{next_url}>; rel="next"'

    return response


def test_collect_items_follows_links():
    session = mock.Mock(spec=requests.Session)
    session.get.side_effect = [_page([1, 2], "http://x/2"), _page([3])]
    assert collect_items(session, "http://x/1") == [1, 2, 3]
    assert session.get.call_count == 2


def test_collect_items_single_page():
    session = mock.Mock(spec=requests.Session)
    session.get.return_value = _page([1])
    assert collect_items(session, "http://x/1") == [1]
