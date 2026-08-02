"""Soft-limit warning headers on successful runtime responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class LimitInfo:
    warning: str | None = None
    scope: str | None = None
    kind: str | None = None
    used: str | None = None
    value: str | None = None
    remaining: str | None = None
    period_ends_at: str | None = None


_LIMIT_KEYS: tuple[tuple[str, str], ...] = (
    ("warning", "x-tonia-limit-warning"),
    ("scope", "x-tonia-limit-scope"),
    ("kind", "x-tonia-limit-kind"),
    ("used", "x-tonia-limit-used"),
    ("value", "x-tonia-limit-value"),
    ("remaining", "x-tonia-limit-remaining"),
    ("period_ends_at", "x-tonia-limit-period-ends-at"),
)


def limits_from_headers(headers: Mapping[str, str] | None) -> LimitInfo | None:
    if not headers:
        return None
    lowered = {str(k).lower(): str(v) for k, v in headers.items()}
    values: dict[str, str | None] = {}
    any_set = False
    for field, header in _LIMIT_KEYS:
        value = lowered.get(header)
        values[field] = value
        if value:
            any_set = True
    if not any_set:
        return None
    return LimitInfo(**values)
