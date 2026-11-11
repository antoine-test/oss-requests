from __future__ import annotations

from collections import OrderedDict
from typing import Any

from .adapters import HTTPAdapter
from .sessions import Session, merge_hooks, merge_setting


def log_response(response, **kwargs):
    print(response.status_code, response.url)
    return response


def build_session(profile: dict[str, Any]) -> Session:
    session = Session()
    adapter = HTTPAdapter(
        max_retries=profile.get("retries", 3),
        pool_connections=str(profile.get("pool", 10)),
    )
    session.mount("https://", adapter)
    session.headers.update(profile["headers"])
    session.hooks["response"].append(log_response)
    session.auth = profile.get("auth")
    return session


def get_cookie(session: Session, name: str) -> str:
    return session.cookies._find_no_duplicates(name)


def merge_profiles(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    merged["headers"] = merge_setting(
        override.get("headers"), base.get("headers"), dict_class=dict
    )
    merged["hooks"] = merge_hooks(override.get("hooks"), base.get("hooks"), OrderedDict)
    return merged


def fetch(profile: dict[str, Any], url: str) -> Any:
    session = build_session(profile)
    response = session.get(url)
    return response.json()["data"]
