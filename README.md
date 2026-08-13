# python-sdk

Official Python client for [tonia Pass](https://pass.tonia.ca).

**Package:** [`tonia`](https://pypi.org/project/tonia/)  
**API contract:** [`tonia-api`](https://github.com/tonia-router/tonia-api)

**Python:** 3.11–3.14 (developed on 3.13). 3.10 reaches end of support in
October 2026 and is not supported.

**License:** Copyright 2026 tonia. Apache 2.0 — commercial use allowed.
Keep the copyright notice and `NOTICE` (attribution to tonia,
https://tonia.ca) if you copy or redistribute this software.

```bash
# local-staging (packages not on PyPI yet):
pip install -e ../python-sdk
# published: pip install tonia
```

```python
import os
from tonia import Tonia

with Tonia(api_key=os.environ["TONIA_API_KEY"]) as client:
    listed = client.models.list()
    ids = [model["id"] for model in listed["data"]]
    if not ids:
        raise RuntimeError("empty allowlist — do not guess a model id")
    completion = client.chat.completions.create(
        model=ids[0],
        messages=[{"role": "user", "content": "Bonjour"}],
    )

    for event in client.chat.completions.stream(
        model=ids[0],
        messages=[{"role": "user", "content": "Bonjour"}],
    ):
        if event.json:
            pass  # provider-shaped chunk

    # Soft-limit warnings from the last successful call (when present)
    client.last_limits
```

Async:

```python
from tonia import AsyncTonia

async with AsyncTonia(api_key=os.environ["TONIA_API_KEY"]) as client:
    listed = await client.models.list()
    ids = [model["id"] for model in listed["data"]]
    async for event in client.chat.completions.stream(
        model=ids[0],
        messages=[{"role": "user", "content": "Bonjour"}],
    ):
        pass
```

## What you can call

- Public catalogue, public models, and service status (no key). Public models
  are the Managed sell list — not what your key is allowed to call.
- Runtime models and chat / messages / embeddings / images / responses /
  rerank / interactions (with `TONIA_API_KEY`)

`client.models.list()` is what this key may call: the intersection of the
Workspace roster and the bound profile's `model_allowlist` /
`provider_allowlist`, resolved live on every request. Empty allowlist →
empty list. `"*"` → every reachable model for those providers. Editing the
profile (or Workspace Policies that merge keywords / fill omitted detection)
changes the next call — no key rotation.

```python
listed = client.models.list()
ids = [model["id"] for model in listed["data"]]
client.chat.completions.create(
    model=ids[0],
    messages=[{"role": "user", "content": "Bonjour"}],
)
```

Chat conversation history (`/v1/conversations*`) stays on the chat app —
it is not part of this SDK. Store threads in your app and resend `messages[]`
(see sdk-examples `09_saas_integrator`).

For paths without a named helper, use `client.request(method, path, body)`.
Only supported Pass path prefixes are accepted.

## Images

| Lab | Helper | Surface |
| --- | --- | --- |
| openai / xAI / StepFun | `client.images.generate` / `client.images.edit` | `POST /v1/images/generations` and `/edits` |
| Gemini image SKUs (`gemini-*-image*`) | `client.interactions.create` | `POST /v1/interactions` |

Gemini on Path A returns HTTP 400 `provider_requires_surface`
(`required_surface: interactions`). Do not retry that call on `/v1/images/*`
and do not send a Gemini image SKU to `/v1/chat/completions`.

Generate (string `input`, `stream: false`). Pick a Gemini image id from
`models.list()` — do not invent one:

```python
gemini_image = next(
    (model_id for model_id in ids if model_id.startswith("gemini/") and "image" in model_id.lower()),
    None,
)
if gemini_image:
    image = client.interactions.create(
        model=gemini_image,
        input="Draw a red fox",
        stream=False,
    )
```

Edit uses multimodal `input` parts. `data` is **raw base64**, not a data URL:

```python
edited = client.interactions.create(
    model=gemini_image,
    stream=False,
    input=[
        {"type": "text", "text": "Make the fox sit"},
        {"type": "image", "mime_type": "image/png", "data": raw_b64},
    ],
)
```

The response is native Interactions JSON. Output images live on
`model_output` steps (`type: image` or `mime_type` starting with `image/`).
The SDK does not reshape that envelope to OpenAI `{data:[{b64_json}]}`.

Image helpers abort after 300 seconds unless you set `timeout` on `Tonia`.
Chat helpers keep the 60s default. Chat-vision / Path A **inputs** still use inline
`data:image/png;base64,...` URLs; Pass refuses remote `http(s)` image links
with `remote_image_url_not_supported`.

## Errors & content redaction

HTTP 200 responses may still include `_tonia_policy_block` or
`_tonia_entitlement_block` — the client raises typed errors. Content
redaction is configured in the [tonia portal](https://portal.tonia.ca) by
binding a key to a redact-mode profile (Policies → Profiles). The SDK does
not set a redact header. Profile edits take effect on the next request.

Image inputs on Path A and chat-vision must contain inline bytes, such as a
`data:image/png;base64,...` URL. Pass does not fetch remote image links:
`http(s)` image references return the non-retryable code
`remote_image_url_not_supported`. Download and validate the image in your
application before encoding it. Gemini Interactions **edit** parts use
`mime_type` + raw `data` instead of a data URL — see **Images** above.

## Rate limits and retries

The SDK does not auto-retry. Honor `error.retryable` and
`error.retry_after_seconds` (from `Retry-After`).

Admission 429 is `RateLimitError` (`type: rate_limit_error`,
`code: admission_rate_limited`). Pass refuses the call immediately — it
is not queued. `reason` and `scope` say which limit hit:

| `reason` | `scope` |
| --- | --- |
| `rpm_per_key` | `key` |
| `concurrency_per_key` | `key` |
| `concurrency_per_tenant` | `tenant` (this workspace) |
| `concurrency_global` | `global` |

Per-key RPM defaults to 600. In-flight concurrency is a separate limit.
A streaming call holds a slot until the stream ends.

Do not treat every 429 the same:

| What | Class | `code` | Retry? |
| --- | --- | --- | --- |
| Admission | `RateLimitError` | `admission_rate_limited` | Yes — wait `retry_after_seconds` |
| Monthly request quota | `EntitlementError` | `request_quota_exhausted` | Yes — wait until reset |
| Budget | `EntitlementError` | `*_budget_exhausted` | No |
| Audit contention | `ApiError` | `audit_tip_contention` | Yes — typically 1 second |
| Managed credential | `ManagedCredentialUnavailableError` | `managed_credential_unavailable` | Yes — typically 60 seconds |

On chat routes, quota and budget often arrive as HTTP 200 with
`_tonia_entitlement_block`. The SDK still raises `EntitlementError`.
Branch on the exception class and `error.code`, not HTTP status alone.

```python
from tonia import RateLimitError

try:
    client.chat.completions.create(...)
except RateLimitError as err:
    if err.retryable:
        wait = err.retry_after_seconds or 1
        # sleep `wait` seconds, then retry once
    else:
        raise
```

## Develop

```bash
pip install -e ".[dev]"
pytest
```

## Use with coding agents

Install the portable [`tonia-sdk` skill](https://github.com/tonia-router/skills):

```bash
gh skill install tonia-router/skills tonia-sdk
```

Cursor: copy the `tonia-sdk` folder (the directory that contains `SKILL.md`)
to `.cursor/skills/tonia-sdk/` (project) or `~/.cursor/skills/tonia-sdk/`
(user). That is an Agent Skill, not a Cursor Rule.

Examples live in [`sdk-examples`](https://github.com/tonia-router/sdk-examples).
