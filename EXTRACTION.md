# Extraction manifest

Canonical source for reusable LMS infrastructure. Each package decouples from `lms.config.Settings` via explicit settings dataclasses or constructor injection.

## Tier 1 — LLM gateway + Langfuse tracing

| LMS path | Package | Notes |
|----------|---------|-------|
| `shared/llm/models.py` | `litellm_gateway.models` | DTOs and errors |
| `shared/llm/routing.py` | `litellm_gateway.routing` | `LlmGatewaySettings` instead of `Settings` |
| `shared/llm/gateway.py` | `litellm_gateway.gateway` | `LlmGateway` class |
| `shared/llm/guardrails.py` | `litellm_gateway.guardrails` | Input validation |
| `shared/llm/cost.py` | `litellm_gateway.cost` | Token/cost extraction |
| `shared/observability/tracing.py` | `langfuse_tracing.tracing` | `LangfuseTracingSettings` |

**Stays in LMS:** `shared/llm/nemo_guardrails.py` (optional NeMo integration), spend SQLAlchemy models.

## Tier 2 — FastAPI platform + idempotency

| LMS path | Package | Notes |
|----------|---------|-------|
| `shared/http/errors.py` | `fastapi_platform.errors` | `register_exception_handlers(debug=…)` |
| `shared/http/health.py` | `fastapi_platform.health` | Health router factory |
| `shared/auth/jwt.py` | `fastapi_platform.jwt` | `JwtSettings` injected |
| `shared/db/mixins.py` | `fastapi_platform.db` | SQLAlchemy mixins |
| `shared/idempotency/` | `sqlalchemy_idempotency` | Generic `DeclarativeBase` store |

**Stays in LMS:** rate-limit paths tied to loan/agent routes, `get_settings()` wiring in routers.

## Tier 3 — Agent desk starter

| LMS path | Package | Notes |
|----------|---------|-------|
| `agent/graph.py` | `agent_desk.graph` | LangGraph HITL interrupt pattern |
| `agent/masking.py` (generic) | `agent_desk.privacy` | PseudonymMap, sanitize |
| `agent/session.py` (generic) | `agent_desk.session` | `DeskSession`, `SessionStore` |

**Stays in LMS:** `coordinator.py`, `tools.py`, `intent_parser.py`, domain slots (`IssueSlots`).

## Tier 4 — Workflow desk (cookbook)

Documentation only — pattern from `api/workflows/` for human-in-the-loop REST workflows.

## Decoupling checklist (LMS follow-up)

- [ ] Add workspace deps in LMS `pyproject.toml`
- [ ] `Settings.to_llm_gateway_settings()` adapter
- [ ] Replace `from lms.shared.llm` imports
- [ ] CI: publish packages to internal PyPI or git submodules
