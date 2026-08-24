"""Probe every DOMAIN/DOMAIN-SUFFIX target for cross-site redirects.

Domain migrations (rebrands, acquisitions, new unified domains) silently
break rules without any error. This probe sends one HEAD per domain, keeps
only redirects that cross a registrable-domain boundary (www./path hops are
noise), then answers two questions per redirect target: is it covered by any
rule, and does that rule map to the same suggested policy? Both must hold
for the redirect to be healthy.

Run it before every major version (discipline recorded in AGENTS.md).

Usage: python tools/probe_migration.py [--proxy http://127.0.0.1:7890] [--workers 10]
Output: healthy cross-site redirects are listed for reference; uncovered or
policy-switching targets are flagged. Exit 0 always - findings need human
judgement (marketing-page targets are deliberately not added).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TWO_LEVEL = {"com.cn", "net.cn", "org.cn", "gov.cn", "co.uk", "com.hk", "com.tw", "co.jp"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # noqa: D102
        return None


def registrable(host: str) -> str:
    parts = host.lower().rstrip(".").split(".")
    if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_LEVEL:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def load_rules() -> tuple[dict[str, list[str]], dict[str, str]]:
    payloads = {
        path.stem: [
            json.loads(line[4:])
            for line in path.read_text(encoding="utf-8").splitlines()[1:]
            if line.strip()
        ]
        for path in sorted((ROOT / "rules").glob("*.yaml"))
    }
    order = dict(
        re.findall(
            r"^  - RULE-SET,([a-z0-9_]+),(\S+)$",
            (ROOT / "examples" / "rules.yaml").read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        )
    )
    return payloads, order


def first_match(host: str, payloads: dict[str, list[str]]) -> str | None:
    for category, rules in payloads.items():
        for rule in rules:
            kind, _, target = rule.partition(",")
            if (
                (kind == "DOMAIN" and host == target)
                or (kind == "DOMAIN-SUFFIX" and (host == target or host.endswith("." + target)))
                or (kind == "DOMAIN-KEYWORD" and target in host)
            ):
                return category
    return None


def probe(domain: str, proxy: str | None) -> tuple[str, str]:
    handlers: list[urllib.request.BaseHandler] = [NoRedirect()]
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    opener = urllib.request.build_opener(*handlers)
    request = urllib.request.Request(f"https://{domain}/", method="HEAD")
    try:
        with opener.open(request, timeout=12) as response:
            return str(response.status), ""
    except urllib.error.HTTPError as exc:
        return str(exc.code), exc.headers.get("Location", "") or ""
    except Exception:  # noqa: BLE001 - unreachable hosts are expected
        return "000", ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy", default="http://127.0.0.1:7890")
    parser.add_argument("--workers", type=int, default=10)
    args = parser.parse_args()

    payloads, order = load_rules()
    domains = sorted(
        {
            rule.partition(",")[2]
            for rules in payloads.values()
            for rule in rules
            if rule.startswith(("DOMAIN,", "DOMAIN-SUFFIX,"))
        }
    )
    domain_category = {
        rule.partition(",")[2]: category
        for category, rules in payloads.items()
        for rule in rules
        if rule.startswith(("DOMAIN,", "DOMAIN-SUFFIX,"))
    }

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = dict(
            zip(domains, pool.map(lambda d: probe(d, args.proxy or None), domains))
        )

    healthy, flagged = [], []
    for domain, (code, location) in sorted(results.items()):
        if not location:
            continue
        match = re.match(r"https?://([^/:]+)", location)
        if not match or registrable(match.group(1)) == registrable(domain):
            continue
        target = match.group(1).lower()
        source_category = domain_category.get(domain, "?")
        source_policy = order.get(source_category, "?")
        target_category = first_match(target, payloads)
        if target_category is None:
            flagged.append(f"[未覆盖] {domain} [{source_category}/{source_policy}] -> {target}")
        elif order.get(target_category) != source_policy:
            flagged.append(
                f"[换策略组] {domain} [{source_category}/{source_policy}] -> "
                f"{target} [{target_category}/{order.get(target_category)}]"
            )
        else:
            healthy.append(f"{domain} -> {target} [{target_category}]")

    print(f"probed {len(domains)} domains; cross-site redirects: "
          f"{len(healthy) + len(flagged)} ({len(flagged)} flagged)")
    if flagged:
        print("\n== 需人工甄别（营销页跳转不收，功能域必收）==")
        for line in flagged:
            print(f"  {line}")
    if healthy:
        print("\n== 健康跳转（新旧域名均已覆盖且同策略）==")
        for line in healthy:
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
