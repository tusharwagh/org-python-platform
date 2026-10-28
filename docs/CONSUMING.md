# Consuming org-python-platform packages

Repository: https://github.com/tusharwagh/org-python-platform

Five installable packages (shared version, see [`VERSION`](../VERSION)):

| PyPI name | Subdirectory |
|-----------|--------------|
| `litellm-gateway` | `packages/litellm_gateway` |
| `langfuse-tracing` | `packages/langfuse_tracing` |
| `fastapi-platform-kit` | `packages/fastapi_platform` |
| `sqlalchemy-idempotency` | `packages/sqlalchemy_idempotency` |
| `agent-desk-starter` | `packages/agent_desk` |

## Option A — Git URL (recommended for open repos)

No registry auth. Pin to a **tag** for reproducible CI.

```toml
# pyproject.toml — requires tool.hatch.metadata.allow-direct-references = true (hatch)
dependencies = [
    "litellm-gateway @ git+https://github.com/tusharwagh/org-python-platform.git@v0.1.0#subdirectory=packages/litellm_gateway",
    "langfuse-tracing @ git+https://github.com/tusharwagh/org-python-platform.git@v0.1.0#subdirectory=packages/langfuse_tracing",
    "fastapi-platform-kit @ git+https://github.com/tusharwagh/org-python-platform.git@v0.1.0#subdirectory=packages/fastapi_platform",
    "sqlalchemy-idempotency @ git+https://github.com/tusharwagh/org-python-platform.git@v0.1.0#subdirectory=packages/sqlalchemy_idempotency",
    "agent-desk-starter @ git+https://github.com/tusharwagh/org-python-platform.git@v0.1.0#subdirectory=packages/agent_desk",
]
```

Install:

```bash
pip install -e .
```

**Release order:** push `org-python-platform` tag `v0.1.0` before consumers reference `@v0.1.0`. See [PUBLISH.md](PUBLISH.md).

### pip only (no pyproject)

```bash
pip install "litellm-gateway @ git+https://github.com/tusharwagh/org-python-platform.git@v0.1.0#subdirectory=packages/litellm_gateway"
```

## Option B — GitHub Packages (internal PyPI)

Faster installs in CI when wheels are cached on GitHub. Requires authentication.

### One-time auth

Create a PAT or use `GITHUB_TOKEN` with `read:packages` (and `write:packages` for publish).

```bash
# ~/.pip/pip.conf or CI secret
[global]
extra-index-url = https://__token__:<GITHUB_TOKEN>@pypi.pkg.github.com/tusharwagh/simple/
```

Or export for a single install:

```bash
export PIP_EXTRA_INDEX_URL="https://__token__:${GITHUB_TOKEN}@pypi.pkg.github.com/tusharwagh/simple/"
```

Copy [`pip.conf.example`](../pip.conf.example) and replace the token placeholder.

### pyproject.toml (version pins)

```toml
dependencies = [
    "litellm-gateway==0.1.0",
    "langfuse-tracing==0.1.0",
    "fastapi-platform-kit==0.1.0",
    "sqlalchemy-idempotency==0.1.0",
    "agent-desk-starter==0.1.0",
]
```

CI must set `PIP_EXTRA_INDEX_URL` (or `pip.conf`) before `pip install`.

### GitHub Actions (consumer)

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
- name: Configure GitHub Packages index
  run: |
    echo "PIP_EXTRA_INDEX_URL=https://__token__:${{ secrets.GITHUB_TOKEN }}@pypi.pkg.github.com/tusharwagh/simple/" >> "$GITHUB_ENV"
- run: pip install -e ".[dev]"
```

For cross-repo private consumers, use a PAT with `read:packages` stored as a repository secret.

## Option C — editable local monorepo (development)

```bash
git clone https://github.com/tusharwagh/org-python-platform.git
cd org-python-platform/packages/litellm_gateway && pip install -e .
# repeat per package, or use file: deps in consumer pyproject
```

## Wiring in your application

Map your app configuration to platform settings dataclasses and inject them at construction time. Patterns and layout: [consumer-integration.md](consumer-integration.md).

## Organization CI (org-ci-standards)

Shared workflow pins, GitHub Packages auth in CI, and release ordering with this repo: [ORG-CI-STANDARDS.md](ORG-CI-STANDARDS.md).

## Upgrading

1. Read [CHANGELOG.md](../CHANGELOG.md) for the target version.
2. Bump git `@vX.Y.Z` or `==X.Y.Z` pins in consumer `pyproject.toml`.
3. Re-run tests; update your config adapters if platform settings fields changed.
