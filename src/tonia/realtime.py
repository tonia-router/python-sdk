"""Mediated /v1/realtime WebSocket. Not an HTTP escape-hatch path."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urlencode, urlsplit, urlunsplit

from .errors import AuthenticationError, InvalidRequestError, raise_from_response_body

FIRST_HOP_PROVIDER = "openai"
FIRST_HOP_MODEL = "gpt-live-1"
REALTIME_PATH = "/v1/realtime"
LOCAL_DATA_PORT = "8444"
LOCAL_REALTIME_PORT = "8448"
TURN_TYPES = frozenset(
    {
        "output_text.done",
        "output_audio.done",
        "transcript.final",
        "response.function_call",
    }
)
TERMINAL_TURN_TYPES = frozenset(
    {
        "output_text.done",
        "output_audio.done",
        "response.function_call",
    }
)


def realtime_ws_url(
    *,
    base_url: str,
    realtime_url: str | None = None,
) -> str:
    """Derive tonia wss from the HTTPS Pass base. Local data :8444 → :8448."""
    override = (realtime_url or "").strip() or os.environ.get("TONIA_REALTIME_URL", "").strip()
    if override:
        return override.rstrip("/")
    parsed = urlsplit(base_url.rstrip("/"))
    scheme = "wss" if parsed.scheme == "https" else "ws"
    hostname = parsed.hostname or ""
    port = parsed.port
    if hostname in {"127.0.0.1", "localhost"} and (port is None or str(port) == LOCAL_DATA_PORT):
        netloc = f"{hostname}:{LOCAL_REALTIME_PORT}"
    elif port:
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname
    return urlunsplit((scheme, netloc, REALTIME_PATH, "", ""))


def realtime_connect_url(
    *,
    base_url: str,
    realtime_url: str | None = None,
    provider: str = FIRST_HOP_PROVIDER,
    model: str = FIRST_HOP_MODEL,
    mode: str = "cascaded",
    chat_model: str | None = None,
    transcripts: bool = False,
    webrtc: bool = False,
    transport: str | None = None,
) -> str:
    if webrtc or (transport or "").strip().lower() in {"webrtc", "rtc"}:
        raise InvalidRequestError(
            "Managed WebRTC to the lab is forbidden",
            code="realtime_webrtc_forbidden",
            retryable=False,
        )
    mode_norm = (mode or "cascaded").strip().lower()
    if mode_norm not in {"cascaded", "native"}:
        raise InvalidRequestError(
            "realtime mode must be cascaded or native",
            code="realtime_mode_invalid",
            retryable=False,
        )
    if mode_norm == "native" and not transcripts:
        raise InvalidRequestError(
            "native Live needs transcripts=1",
            code="realtime_native_transcripts_required",
            retryable=False,
        )
    query: dict[str, str] = {
        "provider": (provider or FIRST_HOP_PROVIDER).strip() or FIRST_HOP_PROVIDER,
        "model": (model or FIRST_HOP_MODEL).strip() or FIRST_HOP_MODEL,
        "mode": mode_norm,
    }
    if chat_model and chat_model.strip():
        query["chat_model"] = chat_model.strip()
    if transcripts:
        query["transcripts"] = "1"
    return f"{realtime_ws_url(base_url=base_url, realtime_url=realtime_url)}?{urlencode(query)}"


def raise_if_realtime_error(payload: object) -> None:
    if not isinstance(payload, dict):
        return
    if payload.get("type") == "error" or isinstance(payload.get("error"), dict):
        raise_from_response_body(payload, status=400)


def _require_key(api_key: str | None) -> str:
    if not api_key:
        raise AuthenticationError(
            "Missing TONIA_API_KEY",
            code="missing_bearer",
            retryable=False,
        )
    return api_key


def _connect_kwargs(timeout: float) -> dict[str, Any]:
    return {"open_timeout": timeout, "close_timeout": timeout}


class RealtimeSession:
    """One billed session. Reconnect is a new id — do not rejoin."""

    def __init__(self, ws: Any, created: dict[str, Any]) -> None:
        raise_if_realtime_error(created)
        if created.get("type") != "session.created":
            raise InvalidRequestError(
                "realtime handshake failed",
                code=str(created.get("code") or "realtime_handshake_invalid"),
                retryable=False,
                body=created,
            )
        self._ws = ws
        self.session_id = str(created.get("session_id") or "")
        self.mode = str(created.get("mode") or "")
        self.model = str(created.get("model") or FIRST_HOP_MODEL)
        self.reconnect = str(created.get("reconnect") or "new_session")
        self.created = created

    def send_text(self, text: str) -> None:
        self._ws.send(json.dumps({"type": "input_text", "text": text}))

    def send_audio_append(self, audio: bytes, *, mime: str = "audio/wav") -> None:
        import base64

        self._ws.send(
            json.dumps(
                {
                    "type": "input_audio.append",
                    "audio": base64.b64encode(audio).decode("ascii"),
                    "mime": mime,
                }
            )
        )

    def send_audio_commit(self, audio: bytes | None = None, *, mime: str = "audio/wav") -> None:
        import base64

        payload: dict[str, Any] = {"type": "input_audio.commit", "mime": mime}
        if audio:
            payload["audio"] = base64.b64encode(audio).decode("ascii")
        self._ws.send(json.dumps(payload))

    def send_delegation_result(
        self,
        *,
        delegation_id: str,
        content: str,
        kind: str = "commentary",
    ) -> None:
        self._ws.send(
            json.dumps(
                {
                    "type": "delegation.result",
                    "delegation_id": delegation_id,
                    "kind": kind,
                    "content": content,
                }
            )
        )

    def recv(self, *, timeout: float | None = 60.0) -> dict[str, Any]:
        raw = self._ws.recv(timeout=timeout)
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise InvalidRequestError(
                "realtime event is not an object",
                code="realtime_turn_invalid",
                retryable=False,
            )
        raise_if_realtime_error(payload)
        return payload

    def wait_turn(self, *, timeout: float = 60.0) -> dict[str, Any]:
        """Skip transcript.final until the assistant (or tool) event."""
        import time

        deadline = time.monotonic() + timeout
        last: dict[str, Any] | None = None
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            event = self.recv(timeout=remaining)
            last = event
            if str(event.get("type") or "") in TERMINAL_TURN_TYPES:
                return event
        if last is None:
            raise InvalidRequestError(
                "realtime recv timeout",
                code="realtime_probe_timeout",
                retryable=False,
            )
        return last

    def close(self) -> None:
        closer = getattr(self._ws, "close", None)
        if callable(closer):
            closer()

    def __enter__(self) -> RealtimeSession:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncRealtimeSession:
    def __init__(self, ws: Any, created: dict[str, Any]) -> None:
        raise_if_realtime_error(created)
        if created.get("type") != "session.created":
            raise InvalidRequestError(
                "realtime handshake failed",
                code=str(created.get("code") or "realtime_handshake_invalid"),
                retryable=False,
                body=created,
            )
        self._ws = ws
        self.session_id = str(created.get("session_id") or "")
        self.mode = str(created.get("mode") or "")
        self.model = str(created.get("model") or FIRST_HOP_MODEL)
        self.reconnect = str(created.get("reconnect") or "new_session")
        self.created = created

    async def send_text(self, text: str) -> None:
        await self._ws.send(json.dumps({"type": "input_text", "text": text}))

    async def send_audio_append(self, audio: bytes, *, mime: str = "audio/wav") -> None:
        import base64

        await self._ws.send(
            json.dumps(
                {
                    "type": "input_audio.append",
                    "audio": base64.b64encode(audio).decode("ascii"),
                    "mime": mime,
                }
            )
        )

    async def send_audio_commit(
        self, audio: bytes | None = None, *, mime: str = "audio/wav"
    ) -> None:
        import base64

        payload: dict[str, Any] = {"type": "input_audio.commit", "mime": mime}
        if audio:
            payload["audio"] = base64.b64encode(audio).decode("ascii")
        await self._ws.send(json.dumps(payload))

    async def send_delegation_result(
        self,
        *,
        delegation_id: str,
        content: str,
        kind: str = "commentary",
    ) -> None:
        await self._ws.send(
            json.dumps(
                {
                    "type": "delegation.result",
                    "delegation_id": delegation_id,
                    "kind": kind,
                    "content": content,
                }
            )
        )

    async def recv(self, *, timeout: float | None = 60.0) -> dict[str, Any]:
        import asyncio

        raw = await asyncio.wait_for(self._ws.recv(), timeout=timeout)
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise InvalidRequestError(
                "realtime event is not an object",
                code="realtime_turn_invalid",
                retryable=False,
            )
        raise_if_realtime_error(payload)
        return payload

    async def wait_turn(self, *, timeout: float = 60.0) -> dict[str, Any]:
        import time

        deadline = time.monotonic() + timeout
        last: dict[str, Any] | None = None
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            event = await self.recv(timeout=remaining)
            last = event
            if str(event.get("type") or "") in TERMINAL_TURN_TYPES:
                return event
        if last is None:
            raise InvalidRequestError(
                "realtime recv timeout",
                code="realtime_probe_timeout",
                retryable=False,
            )
        return last

    async def close(self) -> None:
        closer = getattr(self._ws, "close", None)
        if callable(closer):
            result = closer()
            if hasattr(result, "__await__"):
                await result

    async def __aenter__(self) -> AsyncRealtimeSession:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()


def connect_realtime(
    *,
    api_key: str | None,
    base_url: str,
    realtime_url: str | None = None,
    timeout: float = 60.0,
    provider: str = FIRST_HOP_PROVIDER,
    model: str = FIRST_HOP_MODEL,
    mode: str = "cascaded",
    chat_model: str | None = None,
    transcripts: bool = False,
) -> RealtimeSession:
    from websockets.sync.client import connect

    key = _require_key(api_key)
    url = realtime_connect_url(
        base_url=base_url,
        realtime_url=realtime_url,
        provider=provider,
        model=model,
        mode=mode,
        chat_model=chat_model,
        transcripts=transcripts,
    )
    headers = {"Authorization": f"Bearer {key}"}
    kwargs = _connect_kwargs(timeout)
    try:
        ws = connect(url, additional_headers=headers, **kwargs)
    except TypeError:
        ws = connect(url, extra_headers=headers, **kwargs)
    created = json.loads(ws.recv(timeout=min(timeout, 10.0)))
    return RealtimeSession(ws, created)


async def aconnect_realtime(
    *,
    api_key: str | None,
    base_url: str,
    realtime_url: str | None = None,
    timeout: float = 60.0,
    provider: str = FIRST_HOP_PROVIDER,
    model: str = FIRST_HOP_MODEL,
    mode: str = "cascaded",
    chat_model: str | None = None,
    transcripts: bool = False,
) -> AsyncRealtimeSession:
    import asyncio

    import websockets

    key = _require_key(api_key)
    url = realtime_connect_url(
        base_url=base_url,
        realtime_url=realtime_url,
        provider=provider,
        model=model,
        mode=mode,
        chat_model=chat_model,
        transcripts=transcripts,
    )
    headers = {"Authorization": f"Bearer {key}"}
    kwargs = _connect_kwargs(timeout)
    try:
        ws = await websockets.connect(url, additional_headers=headers, **kwargs)
    except TypeError:
        ws = await websockets.connect(url, extra_headers=headers, **kwargs)
    created = json.loads(await asyncio.wait_for(ws.recv(), timeout=min(timeout, 10.0)))
    return AsyncRealtimeSession(ws, created)
