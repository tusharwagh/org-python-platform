# Changelog

All packages in this monorepo share the version in [`VERSION`](VERSION).

## [Unreleased]

### Added

- [`docs/ORG-CI-STANDARDS.md`](docs/ORG-CI-STANDARDS.md) — user guide for integrating with org-ci-standards (reusable workflows, secrets, release order).

### Changed

- Documentation and manifests are domain-agnostic; product-specific extraction maps belong in consumer repositories.
- [`docs/PLATFORM.md`](docs/PLATFORM.md) and [`docs/consumer-integration.md`](docs/consumer-integration.md) replace LMS-oriented extraction checklists in this repo.

### Removed

- `agent_desk.graph.build_issue_sop_graph` / `compile_issue_sop_graph` aliases (use `build_sop_graph` / `compile_sop_graph`).

## [0.1.0] — 2026-07-03

### Added

- `litellm-gateway` — LiteLLM Router gateway with fallbacks and guardrails
- `langfuse-tracing` — Langfuse spans and structured audit logging
- `fastapi-platform-kit` — FastAPI errors, health, JWT, SQLAlchemy mixins
- `sqlalchemy-idempotency` — Idempotent command API store
- `agent-desk-starter` — LangGraph HITL desk primitives
- `docs/workflow-desk/` cookbook
- GitHub Actions publish workflow (GitHub Packages on tag)
- Consumer docs: `docs/CONSUMING.md`, release checklist: `docs/PUBLISH.md`

[0.1.0]: https://github.com/tusharwagh/org-python-platform/releases/tag/v0.1.0
