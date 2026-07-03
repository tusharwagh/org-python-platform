import hashlib
import json
from datetime import UTC, datetime
from typing import Any, TypeVar

from sqlalchemy.orm import Session

from sqlalchemy_idempotency.model import IDEMPOTENCY_TTL

RecordT = TypeVar("RecordT")


class IdempotencyPayloadMismatchError(Exception):
    """Raised when an idempotency key exists but the request payload hash differs."""


def _payload_hash(payload: dict[str, Any]) -> str:
    normalized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(normalized.encode()).hexdigest()


def find_cached_response(
    session: Session,
    record_model: type[RecordT],
    *,
    scope_key: str,
    idempotency_key: str,
    payload: dict[str, Any],
) -> tuple[int, dict[str, Any]] | None:
    row = (
        session.query(record_model)
        .filter_by(scope_key=scope_key, idempotency_key=idempotency_key)
        .one_or_none()
    )
    if row is None:
        return None
    if row.payload_hash != _payload_hash(payload):  # type: ignore[attr-defined]
        raise IdempotencyPayloadMismatchError(scope_key, idempotency_key)
    return row.response_status, json.loads(row.response_body)  # type: ignore[attr-defined]


def store_response(
    session: Session,
    record_model: type[RecordT],
    *,
    scope_key: str,
    idempotency_key: str,
    payload: dict[str, Any],
    status_code: int,
    body: dict[str, Any],
) -> None:
    session.add(
        record_model(
            scope_key=scope_key,
            idempotency_key=idempotency_key,
            payload_hash=_payload_hash(payload),
            response_status=status_code,
            response_body=json.dumps(body),
            expires_at=datetime.now(UTC) + IDEMPOTENCY_TTL,
        )
    )
