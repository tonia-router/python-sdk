import pytest

from tonia.errors import (
    AuthenticationError,
    BillingError,
    ByokKeyMissingError,
    EntitlementError,
    InvalidRequestError,
    ManagedCredentialUnavailableError,
    PolicyBlockError,
    TenantUpstreamBlockedError,
    error_from_structured,
    raise_from_response_body,
)


def test_chat_200_policy_carrier() -> None:
    with pytest.raises(PolicyBlockError) as exc:
        raise_from_response_body(
            {"_tonia_policy_block": {"code": "regulated_content_detected"}},
            status=200,
        )
    assert exc.value.policy_block["code"] == "regulated_content_detected"


def test_chat_200_entitlement_carrier() -> None:
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
        ("tenant_upstream_blocked", TenantUpstreamBlockedError),
        ("managed_credential_unavailable", ManagedCredentialUnavailableError),
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
