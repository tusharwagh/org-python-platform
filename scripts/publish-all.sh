#!/usr/bin/env bash
# Publish all package wheels to GitHub Packages (requires TWINE_* env).
set -euo pipefail

scripts/build-all.sh
scripts/upload-all.sh
