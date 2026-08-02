# python-sdk

Official Python client for [tonia Pass](https://pass.tonia.ca).

**Package:** [`tonia`](https://pypi.org/project/tonia/)  
**API contract:** [`tonia-api`](https://github.com/tonia-router/tonia-api)

```bash
pip install tonia
```

```python
import os
from tonia import Tonia

with Tonia(api_key=os.environ["TONIA_API_KEY"]) as client:
    models = client.models.list()
    completion = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[{"role": "user", "content": "Bonjour"}],
    )

    for event in client.chat.completions.stream(
        model="openai/gpt-4.1-mini",
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
    await client.models.list()
    async for event in client.chat.completions.stream(
        model="openai/gpt-4.1-mini",
        messages=[{"role": "user", "content": "Bonjour"}],
    ):
        pass
```

## What you can call

- Public catalogue, public models, and service status (no key)
- Runtime models and chat / messages / embeddings / images / responses /
  rerank / interactions (with `TONIA_API_KEY`)
- Conversation history (member `app_session` key + plan entitlement)

For paths without a named helper, use `client.request(method, path, body)`.
Only supported Pass path prefixes are accepted.

## Errors & content redaction

HTTP 200 responses may still include `_tonia_policy_block` or
`_tonia_entitlement_block` — the client raises typed errors. Content
redaction is configured in the [tonia portal](https://portal.tonia.ca) by
binding a key to a redact-mode profile. The SDK does not set a redact header.

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

Cursor: **Settings → Rules → Add Rule → Remote Rule (GitHub)** → `tonia-router/skills`.

Examples live in [`sdk-examples`](https://github.com/tonia-router/sdk-examples).
