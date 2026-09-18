import pytest

from tonia.escape import assert_path_allowed, normalize_path
from tonia.errors import PathNotAllowedError


def test_normalize_path() -> None:
    assert normalize_path("v1/models?x=1") == "/v1/models"
    assert normalize_path("//v1//chat//completions") == "/v1/chat/completions"
    assert normalize_path("/v1/models/../chat/completions") == "/v1/chat/completions"


@pytest.mark.parametrize(
    "path",
    [
        "/v1/models",
        "/v1/chat/completions",
        "/v1/public/catalogue",
        "/v1/status",
        "/v1/interactions",
        "/v1/audio/speech",
        "/v1/audio/transcriptions",
        "/v1/systemone",
    ],
)
def test_supported(path: str) -> None:
    assert assert_path_allowed(path) == path


def test_dot_segment_traversal_to_supported_prefix_is_allowed() -> None:
    assert (
        assert_path_allowed("/v1/models/../chat/completions")
        == "/v1/chat/completions"
    )


@pytest.mark.parametrize(
    "path",
    [
        "/v1/billing/checkout",
        "/v1/conversations",
        "/v1/conversations/export",
        "/healthz",
        "/v1/models/../billing/checkout",
        "/v1/realtime",
    ],
)
def test_unsupported(path: str) -> None:
    with pytest.raises(PathNotAllowedError):
        assert_path_allowed(path)
