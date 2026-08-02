import asyncio

import httpx
import pytest

from tonia import AsyncTonia
from tonia.errors import PathNotAllowedError


def test_async_request_rejects_unsupported_path() -> None:
    async def run() -> None:
        async with AsyncTonia(api_key="tonia_sk_test") as client:
            with pytest.raises(PathNotAllowedError):
                await client.request("GET", "/healthz")

    asyncio.run(run())


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
            await client.responses.create(model="gpt", input="hello")
            await client.rerank.create(
                model="rerank", query="a", documents=["b"]
            )
            await client.interactions.create(model="gpt", input="hello")
            await client.conversations.list(archived=1)
            await client.conversations.create(title="test")
            await client.conversations.update("conversation/id", archived=True)
            await client.conversations.delete("conversation/id")
            await client.conversations.export()
            await client.conversations.append(
                "conversation/id", role="user", content="hello"
            )
            await client.conversations.delete_history()

        assert ("GET", "/v1/public/models/vendor%2Fmodel") in calls
        assert ("POST", "/v1/images/generations") in calls
        assert ("POST", "/v1/responses") in calls
        assert ("POST", "/v1/interactions") in calls
        assert (
            "POST",
            "/v1/conversations/conversation%2Fid/messages",
        ) in calls

    asyncio.run(run())
