#!/usr/bin/env bash
# Build wheels/sdists for all packages in the monorepo.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/sync-versions.py

python3 -m pip install -q build

for pkg in "$ROOT"/packages/*/; do
  name="$(basename "$pkg")"
  echo "==> building $name"
  rm -rf "$pkg/dist"
  python3 -m build "$pkg" -q
done

echo "all packages built under packages/*/dist/"
