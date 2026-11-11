from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from .models import Response
from .sessions import Session


def iter_pages(
    session: Session, url: str, max_pages: int = 10, **kwargs: Any
) -> Iterator[Response]:
    """Yields each page of a paginated API by following ``rel=next`` links."""
    for _ in range(max_pages + 1):
        response = session.get(url, **kwargs)
        yield response
        url = response.links["next"]["url"]

        if not url:
            break


def collect_items(
    session: Session, url: str, key: str = "items", **kwargs: Any
) -> list[Any]:
    items: list[Any] = []

    for page in iter_pages(session, url, **kwargs):
        items.extend(page.json()[key])

    return items


def next_request_url(response: Response) -> str:
    return response.next.url
