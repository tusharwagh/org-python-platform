#!/usr/bin/env bash
# Upload built wheels/sdists to GitHub Packages (requires TWINE_* env).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

: "${TWINE_USERNAME:?Set TWINE_USERNAME (__token__)}"
: "${TWINE_PASSWORD:?Set TWINE_PASSWORD (GITHUB_TOKEN or PAT with write:packages)}"

REPOSITORY_URL="${TWINE_REPOSITORY_URL:-https://upload.pypi.pkg.github.com/tusharwagh/}"

python3 -m pip install -q twine

for pkg in "$ROOT"/packages/*/; do
  name="$(basename "$pkg")"
  echo "==> publishing $name"
  python3 -m twine upload --repository-url "$REPOSITORY_URL" "$pkg"/dist/* --skip-existing
done

echo "publish complete"
