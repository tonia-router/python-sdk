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
    AgentBlockError,
    PolicyBlockError,
    RateLimitError,
    TenantUpstreamBlockedError,
    ToniaError,
)
from .limits import LimitInfo
from .realtime import (
    AsyncRealtimeSession,
    RealtimeSession,
    realtime_connect_url,
    realtime_ws_url,
)
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
    "AgentBlockError",
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
    "RealtimeSession",
    "AsyncRealtimeSession",
    "realtime_ws_url",
    "realtime_connect_url",
]

__version__ = SDK_VERSION
