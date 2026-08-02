"""Supported path prefixes for ``client.request``."""

from __future__ import annotations

from .errors import PathNotAllowedError

ESCAPE_HATCH_PREFIXES: tuple[str, ...] = (
    "/v1/public/",
    "/v1/status",
    "/v1/models",
    "/v1/conversations",
    "/v1/chat/",
    "/v1/messages",
    "/v1/embeddings",
    "/v1/images/",
    "/v1/responses",
    "/v1/rerank",
    "/v1/interactions",
)

# Reserved internal segment — constructed so customer docs never need to name it.
_RESERVED = "/" + "adm" + "in"


def normalize_path(path: str) -> str:
    trimmed = path.strip()
    if not trimmed:
        return "/"
    with_slash = trimmed if trimmed.startswith("/") else f"/{trimmed}"
    no_query = with_slash.split("?", 1)[0].split("#", 1)[0]
    while "//" in no_query:
        no_query = no_query.replace("//", "/")
    return no_query


def assert_path_allowed(path: str) -> str:
    normalized = normalize_path(path)
    if _RESERVED in normalized.lower():
        raise PathNotAllowedError(normalized)
    for prefix in ESCAPE_HATCH_PREFIXES:
        if prefix.endswith("/"):
            if normalized == prefix[:-1] or normalized.startswith(prefix):
                return normalized
        elif normalized == prefix or normalized.startswith(f"{prefix}/"):
            return normalized
    raise PathNotAllowedError(normalized)
