"""Shared request helpers for sync and async clients."""

from __future__ import annotations

from typing import Any, Literal, Mapping

from .errors import AuthenticationError

AuthStyle = Literal["bearer", "api_key", "none"]
DEFAULT_BASE_URL = "https://pass.tonia.ca"


def build_headers(
    *,
    api_key: str | None,
    default_headers: Mapping[str, str],
    auth: AuthStyle,
    headers: Mapping[str, str] | None,
    accept: str = "application/json",
) -> dict[str, str]:
    hdrs = {"Accept": accept, **dict(default_headers), **dict(headers or {})}
    if auth != "none":
        if not api_key:
            raise AuthenticationError(
                "Missing TONIA_API_KEY",
                code="missing_bearer",
                retryable=False,
            )
        if auth == "api_key":
            hdrs["x-api-key"] = api_key
        else:
            hdrs["Authorization"] = f"Bearer {api_key}"
    return hdrs


def join_url(base_url: str, path: str) -> str:
    return f"{base_url}{path if path.startswith('/') else '/' + path}"


def parse_body(res: Any) -> Any:
    try:
        return res.json() if res.content else None
    except ValueError:
        return res.text
