"""PII redaction and HITL detail sanitization for agent desks."""

from __future__ import annotations

import re
from typing import Any
from uuid import UUID

_PII_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN_REDACTED]"),
    (re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"), "[CARD_REDACTED]"),
]

_DEFAULT_INTERNAL_KEYS = frozenset(
    {
        "id",
        "operator_id",
        "session_id",
        "tenant_id",
        "user_id",
    }
)


def redact_for_audit(text: str) -> str:
    for pattern, replacement in _PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def sanitize_approval_details(
    details: dict[str, Any],
    *,
    strip_keys: frozenset[str] | None = None,
) -> dict[str, Any]:
    """Strip internal identifiers from HITL payloads exposed on the API."""
    keys = strip_keys or _DEFAULT_INTERNAL_KEYS

    def _clean(value: Any) -> Any:
        if isinstance(value, dict):
            cleaned: dict[str, Any] = {
                key: _clean(item) for key, item in value.items() if key not in keys
            }
            return cleaned
        if isinstance(value, list):
            return [_clean(item) for item in value]
        return value

    result = _clean(details)
    assert isinstance(result, dict)
    return result


class PseudonymMap:
    """Maps real UUIDs to stable pseudonyms within one agent session."""

    def __init__(self, *, prefix: str = "ENTITY") -> None:
        self._prefix = prefix
        self._entities: dict[str, dict[UUID, str]] = {}

    def label(self, kind: str, entity_id: UUID) -> str:
        bucket = self._entities.setdefault(kind, {})
        if entity_id not in bucket:
            bucket[entity_id] = f"{self._prefix}_{kind.upper()}_{len(bucket) + 1}"
        return bucket[entity_id]

    def resolve(self, kind: str, pseudonym: str) -> UUID | None:
        for uid, label in self._entities.get(kind, {}).items():
            if label == pseudonym:
                return uid
        return None
