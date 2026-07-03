"""Generic agent desk session models and in-memory store."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar
from uuid import UUID, uuid4

from agent_desk.privacy import PseudonymMap

SlotsT = TypeVar("SlotsT")


@dataclass
class PendingApproval:
    kind: str
    summary: str
    details: dict[str, Any]
    idempotency_key: str


@dataclass
class DeskSession(Generic[SlotsT]):
    session_id: UUID
    operator_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    messages: list[dict[str, str]] = field(default_factory=list)
    slots: SlotsT | None = None
    pseudonyms: PseudonymMap = field(default_factory=PseudonymMap)
    pending_approval: PendingApproval | None = None
    tool_calls_this_turn: int = 0


class SessionStore(Generic[SlotsT]):
    """In-memory session store for agent threads (MVP single-process).

    Production horizontal scale requires a durable backing service (Postgres/Redis).
    """

    def __init__(self) -> None:
        self._sessions: dict[UUID, DeskSession[SlotsT]] = {}

    def create(self, operator_id: str, *, slots: SlotsT | None = None) -> DeskSession[SlotsT]:
        session = DeskSession(session_id=uuid4(), operator_id=operator_id, slots=slots)
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: UUID) -> DeskSession[SlotsT] | None:
        return self._sessions.get(session_id)

    def save(self, session: DeskSession[SlotsT]) -> None:
        session.updated_at = datetime.now(UTC)
        self._sessions[session.session_id] = session
