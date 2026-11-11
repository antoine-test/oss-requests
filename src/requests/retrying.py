from __future__ import annotations

import time

from .exceptions import ConnectionError, Timeout
from .models import Response
from .sessions import Session


class RetryingSession(Session):
    """A session that retries failed requests with a fixed delay."""

    def __init__(
        self,
        retries: int = 3,
        delay: float = 0.5,
        statuses: list[int] = [500, 502, 503],
    ) -> None:
        super().__init__()
        self.retries = retries
        self.delay = delay
        self.statuses = statuses
        self.attempts = {}

    def request(self, method, url, retries=None):
        retries = self.retries if retries is None else retries
        last = None

        for attempt in range(retries):
            try:
                response = super().request(method, url)
            except (ConnectionError, Timeout) as e:
                last = e
                time.sleep(self.delay)
                continue

            if response.status_code in self.statuses:
                time.sleep(self.delay)
                continue

            return response

        raise last
