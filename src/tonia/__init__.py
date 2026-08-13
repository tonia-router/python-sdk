"""Official Python client for tonia Pass."""

from .async_client import AsyncTonia
from .client import Tonia
from ._transport import IMAGE_TIMEOUT_S, SDK_USER_AGENT, SDK_VERSION
from .errors import (
    ApiError,
    AuthenticationError,
    BillingError,
    ByokKeyMissingError,
    EntitlementError,
    InvalidRequestError,
    ManagedCredentialUnavailableError,
    PathNotAllowedError,
    PolicyBlockError,
    RateLimitError,
    TenantUpstreamBlockedError,
    ToniaError,
)
from .limits import LimitInfo
from .stream import SseEvent

__all__ = [
    "Tonia",
    "AsyncTonia",
    "ToniaError",
    "AuthenticationError",
    "BillingError",
    "EntitlementError",
    "InvalidRequestError",
    "ByokKeyMissingError",
    "PolicyBlockError",
    "TenantUpstreamBlockedError",
    "ManagedCredentialUnavailableError",
    "RateLimitError",
    "ApiError",
    "PathNotAllowedError",
    "LimitInfo",
    "SseEvent",
    "IMAGE_TIMEOUT_S",
    "SDK_USER_AGENT",
    "SDK_VERSION",
]

__version__ = SDK_VERSION
