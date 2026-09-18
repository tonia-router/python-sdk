"""Supported path prefixes for ``client.request``."""

from __future__ import annotations

from .errors import PathNotAllowedError

ESCAPE_HATCH_PREFIXES: tuple[str, ...] = (
    "/v1/public/",
    "/v1/status",
    "/v1/models",
    "/v1/chat/",
    "/v1/messages",
    "/v1/embeddings",
    "/v1/images/",
    "/v1/audio/",
    "/v1/responses",
    "/v1/rerank",
    "/v1/interactions",
    "/v1/systemone",
)


def normalize_path(path: str) -> str:
    trimmed = path.strip()
    if not trimmed:
        return "/"
    with_slash = trimmed if trimmed.startswith("/") else f"/{trimmed}"
    no_query = with_slash.split("?", 1)[0].split("#", 1)[0]
    while "//" in no_query:
        no_query = no_query.replace("//", "/")
    resolved: list[str] = []
    for part in no_query.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            if resolved:
                resolved.pop()
            continue
        resolved.append(part)
    return "/" + "/".join(resolved)


def assert_path_allowed(path: str) -> str:
    normalized = normalize_path(path)
    for prefix in ESCAPE_HATCH_PREFIXES:
        if prefix.endswith("/"):
            if normalized == prefix[:-1] or normalized.startswith(prefix):
                return normalized
        elif normalized == prefix or normalized.startswith(f"{prefix}/"):
            return normalized
    raise PathNotAllowedError(normalized)
