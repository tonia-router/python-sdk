"""Typed errors raised by the tonia Pass client."""

from __future__ import annotations

from typing import Any, Mapping


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


class AuthenticationError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="authentication_error", **kwargs)


class BillingError(ToniaError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="billing_error", **kwargs)


class EntitlementError(ToniaError):
    def __init__(
        self, message: str, *, entitlement_block: Any = None, **kwargs: Any
    ) -> None:
        super().__init__(message, type="entitlement_error", **kwargs)
        self.entitlement_block = entitlement_block


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
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, type="managed_credential_unavailable", **kwargs)


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
    mapping: dict[str, type[ToniaError]] = {
        "authentication_error": AuthenticationError,
        "billing_error": BillingError,
        "entitlement_error": EntitlementError,
        "invalid_request_error": InvalidRequestError,
        "byok_key_missing": ByokKeyMissingError,
        "policy_block": PolicyBlockError,
        "tenant_upstream_blocked": TenantUpstreamBlockedError,
        "managed_credential_unavailable": ManagedCredentialUnavailableError,
    }
    cls = mapping.get(str(err.get("type")), ToniaError)
    if cls is ToniaError:
        return ToniaError(message, type=str(err.get("type") or "unknown"), **base)
    return cls(message, **base)


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
