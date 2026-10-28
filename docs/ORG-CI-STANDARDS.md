# Integrating with org-ci-standards

User guide for wiring **org-python-platform** into your organization’s shared CI catalog (**org-ci-standards**) and keeping releases aligned with consumer applications.

This repo is a **Python package monorepo** (build + publish wheels). org-ci-standards typically owns **how** CI runs (runners, reusable workflows, secrets naming, Python version policy). org-python-platform owns **what** to run (`make build`, `make upload`, version sync).

Related org repos:

| Repo | Role |
|------|------|
| **org-ci-standards** | Reusable CI workflows, job templates, org secrets contract |
| **org-ai-standards** | AI-SDLC templates, Cursor rules/skills, drift checks (optional submodule) |
| **org-python-platform** (this repo) | Shared Python packages published to GitHub Packages |

---

## Prerequisites

- Access to **org-ci-standards** (read reusable workflows / CI components).
- GitHub Actions enabled on this repository (or GitLab CI with equivalent includes).
- Permission to use **GitHub Packages** for the org owner configured in publish (see [`TWINE_REPOSITORY_URL`](../.github/workflows/publish.yml)).
- Python **3.12** on CI (matches [`.python-version`](../.python-version) and [`build.yml`](../.github/workflows/build.yml)).

---

## CI contract in this repository

Org pipelines should call these entry points instead of duplicating package loops:

| Step | Command | When |
|------|---------|------|
| Sync versions | `make sync` | Before build on release branches or when `VERSION` changed |
| Build all wheels | `make build` | Every PR and push to `main` |
| Install publish tools | `make install-tools` | Before build/upload in CI |
| Upload to registry | `make upload` | Tag `v*` only; requires `TWINE_*` env |
| Local parity | `make venv` / `make env-check` | Developer machines (not required in CI) |

Current workflows (reference implementations):

- [`.github/workflows/build.yml`](../.github/workflows/build.yml) — PR + `main`: `install-tools` → `build`
- [`.github/workflows/publish.yml`](../.github/workflows/publish.yml) — tags `v*`: `install-tools` → `build` → `upload`

**Artifacts:** wheels under `packages/*/dist/` (gitignored locally; produced in CI).

**Version source of truth:** [`VERSION`](../VERSION) → `make sync` → each `packages/*/pyproject.toml`.

---

## Step 1 — Register this repo in org-ci-standards

In **org-ci-standards**, add or extend a catalog entry for monorepo Python libraries. Suggested metadata:

```yaml
# Example catalog fragment (format depends on your org-ci-standards repo)
repo: org-python-platform
language: python
python_version: "3.12"
package_layout: monorepo  # packages/*/
build_command: make build
publish_command: make upload
version_file: VERSION
workflows:
  verify: build
  release: publish-on-tag
registry: github-packages
```

Document required **secrets** and **permissions** (see Step 3).

---

## Step 2 — Replace inline workflows with reusable jobs

Keep thin workflow files in **this** repo that delegate to org-ci-standards. Adjust `uses:` paths to match your org’s layout.

### Verify (PR / main)

```yaml
# .github/workflows/build.yml (pattern)
name: Build

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  build:
    uses: YOUR_ORG/org-ci-standards/.github/workflows/python-monorepo-build.yml@vX.Y.Z
    with:
      python_version: "3.12"
      working_directory: .
      build_command: make install-tools && make build
    # secrets: inherit   # if your reusable workflow needs none
```

If org-ci-standards exposes smaller composable jobs (setup Python, cache pip, run script), compose them:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_ORG/org-ci-standards/.github/actions/setup-python@vX.Y.Z
        with:
          python-version: "3.12"
      - run: make install-tools && make build
```

### Release (semver tag)

Publishing must stay **tag-gated** and use GitHub Packages credentials from org standards:

```yaml
# .github/workflows/publish.yml (pattern)
name: Publish packages

on:
  push:
    tags: ["v*"]

permissions:
  contents: read
  packages: write

jobs:
  publish:
    uses: YOUR_ORG/org-ci-standards/.github/workflows/python-publish-github-packages.yml@vX.Y.Z
    with:
      python_version: "3.12"
      build_command: make install-tools && make build
      upload_command: make upload
      registry_url: https://upload.pypi.pkg.github.com/YOUR_ORG_OWNER/
    secrets:
      TWINE_PASSWORD: ${{ secrets.GITHUB_TOKEN }}
      # or org-ci-standards may map ORG_PYPI_TOKEN → TWINE_PASSWORD
```

Until reusable workflows exist, the committed [`build.yml`](../.github/workflows/build.yml) and [`publish.yml`](../.github/workflows/publish.yml) in this repo are the reference.

---

## Step 3 — Secrets, permissions, and registry

### GitHub Actions (this repo)

| Variable / secret | Purpose |
|-------------------|---------|
| `GITHUB_TOKEN` (default) | `TWINE_PASSWORD` for `make upload` when registry is GitHub Packages |
| `TWINE_USERNAME` | Set to `__token__` in workflow (see publish.yml) |
| `TWINE_REPOSITORY_URL` | `https://upload.pypi.pkg.github.com/<owner>/` |

Job permissions for publish: `packages: write` (and `contents: read`).

### Consumer applications (install platform packages in CI)

Consumers need the **GitHub Packages index** before `pip install`. Org-ci-standards should provide a shared step or action, for example:

```yaml
- name: Configure GitHub Packages PyPI index
  run: |
    echo "PIP_EXTRA_INDEX_URL=https://__token__:${{ secrets.GITHUB_TOKEN }}@pypi.pkg.github.com/YOUR_ORG_OWNER/simple/" >> "$GITHUB_ENV"
- run: pip install -e ".[dev]"
```

See [CONSUMING.md](CONSUMING.md) and [`pip.conf.example`](../pip.conf.example).

Cross-repo private consumers may need an org secret (PAT with `read:packages`) defined in org-ci-standards.

---

## Step 4 — Optional: org-ai-standards in the same repo

Platform code does not require **org-ai-standards**, but product repos often use both:

- **org-ai-standards** — Cursor rules, AI-SDLC docs, `make check-standards`
- **org-python-platform** — runtime libraries (installed via pip/git)

If you add a `standards/` submodule here:

1. Use HTTPS submodule URL (CI-friendly).
2. Checkout with `submodules: recursive`.
3. Pin profiles appropriate for a library monorepo, e.g. `core,python` (skip product-only overlays).

Release order when both change: push **org-ai-standards** tag first, then bump consumer submodule — same “push upstream before pin” rule as platform packages ([org-ai-standards RELEASE](https://github.com/tusharwagh/org-ai-standards/blob/main/docs/RELEASE.md)).

---

## Step 5 — Release coordination checklist

Use this when cutting a platform version consumed by other repos:

### A. org-python-platform (this repo)

1. Merge to `main`
2. Bump [`VERSION`](../VERSION) and [`CHANGELOG.md`](../CHANGELOG.md)
3. `make sync && make build` locally or rely on CI
4. Tag: `git tag -a vX.Y.Z -m "org-python-platform vX.Y.Z"`
5. **Push** `main` and tags: `git push origin main --tags`
6. Confirm publish workflow succeeded (GitHub Packages)

Details: [PUBLISH.md](PUBLISH.md)

### B. org-ci-standards

1. If reusable workflow inputs changed, tag **org-ci-standards** and update `uses: ...@vX.Y.Z` in this repo
2. Notify teams to bump their workflow pin

### C. Consumer applications

1. Bump git `@vX.Y.Z` or `==X.Y.Z` pins ([CONSUMING.md](CONSUMING.md))
2. Update config adapters if settings changed ([consumer-integration.md](consumer-integration.md))
3. Run CI (with org-standard GitHub Packages auth step)

**Failure mode:** consumer pins `@vX.Y.Z` before the tag exists on GitHub → `not our ref`. Always publish platform **before** consumer bumps.

---

## Step 6 — GitLab CI (if org-ci-standards uses GitLab)

Equivalent include pattern:

```yaml
# .gitlab-ci.yml (pattern)
include:
  - project: YOUR_GROUP/org-ci-standards
    file: /templates/python-monorepo.yml
    ref: vX.Y.Z

variables:
  PYTHON_VERSION: "3.12"

build:
  script:
    - make install-tools
    - make build

publish:
  rules:
    - if: $CI_COMMIT_TAG =~ /^v/
  script:
    - make install-tools
    - make build
    - make upload
  variables:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: $CI_JOB_TOKEN  # or org-provided secret
```

Align token scope and registry URL with your org’s GitLab PyPI/GitHub Packages bridge if applicable.

---

## Step 7 — Quality gates to add via org-ci-standards

This repo’s CI currently **builds** all packages. Org standards may require additional jobs — wire them to local commands when you add them:

| Gate | Suggested command (future) | Notes |
|------|----------------------------|--------|
| Lint | `ruff check packages/` | Dev dep in package `[dev]` extras |
| Test | `pytest packages/` | Add tests per package when present |
| Standards drift | `make check-standards` | Requires org-ai-standards submodule |
| Supply chain | org reusable SBOM / dependabot | Configure at org level |

Keep new gates behind `make` targets so CI and local dev stay aligned.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `not our ref vX.Y.Z` in consumer CI | Tag not pushed | Push platform tag before consumer pin |
| `403` on `make upload` | Missing `packages: write` or wrong token | Fix workflow permissions / org secret mapping |
| `No module named ...` in consumer CI | Missing `PIP_EXTRA_INDEX_URL` | Add org-standard Packages auth step |
| Build OK locally, fails in CI | Different Python version | Use 3.12 on runner |
| litellm build from source | Unpinned resolver pulled sdist | Pin wheels in consumer/`requirements-dev.txt` pattern ([`requirements-dev.txt`](../requirements-dev.txt)) |

---

## Quick links

- [CONSUMING.md](CONSUMING.md) — install options for applications
- [PUBLISH.md](PUBLISH.md) — release checklist
- [consumer-integration.md](consumer-integration.md) — app wiring
- [PLATFORM.md](PLATFORM.md) — package boundaries
- Makefile: `make help`

When **org-ci-standards** documents its reusable workflow names and version tags, add them to Step 2 and the catalog in Step 1 so this guide stays the single integration index for platform CI.
