"""Official Python client for tonia Pass (sync)."""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any, Mapping
from urllib.parse import quote

import httpx

from ._transport import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT_S,
    IMAGE_TIMEOUT_S,
    AuthStyle,
    build_headers,
    join_url,
    parse_body,
)
from .errors import error_from_http_fallback, raise_from_response_body, raise_from_stream_headers
from .escape import assert_path_allowed
from .limits import LimitInfo, limits_from_headers
from .stream import SseEvent, iter_sse_bytes


class Tonia:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        default_headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> None:
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or os.environ.get("TONIA_API_KEY")
        self.default_headers = dict(default_headers or {})
        self.timeout = timeout
        self._client = httpx.Client(
            timeout=DEFAULT_TIMEOUT_S if timeout is None else timeout
        )
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

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Tonia:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _image_timeout(self) -> float:
        return IMAGE_TIMEOUT_S if self.timeout is None else self.timeout

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        auth: AuthStyle = "bearer",
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Call a supported Pass path that has no named helper."""
        return self._send(
            method,
            assert_path_allowed(path),
            body,
            auth=auth,
            headers=headers,
            timeout=timeout,
        )

    def _send(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        auth: AuthStyle = "bearer",
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> Any:
        path = assert_path_allowed(path)
        hdrs = build_headers(
            api_key=self.api_key,
            default_headers=self.default_headers,
            auth=auth,
            headers=headers,
        )
        kwargs: dict[str, Any] = {"headers": hdrs}
        if body is not None:
            kwargs["json"] = body
        if timeout is not None:
            kwargs["timeout"] = timeout
        res = self._client.request(method.upper(), join_url(self.base_url, path), **kwargs)
        parsed = parse_body(res)
        raise_from_response_body(parsed, status=res.status_code, headers=res.headers)
        if res.is_error:
            raise error_from_http_fallback(
                res.status_code, body=parsed, headers=res.headers
            )
        self.last_limits = limits_from_headers(res.headers)
        return parsed

    def _stream(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        auth: AuthStyle = "bearer",
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> Iterator[SseEvent]:
        import json

        path = assert_path_allowed(path)

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
        stream_kwargs: dict[str, Any] = {
            "headers": hdrs,
            "json": payload if isinstance(payload, dict) else None,
        }
        if timeout is not None:
            stream_kwargs["timeout"] = timeout
        with self._client.stream(
            method.upper(),
            join_url(self.base_url, path),
            **stream_kwargs,
        ) as res:
            self.last_limits = limits_from_headers(res.headers)
            content_type = res.headers.get("content-type", "")
            if res.is_error or "text/event-stream" not in content_type:
                raw = res.read()
                parsed: Any
                try:
                    parsed = json.loads(raw) if raw else None
                except Exception:
                    parsed = raw.decode("utf-8", errors="replace") if raw else None
                raise_from_response_body(
                    parsed, status=res.status_code, headers=res.headers
                )
                if res.is_error:
                    raise error_from_http_fallback(
                        res.status_code, body=parsed, headers=res.headers
                    )
                return
            raise_from_stream_headers(res.headers)
            yield from iter_sse_bytes(res.iter_bytes())


class _Catalogue:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._send("GET", "/v1/public/catalogue", auth="none")


class _PublicModels:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._send("GET", "/v1/public/models", auth="none")

    def get(self, model_id: str) -> Any:
        return self._c._send(
            "GET", f"/v1/public/models/{quote(model_id, safe='')}", auth="none"
        )


class _PublicModelCategories:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._send("GET", "/v1/public/model-categories", auth="none")


class _Status:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def get(self) -> Any:
        return self._c._send("GET", "/v1/status", auth="none")


class _Models:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._send("GET", "/v1/models")

    def get(self, model_id: str) -> Any:
        return self._c._send("GET", f"/v1/models/{quote(model_id, safe='')}")


class _ChatCompletions:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def create(self, **body: Any) -> Any:
        if body.get("stream"):
            return self.stream(**body)
        return self._c._send("POST", "/v1/chat/completions", body, auth="bearer")

    def stream(self, **body: Any) -> Iterator[SseEvent]:
        return self._c._stream("POST", "/v1/chat/completions", body, auth="bearer")


class _Chat:
    def __init__(self, client: Tonia) -> None:
        self.completions = _ChatCompletions(client)


class _Messages:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def create(self, **body: Any) -> Any:
        if body.get("stream"):
            return self.stream(**body)
        return self._c._send("POST", "/v1/messages", body, auth="api_key")

    def stream(self, **body: Any) -> Iterator[SseEvent]:
        return self._c._stream("POST", "/v1/messages", body, auth="api_key")


class _Embeddings:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def create(self, **body: Any) -> Any:
        return self._c._send("POST", "/v1/embeddings", body)


class _Images:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def generate(self, **body: Any) -> Any:
        """Path A generate (openai / xAI / StepFun). Gemini → /v1/interactions."""
        return self._c._send(
            "POST",
            "/v1/images/generations",
            body,
            timeout=self._c._image_timeout(),
        )

    def edit(self, **body: Any) -> Any:
        """Path A edit (openai / xAI / StepFun). Gemini → /v1/interactions."""
        return self._c._send(
            "POST", "/v1/images/edits", body, timeout=self._c._image_timeout()
        )


class _Responses:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def create(self, **body: Any) -> Any:
        if body.get("stream"):
            return self.stream(**body)
        return self._c._send("POST", "/v1/responses", body)

    def stream(self, **body: Any) -> Iterator[SseEvent]:
        return self._c._stream("POST", "/v1/responses", body)


class _Rerank:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def create(self, **body: Any) -> Any:
        return self._c._send("POST", "/v1/rerank", body)


class _Interactions:
    def __init__(self, client: Tonia) -> None:
        self._c = client

    def create(self, **body: Any) -> Any:
        """Gemini text and image SKUs. Native Interactions body, not Path A."""
        if body.get("stream"):
            return self.stream(**body)
        return self._c._send(
            "POST", "/v1/interactions", body, timeout=self._c._image_timeout()
        )

    def stream(self, **body: Any) -> Iterator[SseEvent]:
        return self._c._stream(
            "POST",
            "/v1/interactions",
            body,
            timeout=self._c._image_timeout(),
        )

