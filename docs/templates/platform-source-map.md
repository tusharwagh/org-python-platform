# Platform source map (copy to your application repo)

Use this template in **your** repository to document how org-python-platform packages map to your codebase. Do not commit product-specific paths to org-python-platform.

## Pinned platform version

- org-python-platform: `vX.Y.Z` (git tag or GitHub Packages version)
- Install method: git URL / GitHub Packages / editable local

## Settings adapters

| Platform type | Your config / env | Adapter location |
|---------------|-------------------|------------------|
| `LlmGatewaySettings` | | |
| `LangfuseTracingSettings` | | |
| `JwtSettings` | | |

## Package usage

| Platform package | Your module(s) | Notes |
|------------------|----------------|-------|
| `litellm-gateway` | | |
| `langfuse-tracing` | | |
| `fastapi-platform-kit` | | |
| `sqlalchemy-idempotency` | | |
| `agent-desk-starter` | | |

## Domain-only (not in org-python-platform)

| Concern | Your module(s) |
|---------|----------------|
| HTTP routers | |
| Workflows | |
| Orchestrators | |
| Agent coordinator / tools / slots | |
| Durable session store | |

## Migration history

- Date / version: notes on breaking changes and adapter updates
