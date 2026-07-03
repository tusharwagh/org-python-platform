"""Idempotency ORM model factory."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, TypeVar

from sqlalchemy import DateTime, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

IDEMPOTENCY_TTL = timedelta(hours=24)

BaseT = TypeVar("BaseT", bound=type[DeclarativeBase])


@dataclass(frozen=True, slots=True)
class IdempotencyResult:
    status_code: int
    body: dict[str, Any]


def make_idempotency_model(base: BaseT) -> BaseT:
    """Return an IdempotencyRecord mapped class bound to the caller's DeclarativeBase."""

    class IdempotencyRecord(base):  # type: ignore[misc, valid-type]
        __tablename__ = "idempotency_records"
        __table_args__ = (
            UniqueConstraint("scope_key", "idempotency_key", name="uq_idempotency_scope_key"),
        )

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        scope_key: Mapped[str] = mapped_column(String(512), nullable=False)
        idempotency_key: Mapped[str] = mapped_column(String(64), nullable=False)
        payload_hash: Mapped[str] = mapped_column(String(64), nullable=False)
        response_status: Mapped[int] = mapped_column(nullable=False)
        response_body: Mapped[str] = mapped_column(Text, nullable=False)
        expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
        )

    return IdempotencyRecord  # type: ignore[return-value]
