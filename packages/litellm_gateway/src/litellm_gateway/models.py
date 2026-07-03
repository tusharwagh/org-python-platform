"""LiteLLM gateway DTOs and errors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class LlmEndpoint:
    provider: str
    model: str
    api_key: str | None = None
    api_base: str | None = None


@dataclass(frozen=True, slots=True)
class LlmUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass(frozen=True, slots=True)
class LlmCompletionResult:
    response: Any
    endpoint: LlmEndpoint
    purpose: str
    cached: bool
    fallback_index: int
    cost_usd: float | None
    usage: LlmUsage | None


class LlmGatewayError(RuntimeError):
    """Base gateway failure."""


class LlmRateLimitError(LlmGatewayError):
    """Provider or router rate limit exceeded."""


class LlmGuardrailError(LlmGatewayError):
    """Input/output guardrail violation."""
