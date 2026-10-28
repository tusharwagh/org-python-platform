# Consumer integration

How to wire **org-python-platform** packages into a domain application without coupling this monorepo to your product.

## Principles

1. **Inject settings** — build `LlmGatewaySettings`, `LangfuseTracingSettings`, `JwtSettings`, etc. from your config layer; do not import platform code from a global app singleton inside the packages.
2. **Own your HTTP surface** — use `fastapi-platform-kit` for shared handlers and helpers; define routes and dependencies in your repo.
3. **Own agents and workflows** — use `agent-desk-starter` for generic session/graph primitives; implement coordinators, tools, and workflows locally.
4. **Pin versions** — git tags or GitHub Packages versions per [CONSUMING.md](CONSUMING.md); upgrade using [CHANGELOG.md](../CHANGELOG.md).

## Minimal wiring example

```python
from litellm_gateway import LlmGateway, LlmGatewaySettings
from langfuse_tracing import LangfuseTracing, LangfuseTracingSettings

def build_llm_gateway(app_config) -> LlmGateway:
    settings = LlmGatewaySettings(
        agent_mock_llm=app_config.mock_llm,
        groq_api_key=app_config.groq_api_key,
        llm_provider=app_config.llm_provider,
        llm_model=app_config.llm_model,
    )
    return LlmGateway.from_settings(settings)

def build_tracing(app_config) -> LangfuseTracing:
    return LangfuseTracing(
        LangfuseTracingSettings(
            langfuse_public_key=app_config.langfuse_public_key,
            langfuse_secret_key=app_config.langfuse_secret_key,
            langfuse_host=app_config.langfuse_host,
        )
    )
```

Keep adapter functions (`app_config → platform settings`) in **your** codebase.

## Suggested layout in a consumer repo

```
your-app/
  src/your_app/
    config.py              # app settings
    platform/              # adapters to org-python-platform dataclasses
    api/                   # FastAPI routers
    workflows/             # multi-step domain workflows
    agent/                 # coordinator, tools, domain slots
  docs/platform/           # product-specific maps & migration notes
```

## Idempotency on commits

Use `sqlalchemy-idempotency` on mutating workflow steps. Choose scope keys that name your domain, for example `workflows:{use_case}:commit`:

```python
cached = find_cached_response(
    session,
    scope_key="workflows:example:commit",
    idempotency_key=key,
    payload=body,
)
```

## Where product-specific docs go

Document in **your** repository:

- Which platform version you pin (`.platform-version` or lockfile)
- Field-by-field mapping from your config to platform settings
- Workflow endpoint tables and orchestrator ownership
- Agent tool registry and HITL approval rules

Do not add those details to org-python-platform; keep this monorepo domain-agnostic.

## Source map template

Copy [templates/platform-source-map.md](templates/platform-source-map.md) into your application repo (for example `docs/platform/source-map.md`) and maintain product-specific paths there.

## Reference consumers

Applications that use these packages publish integration guides in their own repositories. This monorepo does not list product-specific module paths.
