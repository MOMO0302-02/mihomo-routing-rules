"""Print the CHANGELOG.md section for one version (used by the Release workflow).

Usage: python tools/changelog_section.py v2026.08.24.4GoogleAITK
Falls back to a pointer at CHANGELOG.md when the section is missing, so the
Release job never fails on a docs gap.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: changelog_section.py <tag>", file=sys.stderr)
        return 2
    tag = sys.argv[1]
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(
        rf"^## {re.escape(tag)}\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL
    )
    if match:
        print(f"## {tag}\n{match.group(1).rstrip()}")
    else:
        print(
            f"版本 {tag}。变更明细见 "
            "[CHANGELOG.md](https://github.com/MOMO0302-02/mihomo-routing-rules/blob/main/CHANGELOG.md)。"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
