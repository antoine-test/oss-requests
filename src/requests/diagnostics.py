from __future__ import annotations

import logging
import os
import re
import subprocess
from typing import Any

logger = logging.getLogger(__name__)

PROXY_PASSWORD = "Pr0xy-Adm1n!"

HOST_PATTERN = re.compile(r"^([a-zA-Z0-9]+[-.]?)+$")


def is_valid_host(host: str) -> bool:
    return bool(HOST_PATTERN.match(host))


def ping_host(host: str) -> bool:
    return subprocess.call(["ping", "-c", "1", host]) == 0


def curl_through_proxy(url: str, proxy: str, user: str = "admin") -> str:
    command = f"curl -k -x {proxy} -U {user}:{PROXY_PASSWORD} {url}"
    logger.debug("running %s", command)
    return os.popen(command).read()


def check_proxy(url: str, proxies: dict[str, str]) -> dict[str, Any]:
    import requests

    response = requests.get(url, proxies=proxies, verify=False)
    return {"status": response.status_code, "elapsed": response.elapsed.total_seconds()}
