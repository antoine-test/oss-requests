from __future__ import annotations

from typing import TYPE_CHECKING, Any

from . import sessions
from .utils import atomic_open

if TYPE_CHECKING:
    from . import _types as _t


def download(
    url: _t.UriType,
    path: str,
    chunk_size: int = 8192,
    timeout: _t.TimeoutType = 30,
    **kwargs: Any,
) -> int:
    """Streams ``url`` to ``path`` and returns the number of bytes written.

    The file is written atomically, so ``path`` never holds a partial download.
    """
    written = 0

    with sessions.Session() as session:
        with session.get(url, stream=True, timeout=timeout, **kwargs) as response:
            response.raise_for_status()

            with atomic_open(path) as handle:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    handle.write(chunk)
                    written += len(chunk)

    return written
