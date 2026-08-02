import pytest

from tonia.errors import EntitlementError, PolicyBlockError
from tonia.limits import limits_from_headers
from tonia.stream import feed_sse, raise_if_stream_carrier


def test_feed_sse_parses_and_keeps_remainder() -> None:
    events, rest = feed_sse("", 'data: {"a":1}\n\ndata: {"b"')
    assert len(events) == 1
    assert events[0].json == {"a": 1}
    assert rest == 'data: {"b"'


def test_stream_carrier() -> None:
    with pytest.raises(PolicyBlockError):
        raise_if_stream_carrier(
            {"_tonia_policy_block": {"code": "regulated_content_detected"}}
        )

    with pytest.raises(EntitlementError):
        raise_if_stream_carrier(
            {"_tonia_entitlement_block": {"code": "managed_budget_exhausted"}}
        )


def test_limits_from_headers() -> None:
    limits = limits_from_headers(
        {
            "x-tonia-limit-warning": "usage_limit_80_percent",
            "x-tonia-limit-remaining": "17",
        }
    )
    assert limits is not None
    assert limits.warning == "usage_limit_80_percent"
    assert limits.remaining == "17"
