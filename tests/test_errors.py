import pytest

from tonia.errors import (
    ApiError,
    AuthenticationError,
    BillingError,
    ByokKeyMissingError,
    EntitlementError,
    InvalidRequestError,
    ManagedCredentialUnavailableError,
    AgentBlockError,
    PolicyBlockError,
    RateLimitError,
    TenantUpstreamBlockedError,
    error_from_http_fallback,
    error_from_structured,
    raise_from_response_body,
    raise_from_stream_headers,
)


def test_http_200_policy_carrier() -> None:
    with pytest.raises(PolicyBlockError) as exc:
        raise_from_response_body(
            {"_tonia_policy_block": {"code": "regulated_content_detected"}},
            status=200,
        )
    assert exc.value.policy_block["code"] == "regulated_content_detected"


def test_http_200_agent_carrier() -> None:
    with pytest.raises(AgentBlockError) as exc:
        raise_from_response_body(
            {
                "_tonia_agent_block": {
                    "code": "tool_calls_disabled_by_profile",
                    "capability": "tool_calls",
                    "retryable": False,
                }
            },
            status=200,
        )
    assert exc.value.agent_block["code"] == "tool_calls_disabled_by_profile"
    assert exc.value.code == "tool_calls_disabled_by_profile"
    assert exc.value.capability == "tool_calls"
    assert exc.value.retryable is False


def test_http_200_entitlement_carrier() -> None:
    with pytest.raises(EntitlementError) as exc:
        raise_from_response_body(
            {
                "_tonia_entitlement_block": {
                    "code": "managed_budget_exhausted",
                    "retryable": False,
                }
            },
            status=200,
        )
    assert exc.value.entitlement_block["code"] == "managed_budget_exhausted"
    assert exc.value.code == "managed_budget_exhausted"
    assert exc.value.retryable is False


def test_public_model_flat_404_is_typed() -> None:
    with pytest.raises(InvalidRequestError) as exc:
        raise_from_response_body({"error": "not_found"}, status=404)
    assert exc.value.code == "not_found"
    assert exc.value.retryable is False


@pytest.mark.parametrize(
    ("error_type", "expected"),
    [
        ("authentication_error", AuthenticationError),
        ("billing_error", BillingError),
        ("entitlement_error", EntitlementError),
        ("invalid_request_error", InvalidRequestError),
        ("byok_key_missing", ByokKeyMissingError),
        ("policy_block", PolicyBlockError),
        ("agent_block", AgentBlockError),
        ("tenant_upstream_blocked", TenantUpstreamBlockedError),
        ("managed_credential_unavailable", ManagedCredentialUnavailableError),
        ("rate_limit_error", RateLimitError),
        ("api_error", ApiError),
    ],
)
def test_structured_error_taxonomy_maps_to_specific_class(
    error_type: str, expected: type[Exception]
) -> None:
    error = error_from_structured(
        {
            "type": error_type,
            "code": "synthetic_code",
            "message": "Synthetic",
            "retryable": True,
        },
        status=503,
        headers={"retry-after": "60"},
    )
    assert isinstance(error, expected)
    assert error.code == "synthetic_code"
    assert error.retryable is True
    assert error.status == 503
    assert error.headers["retry-after"] == "60"
    assert error.retry_after_seconds == 60


def test_stream_policy_header_raises() -> None:
    with pytest.raises(PolicyBlockError) as exc:
        raise_from_stream_headers(
            {"x-tonia-policy-block": "regulated_content_detected"}
        )
    assert exc.value.code == "regulated_content_detected"
    assert exc.value.retryable is False
    assert exc.value.policy_block["code"] == "regulated_content_detected"


def test_stream_agent_header_raises() -> None:
    with pytest.raises(AgentBlockError) as exc:
        raise_from_stream_headers(
            {
                "x-tonia-agent-block": "tool_calls_disabled_by_profile",
                "x-tonia-agent-capability": "tool_calls",
            }
        )
    assert exc.value.code == "tool_calls_disabled_by_profile"
    assert exc.value.capability == "tool_calls"
    assert exc.value.retryable is False
    assert exc.value.agent_block["code"] == "tool_calls_disabled_by_profile"


def test_stream_entitlement_header_raises() -> None:
    with pytest.raises(EntitlementError) as exc:
        raise_from_stream_headers(
            {"x-tonia-entitlement-block": "managed_budget_exhausted"}
        )
    assert exc.value.code == "managed_budget_exhausted"
    assert exc.value.retryable is True


def test_stream_headers_without_block_are_noop() -> None:
    raise_from_stream_headers({"content-type": "text/event-stream"})


def test_provider_requires_surface_is_invalid_request() -> None:
    with pytest.raises(InvalidRequestError) as exc:
        raise_from_response_body(
            {
                "error": {
                    "type": "invalid_request_error",
                    "code": "provider_requires_surface",
                    "required_surface": "interactions",
                    "retryable": False,
                }
            },
            status=400,
        )
    assert exc.value.code == "provider_requires_surface"
    assert exc.value.retryable is False
    assert exc.value.body["error"]["required_surface"] == "interactions"


def test_admission_429_lifts_reason_scope_and_retry_after() -> None:
    with pytest.raises(RateLimitError) as exc:
        raise_from_response_body(
            {
                "error": {
                    "type": "rate_limit_error",
                    "code": "admission_rate_limited",
                    "reason": "rpm_per_key",
                    "scope": "key",
                    "retryable": True,
                }
            },
            status=429,
            headers={"Retry-After": "47"},
        )
    assert exc.value.code == "admission_rate_limited"
    assert exc.value.reason == "rpm_per_key"
    assert exc.value.scope == "key"
    assert exc.value.retryable is True
    assert exc.value.retry_after_seconds == 47


def test_quota_429_is_entitlement_not_rate_limit() -> None:
    with pytest.raises(EntitlementError) as exc:
        raise_from_response_body(
            {
                "error": {
                    "type": "entitlement_error",
                    "code": "request_quota_exhausted",
                    "scope": "organization",
                    "retryable": True,
                }
            },
            status=429,
            headers={"Retry-After": "86400"},
        )
    assert exc.value.code == "request_quota_exhausted"
    assert exc.value.scope == "organization"
    assert exc.value.retryable is True
    assert exc.value.retry_after_seconds == 86400


def test_http_200_entitlement_carrier_lifts_retry_after_and_scope() -> None:
    with pytest.raises(EntitlementError) as exc:
        raise_from_response_body(
            {
                "_tonia_entitlement_block": {
                    "type": "entitlement_block",
                    "code": "request_quota_exhausted",
                    "scope": "organization",
                    "retryable": True,
                }
            },
            status=200,
            headers={"Retry-After": "3600"},
        )
    assert exc.value.code == "request_quota_exhausted"
    assert exc.value.scope == "organization"
    assert exc.value.retryable is True
    assert exc.value.retry_after_seconds == 3600


def test_audit_tip_contention_parses_retry_after_and_request_id() -> None:
    with pytest.raises(ApiError) as exc:
        raise_from_response_body(
            {
                "error": {
                    "type": "api_error",
                    "code": "audit_tip_contention",
                    "retryable": True,
                }
            },
            status=503,
            headers={
                "Retry-After": "1",
                "x-tonia-request-id": "tonia_req_abc",
            },
        )
    assert exc.value.code == "audit_tip_contention"
    assert exc.value.retryable is True
    assert exc.value.retry_after_seconds == 1
    assert exc.value.request_id == "tonia_req_abc"


def test_http_date_retry_after_is_ignored() -> None:
    error = error_from_structured(
        {
            "type": "rate_limit_error",
            "code": "admission_rate_limited",
            "retryable": True,
        },
        status=429,
        headers={"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"},
    )
    assert isinstance(error, RateLimitError)
    assert error.retry_after_seconds is None


def test_bare_429_fallback_is_retryable_rate_limit() -> None:
    error = error_from_http_fallback(429, headers={"Retry-After": "2"})
    assert isinstance(error, RateLimitError)
    assert error.retryable is True
    assert error.retry_after_seconds == 2
    assert error.reason is None


def test_bare_503_fallback_is_retryable_api_error() -> None:
    error = error_from_http_fallback(503, headers={"Retry-After": "60"})
    assert isinstance(error, ApiError)
    assert error.retryable is True
    assert error.retry_after_seconds == 60


def test_bare_400_fallback_stays_non_retryable() -> None:
    error = error_from_http_fallback(400)
    assert error.type == "invalid_request_error"
    assert error.retryable is False
