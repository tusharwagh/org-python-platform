# org-python-platform

Domain-agnostic Python packages for LLM gateways, observability, FastAPI plumbing, idempotency, and agent desk primitives.

**Current version:** see [`VERSION`](VERSION) · **Consume:** [`docs/CONSUMING.md`](docs/CONSUMING.md) · **Release:** [`docs/PUBLISH.md`](docs/PUBLISH.md) · **Integrate:** [`docs/consumer-integration.md`](docs/consumer-integration.md) · **Org CI:** [`docs/ORG-CI-STANDARDS.md`](docs/ORG-CI-STANDARDS.md)

## Packages

| Package | PyPI name | Purpose |
|---------|-----------|---------|
| [litellm_gateway](packages/litellm_gateway/) | `litellm-gateway` | LiteLLM Router gateway, guardrails, cost tracking |
| [langfuse_tracing](packages/langfuse_tracing/) | `langfuse-tracing` | Langfuse spans and structured audit logging |
| [fastapi_platform](packages/fastapi_platform/) | `fastapi-platform-kit` | FastAPI errors, health, JWT, SQLAlchemy mixins |
| [sqlalchemy_idempotency](packages/sqlalchemy_idempotency/) | `sqlalchemy-idempotency` | Idempotent commit store |
| [agent_desk](packages/agent_desk/) | `agent-desk-starter` | LangGraph HITL skeleton, sessions, privacy helpers |

Product-specific workflows, agents, and APIs are **not** in this repo — wire these packages in your application. See [docs/PLATFORM.md](docs/PLATFORM.md).

## Cookbooks

- [workflow-desk](docs/workflow-desk/README.md) — generic HITL multi-step REST workflow pattern

## Install (consumers)

**Git URL (no registry auth):**

```toml
"litellm-gateway @ git+https://github.com/tusharwagh/org-python-platform.git@v0.1.0#subdirectory=packages/litellm_gateway"
```

**GitHub Packages (internal PyPI):**

```bash
pip install litellm-gateway==0.1.0 \
  --extra-index-url "https://__token__:${GITHUB_TOKEN}@pypi.pkg.github.com/tusharwagh/simple/"
```

Full examples: [`docs/CONSUMING.md`](docs/CONSUMING.md).

## Release

```bash
# bump VERSION + CHANGELOG, then:
make sync
make build
git tag -a v0.1.0 -m "org-python-platform v0.1.0"
git push origin main --tags   # triggers .github/workflows/publish.yml
```

## Local development

Create the IDE Python environment (`.venv` + editable package installs):

```bash
make venv          # create .venv and install all packages
make env-check     # verify .env loads
make help          # list build targets
```

Cursor/VS Code picks up `.venv/bin/python` automatically via [`.vscode/settings.json`](.vscode/settings.json).

Environment variables are documented in [`.env.example`](.env.example). From the repo root (after `make venv`):

```bash
python -c "from scripts.from_env import load_dotenv_file, llm_gateway_settings; load_dotenv_file(); print(llm_gateway_settings())"
```

## Manifest

Package scope and boundaries: [`docs/PLATFORM.md`](docs/PLATFORM.md).
