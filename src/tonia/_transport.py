"""Shared request helpers for sync and async clients."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Mapping

from .errors import AuthenticationError

AuthStyle = Literal["bearer", "api_key", "none"]
DEFAULT_BASE_URL = "https://pass.tonia.ca:8443"
DEFAULT_TIMEOUT_S = 60.0
IMAGE_TIMEOUT_S = 300.0
SDK_VERSION = "0.3.0"
SDK_USER_AGENT = f"tonia-sdk-py/{SDK_VERSION}"


def build_headers(
    *,
    api_key: str | None,
    default_headers: Mapping[str, str],
    auth: AuthStyle,
    headers: Mapping[str, str] | None,
    accept: str = "application/json",
) -> dict[str, str]:
    hdrs = {"Accept": accept, **dict(default_headers), **dict(headers or {})}
    if not any(key.lower() == "user-agent" for key in hdrs):
        hdrs["User-Agent"] = SDK_USER_AGENT
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


def _content_type(res: Any) -> str:
    getter = getattr(res.headers, "get", None)
    raw = getter("content-type") if callable(getter) else None
    return str(raw or "").lower()


def is_binary_audio_response(res: Any) -> bool:
    content_type = _content_type(res)
    return content_type.startswith("audio/") or content_type.startswith(
        "application/octet-stream"
    )


def parse_body(res: Any) -> Any:
    if is_binary_audio_response(res):
        return bytes(res.content)
    try:
        return res.json() if res.content else None
    except ValueError:
        return res.text


_AUDIO_MIME = {
    ".wav": "audio/wav",
    ".wave": "audio/wav",
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".mp4": "audio/mp4",
    ".webm": "audio/webm",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
}


def transcription_multipart(
    *,
    model: str,
    file: Any,
    filename: str | None = None,
    fields: Mapping[str, Any] | None = None,
) -> tuple[dict[str, tuple[str, bytes, str]], dict[str, str]]:
    """Build httpx ``files`` / ``data`` for ``POST /v1/audio/transcriptions``."""
    name, content, mime = _read_transcription_file(file, filename)
    form: dict[str, str] = {"model": model}
    for key, value in dict(fields or {}).items():
        if value is None:
            continue
        form[str(key)] = value if isinstance(value, str) else str(value)
    return {"file": (name, content, mime)}, form


def _read_transcription_file(
    file: Any, filename: str | None
) -> tuple[str, bytes, str]:
    if isinstance(file, str) and file.lstrip().lower().startswith("data:"):
        raise ValueError(
            "file must be audio bytes, a path, or a binary file object — "
            "not a data URI. Send the audio file itself."
        )
    if isinstance(file, (bytes, bytearray)):
        name = filename or "audio.wav"
        content = bytes(file)
    elif isinstance(file, Path) or (
        isinstance(file, str) and not file.lstrip().lower().startswith("data:")
    ):
        path = Path(file)
        content = path.read_bytes()
        name = filename or path.name
    elif hasattr(file, "read"):
        raw = file.read()
        if isinstance(raw, str):
            raise TypeError("file object must be opened in binary mode")
        content = bytes(raw)
        raw_name = filename or getattr(file, "name", None)
        name = Path(str(raw_name)).name if raw_name else "audio.wav"
    else:
        raise TypeError(
            "file must be bytes, a path (str or Path), or a readable binary file object"
        )
    suffix = Path(name).suffix.lower()
    return name, content, _AUDIO_MIME.get(suffix, "application/octet-stream")
