from __future__ import annotations

import pytest

from tonia import Tonia, realtime_connect_url, realtime_ws_url
from tonia.errors import InvalidRequestError, PathNotAllowedError
from tonia.realtime import raise_if_realtime_error


def test_ws_url_keeps_hosted_8443() -> None:
    assert (
        realtime_ws_url(base_url="https://pass-dev.tonia.ca:8443")
        == "wss://pass-dev.tonia.ca:8443/v1/realtime"
    )
    assert (
        realtime_ws_url(base_url="https://pass.tonia.ca:8443")
        == "wss://pass.tonia.ca:8443/v1/realtime"
    )


def test_ws_url_maps_local_data_plane_to_8448() -> None:
    assert (
        realtime_ws_url(base_url="http://127.0.0.1:8444")
        == "ws://127.0.0.1:8448/v1/realtime"
    )
    assert (
        realtime_ws_url(base_url="http://127.0.0.1:8448")
        == "ws://127.0.0.1:8448/v1/realtime"
    )


def test_ws_url_override_wins() -> None:
    assert (
        realtime_ws_url(
            base_url="https://pass.tonia.ca:8443",
            realtime_url="wss://pass-dev.tonia.ca:8443/v1/realtime",
        )
        == "wss://pass-dev.tonia.ca:8443/v1/realtime"
    )


def test_connect_url_defaults_cascaded_first_hop() -> None:
    url = realtime_connect_url(base_url="https://pass-dev.tonia.ca:8443")
    assert url.startswith("wss://pass-dev.tonia.ca:8443/v1/realtime?")
    assert "provider=openai" in url
    assert "model=gpt-live-1" in url
    assert "mode=cascaded" in url


def test_native_without_transcripts_is_rejected() -> None:
    with pytest.raises(InvalidRequestError) as exc:
        realtime_connect_url(
            base_url="https://pass.tonia.ca:8443",
            mode="native",
        )
    assert exc.value.code == "realtime_native_transcripts_required"


def test_webrtc_is_rejected() -> None:
    with pytest.raises(InvalidRequestError) as exc:
        realtime_connect_url(
            base_url="https://pass.tonia.ca:8443",
            webrtc=True,
        )
    assert exc.value.code == "realtime_webrtc_forbidden"


def test_http_request_still_blocks_realtime_path() -> None:
    with Tonia() as client:
        with pytest.raises(PathNotAllowedError):
            client.request("GET", "/v1/realtime")


def test_error_envelope_raises() -> None:
    with pytest.raises(InvalidRequestError) as exc:
        raise_if_realtime_error(
            {
                "error": {
                    "type": "invalid_request_error",
                    "code": "realtime_webrtc_forbidden",
                    "retryable": False,
                }
            }
        )
    assert exc.value.code == "realtime_webrtc_forbidden"
