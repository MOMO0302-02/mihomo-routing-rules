"""Report official-geosite AI domains that this library does not match at all.

The official MetaCubeX geosite list answers "is this an AI site"; this
library also answers "which exit should it take", so the two are
complementary, not substitutes (AGENTS.md, 2026-08-24). New entries landing
in the official list are still the cheapest signal that a new AI product
exists, which is why the monthly health check runs this gap report.

Usage: python tools/geosite_gap.py [--list category-ai-!cn] [--proxy http://...]
Exit 0 always - uncovered entries need human triage, not an automatic fail.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/{}.list"
REJECTED_PATH = ROOT / "tools" / "geosite_rejected.txt"


def load_rejected() -> set[str]:
    if not REJECTED_PATH.exists():
        return set()
    return {
        line.strip()
        for line in REJECTED_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def load_library() -> tuple[set[str], set[str], set[str]]:
    suffixes, exacts, keywords = set(), set(), set()
    for path in sorted((ROOT / "rules").glob("*.yaml")):
        for line in path.read_text(encoding="utf-8").splitlines()[1:]:
            if not line.strip():
                continue
            kind, _, value = json.loads(line[4:]).partition(",")
            if kind == "DOMAIN-SUFFIX":
                suffixes.add(value)
            elif kind == "DOMAIN":
                exacts.add(value)
            elif kind == "DOMAIN-KEYWORD":
                keywords.add(value)
    return suffixes, exacts, keywords


def fetch_list(name: str, proxy: str | None) -> list[tuple[str, str]]:
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    opener = urllib.request.build_opener(*handlers)
    with opener.open(SOURCE.format(name), timeout=30) as response:
        text = response.read().decode("utf-8")
    entries = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("+."):
            entries.append(("suffix", line[2:]))
        elif re.fullmatch(r"[a-z0-9.-]+", line):
            entries.append(("domain", line))
        # regexp:/full:/other prefixes are rare in these lists; skip silently.
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", default="category-ai-!cn", dest="list_name")
    parser.add_argument("--proxy", default=None)
    args = parser.parse_args()

    suffixes, exacts, keywords = load_library()

    def covered(kind: str, value: str) -> bool:
        if value in exacts:
            return True
        if any(value == s or value.endswith("." + s) for s in suffixes):
            return True
        if any(k in value for k in keywords):
            return True
        return False

    rejected = load_rejected()
    entries = fetch_list(args.list_name, args.proxy)
    missing, skipped = [], 0
    for kind, value in entries:
        if covered(kind, value):
            continue
        if value in rejected:
            skipped += 1
            continue
        missing.append((kind, value))
    print(
        f"official {args.list_name}: {len(entries)} entries, "
        f"{len(missing)} uncovered ({skipped} on the rejected list)"
    )
    for kind, value in missing:
        print(f"  {kind}\t{value}")
    print(f"TOTAL uncovered: {len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
