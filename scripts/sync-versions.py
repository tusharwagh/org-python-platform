#!/usr/bin/env python3
"""Sync VERSION file into each package pyproject.toml."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
PACKAGES_DIR = ROOT / "packages"

VERSION_PATTERN = re.compile(r'^version = ".*"$', re.MULTILINE)


def main() -> int:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not version:
        print("VERSION file is empty", file=sys.stderr)
        return 1

    updated = 0
    for pyproject in sorted(PACKAGES_DIR.glob("*/pyproject.toml")):
        text = pyproject.read_text(encoding="utf-8")
        new_text, count = VERSION_PATTERN.subn(f'version = "{version}"', text, count=1)
        if count != 1:
            print(f"skip (no version field): {pyproject}", file=sys.stderr)
            continue
        if new_text != text:
            pyproject.write_text(new_text, encoding="utf-8")
            updated += 1
            print(f"updated {pyproject.relative_to(ROOT)} -> {version}")

    print(f"done: {updated} package(s) at v{version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
