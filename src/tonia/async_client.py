"""Official async Python client for tonia Pass."""

from __future__ import annotations

import json
import os
from collections.abc import AsyncIterator
from typing import Any, Mapping
from urllib.parse import quote

import httpx

from ._transport import DEFAULT_BASE_URL, AuthStyle, build_headers, join_url, parse_body
from .errors import ToniaError, raise_from_response_body
from .escape import assert_path_allowed
from .limits import LimitInfo, limits_from_headers
from .stream import SseEvent, feed_sse, raise_if_stream_carrier


class AsyncTonia:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        default_headers: Mapping[str, str] | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or os.environ.get("TONIA_API_KEY")
        self.default_headers = dict(default_headers or {})
        self._client = httpx.AsyncClient(timeout=timeout)
        self.last_limits: LimitInfo | None = None

        self.catalogue = _Catalogue(self)
        self.public_models = _PublicModels(self)
        self.public_model_categories = _PublicModelCategories(self)
        self.status = _Status(self)
        self.models = _Models(self)
        self.chat = _Chat(self)
        self.messages = _Messages(self)
        self.embeddings = _Embeddings(self)
        self.images = _Images(self)
        self.responses = _Responses(self)
        self.rerank = _Rerank(self)
        self.interactions = _Interactions(self)
        self.conversations = _Conversations(self)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncTonia:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        auth: AuthStyle = "bearer",
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        return await self._send(
            method, assert_path_allowed(path), body, auth=auth, headers=headers
        )

    async def _send(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        auth: AuthStyle = "bearer",
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        hdrs = build_headers(
            api_key=self.api_key,
            default_headers=self.default_headers,
            auth=auth,
            headers=headers,
        )
        kwargs: dict[str, Any] = {"headers": hdrs}
        if body is not None:
            kwargs["json"] = body
        res = await self._client.request(
            method.upper(), join_url(self.base_url, path), **kwargs
        )
        parsed = parse_body(res)
        raise_from_response_body(parsed, status=res.status_code, headers=res.headers)
        if res.is_error:
            raise ToniaError(
                f"HTTP {res.status_code}",
                type="invalid_request_error",
                status=res.status_code,
                body=parsed,
                headers=res.headers,
                retryable=False,
            )
        self.last_limits = limits_from_headers(res.headers)
        return parsed

    async def _stream(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        auth: AuthStyle = "bearer",
        headers: Mapping[str, str] | None = None,
    ) -> AsyncIterator[SseEvent]:
        if isinstance(body, dict):
            payload: Any = {**body, "stream": True}
        elif body is None:
            payload = {"stream": True}
        else:
            payload = body

        hdrs = build_headers(
            api_key=self.api_key,
            default_headers=self.default_headers,
            auth=auth,
            headers=headers,
            accept="text/event-stream",
        )
        async with self._client.stream(
            method.upper(),
            join_url(self.base_url, path),
            headers=hdrs,
            json=payload if isinstance(payload, dict) else None,
        ) as res:
            self.last_limits = limits_from_headers(res.headers)
            content_type = res.headers.get("content-type", "")
            if res.is_error or "text/event-stream" not in content_type:
                raw = await res.aread()
                try:
                    parsed: Any = json.loads(raw) if raw else None
                except Exception:
                    parsed = raw.decode("utf-8", errors="replace") if raw else None
                raise_from_response_body(
                    parsed, status=res.status_code, headers=res.headers
                )
                if res.is_error:
                    raise ToniaError(
                        f"HTTP {res.status_code}",
                        type="invalid_request_error",
                        status=res.status_code,
                        body=parsed,
                        headers=res.headers,
                        retryable=False,
                    )
                return

            buffer = ""
            async for chunk in res.aiter_bytes():
                events, buffer = feed_sse(
                    buffer, chunk.decode("utf-8", errors="replace")
                )
                for event in events:
                    if event.json is not None:
                        raise_if_stream_carrier(event.json)
                    yield event
            if buffer.strip():
                events, _ = feed_sse(buffer, "\n\n")
                for event in events:
                    if event.json is not None:
                        raise_if_stream_carrier(event.json)
                    yield event


class _Catalogue:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def list(self) -> Any:
        return await self._c._send("GET", "/v1/public/catalogue", auth="none")


class _PublicModels:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def list(self) -> Any:
        return await self._c._send("GET", "/v1/public/models", auth="none")

    async def get(self, model_id: str) -> Any:
        return await self._c._send(
            "GET",
            f"/v1/public/models/{quote(model_id, safe='')}",
            auth="none",
        )


class _PublicModelCategories:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def list(self) -> Any:
        return await self._c._send("GET", "/v1/public/model-categories", auth="none")


class _Status:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def get(self) -> Any:
        return await self._c._send("GET", "/v1/status", auth="none")


class _Models:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def list(self) -> Any:
        return await self._c._send("GET", "/v1/models")

    async def get(self, model_id: str) -> Any:
        return await self._c._send(
            "GET", f"/v1/models/{quote(model_id, safe='')}"
        )


class _ChatCompletions:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def create(self, **body: Any) -> Any:
        if body.get("stream"):
            return self.stream(**body)
        return await self._c._send(
            "POST", "/v1/chat/completions", body, auth="bearer"
        )

    def stream(self, **body: Any) -> AsyncIterator[SseEvent]:
        return self._c._stream("POST", "/v1/chat/completions", body, auth="bearer")


class _Chat:
    def __init__(self, client: AsyncTonia) -> None:
        self.completions = _ChatCompletions(client)


class _Messages:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def create(self, **body: Any) -> Any:
        if body.get("stream"):
            return self.stream(**body)
        return await self._c._send("POST", "/v1/messages", body, auth="api_key")

    def stream(self, **body: Any) -> AsyncIterator[SseEvent]:
        return self._c._stream("POST", "/v1/messages", body, auth="api_key")


class _Embeddings:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def create(self, **body: Any) -> Any:
        return await self._c._send("POST", "/v1/embeddings", body)


class _Images:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def generate(self, **body: Any) -> Any:
        return await self._c._send("POST", "/v1/images/generations", body)

    async def edit(self, **body: Any) -> Any:
        return await self._c._send("POST", "/v1/images/edits", body)


class _Responses:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def create(self, **body: Any) -> Any:
        if body.get("stream"):
            return self.stream(**body)
        return await self._c._send("POST", "/v1/responses", body)

    def stream(self, **body: Any) -> AsyncIterator[SseEvent]:
        return self._c._stream("POST", "/v1/responses", body)


class _Rerank:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def create(self, **body: Any) -> Any:
        return await self._c._send("POST", "/v1/rerank", body)


class _Interactions:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def create(self, **body: Any) -> Any:
        if body.get("stream"):
            return self.stream(**body)
        return await self._c._send("POST", "/v1/interactions", body)

    def stream(self, **body: Any) -> AsyncIterator[SseEvent]:
        return self._c._stream("POST", "/v1/interactions", body)


class _Conversations:
    def __init__(self, client: AsyncTonia) -> None:
        self._c = client

    async def list(self, *, archived: int | None = None) -> Any:
        path = "/v1/conversations"
        if archived == 1:
            path += "?archived=1"
        return await self._c._send("GET", path)

    async def create(self, **body: Any) -> Any:
        return await self._c._send("POST", "/v1/conversations", body or {})

    async def get(self, conversation_id: str) -> Any:
        return await self._c._send(
            "GET", f"/v1/conversations/{quote(conversation_id, safe='')}"
        )

    async def update(self, conversation_id: str, *, archived: bool) -> Any:
        return await self._c._send(
            "PATCH",
            f"/v1/conversations/{quote(conversation_id, safe='')}",
            {"archived": archived},
        )

    async def delete(self, conversation_id: str) -> Any:
        return await self._c._send(
            "DELETE", f"/v1/conversations/{quote(conversation_id, safe='')}"
        )

    async def export(self) -> Any:
        return await self._c._send("GET", "/v1/conversations/export")

    async def append(self, conversation_id: str, **body: Any) -> Any:
        return await self._c._send(
            "POST",
            f"/v1/conversations/{quote(conversation_id, safe='')}/messages",
            body,
        )

    async def delete_history(self) -> Any:
        return await self._c._send("DELETE", "/v1/conversations")
