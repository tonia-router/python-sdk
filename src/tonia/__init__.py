"""Official Python client for tonia Pass."""

from .async_client import AsyncTonia
from .client import Tonia
from .errors import (
    AuthenticationError,
    BillingError,
    ByokKeyMissingError,
    EntitlementError,
    InvalidRequestError,
    ManagedCredentialUnavailableError,
    PathNotAllowedError,
    PolicyBlockError,
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
    "PathNotAllowedError",
    "LimitInfo",
    "SseEvent",
]

__version__ = "0.1.0"
