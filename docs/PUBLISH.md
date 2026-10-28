# Release and publish checklist

Monorepo version lives in [`VERSION`](../VERSION). All five packages publish at the **same** version.

## Order matters

1. **Push platform packages** (tag + GitHub Packages) **before** consumer repos pin the version.
2. Consumer CI that uses `@vX.Y.Z` git refs fails with `not our ref` if the tag is not on GitHub yet.

## Checklist

### 1. Platform repo (`org-python-platform`)

- [ ] Changes merged to `main`
- [ ] [`VERSION`](../VERSION) bumped (semver)
- [ ] [`CHANGELOG.md`](../CHANGELOG.md) entry added
- [ ] `make sync` — sync version into each `packages/*/pyproject.toml`
- [ ] `make build` — all wheels build cleanly
- [ ] Annotated tag: `git tag -a vX.Y.Z -m "org-python-platform vX.Y.Z"`
- [ ] **Push:** `git push origin main --tags`

Verify remote:

```bash
git ls-remote origin refs/heads/main 'refs/tags/vX.Y.Z'
```

GitHub Actions (`.github/workflows/publish.yml`) publishes all packages to **GitHub Packages** when tag `v*` is pushed.

### 2. Consumer applications

- [ ] Pin git deps to `@vX.Y.Z` **or** bump PyPI version pins (see [CONSUMING.md](CONSUMING.md))
- [ ] Update `.platform-version` if used
- [ ] `pip install -e ".[dev]"` and run tests
- [ ] Push consumer

### 3. Semver

| Bump | When |
|------|------|
| MAJOR | Breaking public API in any package |
| MINOR | New backward-compatible features |
| PATCH | Bug fixes, docs, internal changes |

## Manual publish (fallback)

If CI is unavailable, from repo root with `GITHUB_TOKEN` or PAT (`write:packages`):

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD="$GITHUB_TOKEN"
make publish
```

## Tags on GitHub

`git push origin main` alone does **not** publish tags. Use `git push origin main --tags` or `git push origin vX.Y.Z`.
