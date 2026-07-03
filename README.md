# org-python-platform

Reusable Python packages extracted from [LMS-AI](https://github.com/org/LMS-AI) following the tiered extraction plan.

## Packages

| Package | PyPI name | Source in LMS-AI | Status |
|---------|-----------|------------------|--------|
| [litellm_gateway](packages/litellm_gateway/) | `litellm-gateway` | `src/lms/shared/llm/` | Extracted |
| [langfuse_tracing](packages/langfuse_tracing/) | `langfuse-tracing` | `src/lms/shared/observability/tracing.py` | Extracted |
| [fastapi_platform](packages/fastapi_platform/) | `fastapi-platform-kit` | `src/lms/shared/http/`, `auth/`, `db/` | Extracted |
| [sqlalchemy_idempotency](packages/sqlalchemy_idempotency/) | `sqlalchemy-idempotency` | `src/lms/shared/idempotency/` | Extracted |
| [agent_desk](packages/agent_desk/) | `agent-desk-starter` | `src/lms/agent/graph.py`, generic masking | Extracted |

## Cookbooks

- [workflow-desk](docs/workflow-desk/README.md) — HITL workflow API pattern (from `lms/api/workflows/`)

## Extraction order

1. **LLM + tracing** — `litellm_gateway`, `langfuse_tracing`
2. **FastAPI platform + idempotency** — `fastapi_platform`, `sqlalchemy_idempotency`
3. **Agent desk** — `agent_desk`
4. **Workflow cookbook** — docs only

## Install (local dev)

```bash
cd packages/litellm_gateway && pip install -e .
cd packages/langfuse_tracing && pip install -e .
# … repeat per package
```

## LMS adoption

LMS-AI continues to use in-tree copies until wired via `pyproject.toml` optional deps. See `LMS-AI/docs/extraction/README.md`.

## License

Same as LMS-AI (project-specific).
