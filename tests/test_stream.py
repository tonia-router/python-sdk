import pytest

from tonia.errors import EntitlementError, PolicyBlockError
from tonia.limits import limits_from_headers
from tonia.stream import SseEvent, SseStream, feed_sse, raise_if_stream_carrier


def test_feed_sse_parses_and_keeps_remainder() -> None:
    events, rest = feed_sse("", 'data: {"a":1}\n\ndata: {"b"')
    assert len(events) == 1
    assert events[0].json == {"a": 1}
    assert rest == 'data: {"b"'


def test_stream_carrier_nested_anthropic_message_start() -> None:
    with pytest.raises(PolicyBlockError):
        raise_if_stream_carrier(
            {
                "type": "message_start",
                "message": {
                    "_tonia_policy_block": {"code": "regulated_content_detected"}
                },
            }
        )


def test_stream_carrier() -> None:
    with pytest.raises(PolicyBlockError):
        raise_if_stream_carrier(
            {"_tonia_policy_block": {"code": "regulated_content_detected"}}
        )

    with pytest.raises(EntitlementError):
        raise_if_stream_carrier(
            {"_tonia_entitlement_block": {"code": "managed_budget_exhausted"}}
        )


def test_sse_stream_close_closes_inner() -> None:
    closed = {"n": 0}

    def events():
        try:
            yield SseEvent(data="a", raw="a")
            yield SseEvent(data="b", raw="b")
        finally:
            closed["n"] += 1

    stream = SseStream(events())
    assert next(stream).data == "a"
    stream.close()
    assert closed["n"] == 1
    with pytest.raises(StopIteration):
        next(stream)


def test_sse_stream_break_closes_inner() -> None:
    closed = {"n": 0}

    def events():
        try:
            yield SseEvent(data="a", raw="a")
            yield SseEvent(data="b", raw="b")
        finally:
            closed["n"] += 1

    stream = SseStream(events())
    for event in stream:
        assert event.data == "a"
        break
    assert closed["n"] == 1


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
