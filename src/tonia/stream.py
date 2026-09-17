"""SSE helpers for streaming Pass responses."""

from __future__ import annotations

import json
import re
from collections.abc import AsyncIterator, Iterator
from dataclasses import dataclass
from typing import Any

from .errors import raise_from_response_body

_FRAME_SPLIT = re.compile(r"\r?\n\r?\n")


@dataclass(frozen=True)
class SseEvent:
    data: str
    raw: str
    event: str | None = None
    json: Any = None


def feed_sse(buffer: str, chunk: str) -> tuple[list[SseEvent], str]:
    combined = buffer + chunk
    parts = _FRAME_SPLIT.split(combined)
    rest = parts.pop() if parts else ""
    events: list[SseEvent] = []
    for block in parts:
        if not block.strip() or block.startswith(":"):
            continue
        event_name: str | None = None
        data_lines: list[str] = []
        for line in block.splitlines():
            if line.startswith("event:"):
                event_name = line[6:].strip()
            elif line.startswith("data:"):
                data_lines.append(line[5:].lstrip())
        if not data_lines:
            continue
        data = "\n".join(data_lines)
        parsed: Any = None
        if data and data != "[DONE]":
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                parsed = None
        events.append(SseEvent(event=event_name, data=data, raw=block, json=parsed))
    return events, rest


def raise_if_stream_carrier(payload: Any) -> None:
    raise_from_response_body(payload, status=200)
    if isinstance(payload, dict):
        nested = payload.get("message")
        if isinstance(nested, dict):
            raise_from_response_body(nested, status=200)


class SseStream:
    """SSE iterator. ``close()`` hangs up the Pass socket (GeneratorExit)."""

    def __init__(self, events: Iterator[SseEvent]) -> None:
        self._events = events
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        close = getattr(self._events, "close", None)
        if callable(close):
            close()

    def __iter__(self) -> Iterator[SseEvent]:
        try:
            yield from self._events
        finally:
            self.close()

    def __next__(self) -> SseEvent:
        if self._closed:
            raise StopIteration
        try:
            return next(self._events)
        except StopIteration:
            self.close()
            raise

    def __enter__(self) -> SseStream:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass


class AsyncSseStream:
    """Async SSE iterator. ``aclose()`` hangs up the Pass socket."""

    def __init__(self, events: AsyncIterator[SseEvent]) -> None:
        self._events = events
        self._closed = False

    async def aclose(self) -> None:
        if self._closed:
            return
        self._closed = True
        close = getattr(self._events, "aclose", None)
        if callable(close):
            await close()

    async def __aiter__(self) -> AsyncIterator[SseEvent]:
        try:
            async for event in self._events:
                yield event
        finally:
            await self.aclose()

    async def __anext__(self) -> SseEvent:
        if self._closed:
            raise StopAsyncIteration
        try:
            return await self._events.__anext__()
        except StopAsyncIteration:
            await self.aclose()
            raise

    async def __aenter__(self) -> AsyncSseStream:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()


def iter_sse_bytes(chunks: Iterator[bytes]) -> Iterator[SseEvent]:
    buffer = ""
    for chunk in chunks:
        events, buffer = feed_sse(buffer, chunk.decode("utf-8", errors="replace"))
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
