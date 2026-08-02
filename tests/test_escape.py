import pytest

from tonia.escape import assert_path_allowed, normalize_path
from tonia.errors import PathNotAllowedError


def test_normalize_path() -> None:
    assert normalize_path("v1/models?x=1") == "/v1/models"
    assert normalize_path("//v1//chat//completions") == "/v1/chat/completions"


@pytest.mark.parametrize(
    "path",
    [
        "/v1/models",
        "/v1/chat/completions",
        "/v1/public/catalogue",
        "/v1/status",
        "/v1/conversations/export",
    ],
)
def test_supported(path: str) -> None:
    assert assert_path_allowed(path) == path


@pytest.mark.parametrize(
    "path",
    [
        "/v1" + "/" + "adm" + "in" + "/keys",
        "/v1/models/../" + "adm" + "in" + "/x",
        "/V1/" + "ADM" + "IN" + "/foo",
        "/v1/billing/checkout",
        "/healthz",
    ],
)
def test_unsupported(path: str) -> None:
    with pytest.raises(PathNotAllowedError):
        assert_path_allowed(path)
