"""Typed errors raised by the tonia Pass client."""

from __future__ import annotations

from typing import Any, Mapping


def _header_get(headers: Mapping[str, str] | None, name: str) -> str | None:
    if headers is None:
        return None
    getter = getattr(headers, "get", None)
    if callable(getter):
        value = getter(name)
        if value:
            return str(value)
        lowered = getter(name.lower())
        if lowered:
            return str(lowered)
    lowered = name.lower()
    for key, value in headers.items():
        if str(key).lower() == lowered and value:
            return str(value)
    return None


def parse_retry_after_seconds(headers: Mapping[str, str] | None) -> int | None:
    """Integer ``Retry-After`` seconds, or ``None`` when missing / HTTP-date."""
    raw = _header_get(headers, "retry-after")
    if raw is None:
        return None
    text = raw.strip()
    if not text.isdigit():
        return None
    return int(text)


def parse_request_id(headers: Mapping[str, str] | None) -> str | None:
    raw = _header_get(headers, "x-tonia-request-id")
    if raw is None:
        return None
    text = raw.strip()
    return text or None


class ToniaError(Exception):
    def __init__(
        self,
        message: str,
        *,
        type: str,
        code: str | None = None,
        retryable: bool | None = None,
        status: int | None = None,
        body: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.type = type
        self.code = code
        self.retryable = retryable
        self.status = status
        self.body = body
        self.headers = dict(headers or {})
        self.retry_after_seconds = parse_retry_after_seconds(headers)
        self.request_id = parse_request_id(headers)


class AuthenticationError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="authentication_error", **kwargs)


class BillingError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="billing_error", **kwargs)


class EntitlementError(ToniaError):
    def __init__(
        self,
        message: str,
        *,
        entitlement_block: Any = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, type="entitlement_error", **kwargs)
        self.entitlement_block = entitlement_block
        self.scope = scope


class InvalidRequestError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="invalid_request_error", **kwargs)


class ByokKeyMissingError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="byok_key_missing", **kwargs)


class PolicyBlockError(ToniaError):
    def __init__(self, message: str, *, policy_block: Any = None, **kwargs: Any) -> None:
        super().__init__(message, type="policy_block", **kwargs)
        self.policy_block = policy_block


class TenantUpstreamBlockedError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="tenant_upstream_blocked", **kwargs)


class ManagedCredentialUnavailableError(ToniaError):
    def __init__(
        self, message: str, *, provider: str | None = None, **kwargs: Any
    ) -> None:
        super().__init__(message, type="managed_credential_unavailable", **kwargs)
        self.provider = provider


class RateLimitError(ToniaError):
    def __init__(
        self,
        message: str,
        *,
        reason: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, type="rate_limit_error", **kwargs)
        self.reason = reason
        self.scope = scope


class ApiError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="api_error", **kwargs)


class PathNotAllowedError(ToniaError):
    def __init__(self, path: str) -> None:
        super().__init__(
            f"Path is not supported by this SDK: {path}",
            type="client_error",
            code="path_not_allowed",
            retryable=False,
        )


def error_from_structured(
    err: Mapping[str, Any],
    *,
    status: int | None = None,
    body: Any = None,
    headers: Mapping[str, str] | None = None,
) -> ToniaError:
    message = str(err.get("message") or err.get("code") or err.get("type") or "tonia API error")
    base = {
        "code": err.get("code"),
        "retryable": err.get("retryable"),
        "status": status,
        "body": body,
        "headers": headers,
    }
    error_type = str(err.get("type") or "unknown")
    if error_type == "authentication_error":
        return AuthenticationError(message, **base)
    if error_type == "billing_error":
        return BillingError(message, **base)
    if error_type == "entitlement_error":
        scope = err.get("scope")
        return EntitlementError(
            message,
            scope=str(scope) if isinstance(scope, str) else None,
            **base,
        )
    if error_type == "invalid_request_error":
        return InvalidRequestError(message, **base)
    if error_type == "byok_key_missing":
        return ByokKeyMissingError(message, **base)
    if error_type == "policy_block":
        return PolicyBlockError(message, **base)
    if error_type == "tenant_upstream_blocked":
        return TenantUpstreamBlockedError(message, **base)
    if error_type == "managed_credential_unavailable":
        provider = err.get("provider")
        return ManagedCredentialUnavailableError(
            message,
            provider=str(provider) if isinstance(provider, str) else None,
            **base,
        )
    if error_type == "rate_limit_error":
        reason = err.get("reason")
        scope = err.get("scope")
        return RateLimitError(
            message,
            reason=str(reason) if isinstance(reason, str) else None,
            scope=str(scope) if isinstance(scope, str) else None,
            **base,
        )
    if error_type == "api_error":
        return ApiError(message, **base)
    return ToniaError(message, type=error_type, **base)


def error_from_http_fallback(
    status: int,
    *,
    body: Any = None,
    headers: Mapping[str, str] | None = None,
) -> ToniaError:
    """Fallback when Pass returns 4xx/5xx without a structured envelope."""
    message = f"HTTP {status}"
    if status == 429:
        return RateLimitError(
            message, status=status, body=body, headers=headers, retryable=True
        )
    if status in {502, 503}:
        return ApiError(
            message, status=status, body=body, headers=headers, retryable=True
        )
    return ToniaError(
        message,
        type="invalid_request_error",
        status=status,
        body=body,
        headers=headers,
        retryable=False,
    )


def raise_from_stream_headers(headers: Mapping[str, str] | None) -> None:
    """Raise if Pass already decided the stream is blocked (headers, before SSE)."""
    policy = _header_get(headers, "x-tonia-policy-block")
    if policy:
        raise PolicyBlockError(
            "tonia policy block",
            code=policy,
            retryable=False,
            status=200,
            headers=headers,
            policy_block={"code": policy},
        )
    entitlement = _header_get(headers, "x-tonia-entitlement-block")
    if entitlement:
        raise EntitlementError(
            "tonia entitlement block",
            code=entitlement,
            retryable=True,
            status=200,
            headers=headers,
            entitlement_block={"code": entitlement},
        )


def raise_from_response_body(
    body: Any,
    *,
    status: int,
    headers: Mapping[str, str] | None = None,
) -> None:
    if not isinstance(body, dict):
        return

    if status == 200:
        if "_tonia_policy_block" in body:
            carrier = body["_tonia_policy_block"]
            raise PolicyBlockError(
                "tonia policy block",
                code=(
                    str(carrier.get("code"))
                    if isinstance(carrier, dict) and carrier.get("code")
                    else None
                ),
                retryable=(
                    bool(carrier.get("retryable"))
                    if isinstance(carrier, dict)
                    and carrier.get("retryable") is not None
                    else False
                ),
                status=200,
                body=body,
                headers=headers,
                policy_block=carrier,
            )
        if "_tonia_entitlement_block" in body:
            carrier = body["_tonia_entitlement_block"]
            raise EntitlementError(
                "tonia entitlement block",
                code=(
                    str(carrier.get("code"))
                    if isinstance(carrier, dict) and carrier.get("code")
                    else None
                ),
                status=200,
                body=body,
                headers=headers,
                entitlement_block=carrier,
                scope=(
                    str(carrier.get("scope"))
                    if isinstance(carrier, dict) and isinstance(carrier.get("scope"), str)
                    else None
                ),
                retryable=(
                    bool(carrier.get("retryable"))
                    if isinstance(carrier, dict)
                    and carrier.get("retryable") is not None
                    else True
                ),
            )
        return

    if status == 404 and body.get("error") == "not_found":
        raise InvalidRequestError(
            "not_found",
            status=404,
            code="not_found",
            body=body,
            headers=headers,
            retryable=False,
        )

    envelope = body.get("error")
    if isinstance(envelope, dict):
        raise error_from_structured(envelope, status=status, body=body, headers=headers)
    if isinstance(envelope, str):
        raise ToniaError(
            envelope,
            type="invalid_request_error",
            status=status,
            body=body,
            headers=headers,
        )
