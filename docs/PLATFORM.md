# Platform manifest

**org-python-platform** is a domain-agnostic Python monorepo. Packages expose explicit settings dataclasses and constructor injection — no shared application `Settings` singleton and no product-specific routes or workflows in this repository.

Domain tools, coordinators, intent parsers, workflow implementations, and HTTP APIs belong in **consumer applications** that depend on these packages.

## Packages

| Directory | PyPI name | Responsibility |
|-----------|-----------|----------------|
| `packages/litellm_gateway` | `litellm-gateway` | LiteLLM Router routing, fallbacks, cache, input guardrails, cost/usage |
| `packages/langfuse_tracing` | `langfuse-tracing` | Structured audit logging; optional Langfuse spans |
| `packages/fastapi_platform` | `fastapi-platform-kit` | FastAPI exception handlers, health router, JWT helpers, SQLAlchemy mixins |
| `packages/sqlalchemy_idempotency` | `sqlalchemy-idempotency` | Idempotent command store for commit-style endpoints |
| `packages/agent_desk` | `agent-desk-starter` | Generic LangGraph SOP skeleton, desk sessions, privacy/redaction helpers |

## Configuration pattern

Each package defines frozen dataclass settings (for example `LlmGatewaySettings`, `LangfuseTracingSettings`, `JwtSettings`). Your application maps environment variables or config files into those types and passes them into constructors.

See [`.env.example`](../.env.example) and [`scripts/from_env.py`](../scripts/from_env.py) for local development helpers — not required at runtime in production apps.

## What stays in consumer applications

Implement in the repo that owns your product domain:

- REST routers and RBAC tied to your roles
- Multi-step **workflow** classes and orchestrators
- Agent **coordinator**, **tools**, and typed **slots**
- Durable session/checkpoint stores (Postgres, Redis)
- Product-specific guardrails (NeMo, spend ledgers, domain validation)
- Settings adapters from your app config → platform dataclasses

## Cookbooks (patterns only)

| Doc | Purpose |
|-----|---------|
| [workflow-desk](workflow-desk/README.md) | HITL multi-step REST workflow shape (generic) |

Cookbooks describe architecture; they do not ship runnable domain code.

## Versioning

All packages share the version in [`VERSION`](../VERSION). Release process: [PUBLISH.md](PUBLISH.md). Install options: [CONSUMING.md](CONSUMING.md).

## Organization CI

Integrate reusable pipelines from **org-ci-standards** with this repo’s `make` targets and GitHub Actions: [ORG-CI-STANDARDS.md](ORG-CI-STANDARDS.md).
