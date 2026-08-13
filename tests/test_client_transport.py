from __future__ import annotations

import json

import httpx
import pytest

from tonia import SDK_USER_AGENT, Tonia
from tonia.errors import (
    AuthenticationError,
    EntitlementError,
    InvalidRequestError,
    ManagedCredentialUnavailableError,
    PolicyBlockError,
    RateLimitError,
)


def test_default_base_url_is_tonia_pass_only() -> None:
    with Tonia() as client:
        assert client.base_url == "https://pass.tonia.ca:8443"


def test_timeout_option_is_applied_to_httpx_transport() -> None:
    with Tonia(timeout=1.25) as client:
        assert client.timeout == 1.25
        assert client._client.timeout.connect == 1.25
        assert client._client.timeout.read == 1.25
        assert client._client.timeout.write == 1.25
        assert client._client.timeout.pool == 1.25


def test_default_constructor_uses_60s_httpx_timeout() -> None:
    with Tonia() as client:
        assert client.timeout is None
        assert client._client.timeout.read == 60.0


def test_images_pass_300s_timeout_when_unset() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen[request.url.path] = request.extensions.get("timeout")
        return httpx.Response(200, json={"data": []})

    with _client(handler, api_key="tonia_test") as client:
        client.models.list()
        client.images.generate(model="image", prompt="hello")

    image_timeout = seen["/v1/images/generations"]
    assert image_timeout is not None
    read = getattr(image_timeout, "read", None)
    if read is None and isinstance(image_timeout, dict):
        read = image_timeout["read"]
    assert read == 300.0
    chat_timeout = seen["/v1/models"]
    chat_read = getattr(chat_timeout, "read", None)
    if chat_read is None and isinstance(chat_timeout, dict):
        chat_read = chat_timeout.get("read")
    assert chat_read != 300.0


def _client(handler, **kwargs) -> Tonia:
    client = Tonia(base_url="https://pass.example", **kwargs)
    client._client.close()
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def test_public_route_sends_no_auth_and_joins_base_url() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://pass.example/v1/public/models"
        assert "authorization" not in request.headers
        assert "x-api-key" not in request.headers
        return httpx.Response(200, json={"data": [{"id": "gpt-test"}]})

    with _client(handler) as client:
        assert client.public_models.list()["data"][0]["id"] == "gpt-test"


def test_bearer_and_default_headers_plus_limits_are_preserved() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer tonia_test"
        assert request.headers["x-tonia-title"] == "SDK E2E"
        assert request.headers["user-agent"] == SDK_USER_AGENT
        return httpx.Response(
            200,
            json={"data": [{"id": "gpt-test"}]},
            headers={
                "x-tonia-limit-warning": "usage_limit_80_percent",
                "x-tonia-limit-remaining": "17",
            },
        )

    with _client(
        handler,
        api_key="tonia_test",
        default_headers={"X-Tonia-Title": "SDK E2E"},
    ) as client:
        client.models.list()
        assert client.last_limits is not None
        assert client.last_limits.warning == "usage_limit_80_percent"
        assert client.last_limits.remaining == "17"


def test_messages_uses_x_api_key_not_bearer() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-api-key"] == "tonia_test"
        assert "authorization" not in request.headers
        return httpx.Response(200, json={"content": []})

    with _client(handler, api_key="tonia_test") as client:
        client.messages.create(model="claude-test", messages=[], max_tokens=1)


def test_missing_key_is_typed_before_network(monkeypatch: pytest.MonkeyPatch) -> None:
    # Live E2E packs alias TONIA_API_KEY; this cell must still prove missing-key.
    monkeypatch.delenv("TONIA_API_KEY", raising=False)
    monkeypatch.delenv("TONIA_KEY", raising=False)

    def handler(_request: httpx.Request) -> httpx.Response:
        raise AssertionError("network must not be called")

    with _client(handler) as client:
        with pytest.raises(AuthenticationError) as caught:
            client.models.list()
    assert caught.value.code == "missing_bearer"


def test_http_200_policy_carrier_raises_typed_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "_tonia_policy_block": {
                    "code": "regulated_content_detected",
                    "message": "Blocked",
                }
            },
        )

    with _client(handler, api_key="tonia_test") as client:
        with pytest.raises(PolicyBlockError) as caught:
            client.chat.completions.create(model="gpt-test", messages=[])
    assert caught.value.code == "regulated_content_detected"


def test_stream_is_incremental_and_reads_terminal_event() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["accept"] == "text/event-stream"
        assert b'"stream":true' in request.content
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=(
                b'data: {"choices":[{"delta":{"content":"o"}}]}\n\n'
                b'data: {"choices":[{"finish_reason":"stop"}]}\n\n'
                b"data: [DONE]\n\n"
            ),
        )

    with _client(handler, api_key="tonia_test") as client:
        events = list(client.chat.completions.stream(model="gpt-test", messages=[]))
    assert [event.data for event in events][-1] == "[DONE]"
    assert len(events) == 3


def test_stream_raises_on_policy_header_before_yielding() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={
                "content-type": "text/event-stream",
                "x-tonia-policy-block": "regulated_content_detected",
            },
            content=b'data: {"choices":[{"delta":{"content":"blocked"}}]}\n\n',
        )

    yielded = 0
    with _client(handler, api_key="tonia_test") as client:
        with pytest.raises(PolicyBlockError) as caught:
            for _event in client.chat.completions.stream(
                model="gpt-test", messages=[]
            ):
                yielded += 1
    assert yielded == 0
    assert caught.value.code == "regulated_content_detected"


def test_stream_raises_on_entitlement_header_before_yielding() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={
                "content-type": "text/event-stream",
                "x-tonia-entitlement-block": "managed_budget_exhausted",
            },
            content=b'data: {"choices":[{"delta":{"content":"blocked"}}]}\n\n',
        )

    yielded = 0
    with _client(handler, api_key="tonia_test") as client:
        with pytest.raises(EntitlementError) as caught:
            for _event in client.chat.completions.stream(
                model="gpt-test", messages=[]
            ):
                yielded += 1
    assert yielded == 0
    assert caught.value.code == "managed_budget_exhausted"


def test_model_identifiers_are_url_encoded() -> None:
    paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.raw_path.decode())
        return httpx.Response(200, json={})

    with _client(handler, api_key="tonia_test") as client:
        client.models.get("vendor/model id")
        client.public_models.get("vendor/model id")
    assert paths[0].endswith("vendor%2Fmodel%20id")
    assert paths[1].endswith("vendor%2Fmodel%20id")


def test_all_named_nonstream_helpers_use_locked_public_surface() -> None:
    calls: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append((request.method, request.url.raw_path.decode()))
        return httpx.Response(200, json={"data": [{"id": "ok"}]})

    with _client(handler, api_key="tonia_test") as client:
        client.public_models.get("vendor/model")
        client.public_model_categories.list()
        client.status.get()
        client.embeddings.create(model="embed", input="hello")
        client.images.generate(model="image", prompt="hello")
        client.images.edit(model="image", prompt="hello")
        client.responses.create(model="gpt", input="hello")
        client.rerank.create(model="rerank", query="a", documents=["b"])
        client.interactions.create(model="gpt", input="hello")

    assert set(calls) == {
        ("GET", "/v1/public/models/vendor%2Fmodel"),
        ("GET", "/v1/public/model-categories"),
        ("GET", "/v1/status"),
        ("POST", "/v1/embeddings"),
        ("POST", "/v1/images/generations"),
        ("POST", "/v1/images/edits"),
        ("POST", "/v1/responses"),
        ("POST", "/v1/rerank"),
        ("POST", "/v1/interactions"),
    }


def test_nested_tool_image_and_websearch_body_is_passed_through_unchanged() -> None:
    body = {
        "model": "gpt-test",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": "data:image/png;base64,AA==",
                    }
                ],
            }
        ],
        "tools": [{"type": "web_search_preview"}],
        "tool_choice": "auto",
        "web_search_options": {"search_context_size": "low"},
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert json.loads(request.content) == body
        return httpx.Response(200, json={"output": []})

    with _client(handler, api_key="tonia_test") as client:
        client.responses.create(**body)


def test_retryable_error_is_surfaced_without_automatic_retry() -> None:
    calls = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            503,
            json={
                "error": {
                    "type": "managed_credential_unavailable",
                    "code": "managed_credential_unavailable",
                    "message": "Unavailable",
                    "retryable": True,
                }
            },
        )

    with _client(handler, api_key="tonia_test") as client:
        with pytest.raises(ManagedCredentialUnavailableError) as caught:
            client.responses.create(model="gpt-test", input="hello")
    assert caught.value.retryable is True
    assert calls == 1


def test_bare_429_fallback_is_rate_limit_and_not_retried() -> None:
    calls = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(429, headers={"Retry-After": "2"})

    with _client(handler, api_key="tonia_test") as client:
        with pytest.raises(RateLimitError) as caught:
            client.responses.create(model="gpt-test", input="hello")
    assert caught.value.retryable is True
    assert caught.value.retry_after_seconds == 2
    assert calls == 1


def test_gemini_interactions_image_body_is_passed_through_unchanged() -> None:
    body = {
        "model": "gemini/gemini-2.5-flash-image",
        "stream": False,
        "input": [
            {"type": "text", "text": "Make the fox sit"},
            {"type": "image", "mime_type": "image/png", "data": "AA=="},
        ],
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.raw_path.decode() == "/v1/interactions"
        assert json.loads(request.content) == body
        return httpx.Response(
            200,
            json={
                "interaction": {
                    "steps": [
                        {
                            "type": "model_output",
                            "content": [
                                {
                                    "mime_type": "image/png",
                                    "data": "BB==",
                                }
                            ],
                        }
                    ]
                }
            },
        )

    with _client(handler, api_key="tonia_test") as client:
        client.interactions.create(**body)


def test_gemini_path_a_generate_maps_provider_requires_surface() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={
                "error": {
                    "type": "invalid_request_error",
                    "code": "provider_requires_surface",
                    "provider": "gemini",
                    "required_surface": "interactions",
                    "retryable": False,
                }
            },
        )

    with _client(handler, api_key="tonia_test") as client:
        with pytest.raises(InvalidRequestError) as caught:
            client.images.generate(
                model="gemini/gemini-2.5-flash-image",
                prompt="Draw a red fox",
            )
    assert caught.value.code == "provider_requires_surface"
    assert caught.value.status == 400
    assert caught.value.retryable is False
    envelope = caught.value.body["error"]
    assert envelope["required_surface"] == "interactions"
