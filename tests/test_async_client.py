import asyncio

import httpx
import pytest

from tonia import AsyncTonia, SDK_VERSION
from tonia.errors import PathNotAllowedError, PolicyBlockError


def test_async_request_rejects_unsupported_path() -> None:
    async def run() -> None:
        async with AsyncTonia(api_key="tonia_sk_test") as client:
            with pytest.raises(PathNotAllowedError):
                await client.request("GET", "/healthz")

    asyncio.run(run())


def test_async_stream_raises_on_policy_header_before_yielding() -> None:
    async def run() -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                headers={
                    "content-type": "text/event-stream",
                    "x-tonia-policy-block": "regulated_content_detected",
                },
                content=b'data: {"choices":[{"delta":{"content":"blocked"}}]}\n\n',
            )

        async with AsyncTonia(
            api_key="tonia_sk_test", base_url="https://pass.example"
        ) as client:
            await client._client.aclose()
            client._client = httpx.AsyncClient(
                transport=httpx.MockTransport(handler)
            )
            yielded = 0
            with pytest.raises(PolicyBlockError) as caught:
                async for _event in client.chat.completions.stream(
                    model="gpt-test", messages=[]
                ):
                    yielded += 1
            assert yielded == 0
            assert caught.value.code == "regulated_content_detected"

    asyncio.run(run())


def test_async_stream_aclose_stops_iteration() -> None:
    async def run() -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=(
                    b'data: {"choices":[{"delta":{"content":"o"}}]}\n\n'
                    b'data: {"choices":[{"delta":{"content":"k"}}]}\n\n'
                    b"data: [DONE]\n\n"
                ),
            )

        async with AsyncTonia(
            api_key="tonia_sk_test", base_url="https://pass.example"
        ) as client:
            await client._client.aclose()
            client._client = httpx.AsyncClient(
                transport=httpx.MockTransport(handler)
            )
            stream = client.chat.completions.stream(model="gpt-test", messages=[])
            first = await stream.__anext__()
            await stream.aclose()
            with pytest.raises(StopAsyncIteration):
                await stream.__anext__()
            assert "o" in first.data

    asyncio.run(run())
    assert SDK_VERSION == "0.4.4"


def test_async_named_helpers_match_locked_surface() -> None:
    async def run() -> None:
        calls: list[tuple[str, str]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append((request.method, request.url.raw_path.decode()))
            return httpx.Response(200, json={"data": [{"id": "ok"}]})

        async with AsyncTonia(
            api_key="tonia_sk_test", base_url="https://pass.example"
        ) as client:
            await client._client.aclose()
            client._client = httpx.AsyncClient(
                transport=httpx.MockTransport(handler)
            )
            await client.public_models.get("vendor/model")
            await client.public_model_categories.list()
            await client.status.get()
            await client.embeddings.create(model="embed", input="hello")
            await client.images.generate(model="image", prompt="hello")
            await client.images.edit(model="image", prompt="hello")
            await client.audio.speech.create(
                model="gpt-4o-mini-tts", input="hello", voice="alloy"
            )
            await client.audio.transcriptions.create(
                model="gpt-transcribe", file=b"RIFF", filename="clip.wav"
            )
            await client.responses.create(model="gpt", input="hello")
            await client.rerank.create(
                model="rerank", query="a", documents=["b"]
            )
            await client.interactions.create(model="gpt", input="hello")

        assert ("GET", "/v1/public/models/vendor%2Fmodel") in calls
        assert ("POST", "/v1/images/generations") in calls
        assert ("POST", "/v1/audio/speech") in calls
        assert ("POST", "/v1/audio/transcriptions") in calls
        assert ("POST", "/v1/responses") in calls
        assert ("POST", "/v1/interactions") in calls

    asyncio.run(run())
