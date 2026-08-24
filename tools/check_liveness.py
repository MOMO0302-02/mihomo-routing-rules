"""DoH-based domain liveness check with mandatory controls.

Plain DNS cannot be trusted on machines where a proxy client hijacks UDP 53
with fake-ip (every query answers 198.18.0.x, dead or alive — observed
2026-08-24). DNS-over-HTTPS through the proxy bypasses that. Judgement is by
the DoH Status field: 0 = domain exists, 3 = NXDOMAIN. "Exists but the apex
has no A record" is the normal shape for CDN wildcard domains and is NOT
death (see AGENTS.md, 2026-08-17).

Every batch runs two controls first; if either misbehaves the whole batch is
aborted rather than reporting garbage.

Usage: python tools/check_liveness.py [--proxy http://127.0.0.1:7890] domain [domain ...]
       python tools/check_liveness.py --stdin < domains.txt
Output: TSV of status<TAB>domain, where status is LIVE, NO_APEX_A, or NXDOMAIN.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request

DOH = "https://dns.google/resolve?name={}&type=A"
CONTROL_LIVE = "baidu.com"
CONTROL_DEAD = "this-domain-must-not-exist-4f9c2ab1.com"


def query(domain: str, proxy: str | None) -> dict:
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    opener = urllib.request.build_opener(*handlers)
    with opener.open(DOH.format(domain), timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def classify(answer: dict) -> str:
    status = answer.get("Status")
    if status == 3:
        return "NXDOMAIN"
    if status != 0:
        return f"DNS_STATUS_{status}"
    return "LIVE" if answer.get("Answer") else "NO_APEX_A"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("domains", nargs="*")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--proxy", default=None)
    args = parser.parse_args()

    domains = list(args.domains)
    if args.stdin:
        domains += [line.strip() for line in sys.stdin if line.strip()]
    if not domains:
        parser.error("no domains given")

    live_control = classify(query(CONTROL_LIVE, args.proxy))
    dead_control = classify(query(CONTROL_DEAD, args.proxy))
    if live_control != "LIVE" or dead_control != "NXDOMAIN":
        print(
            f"ABORT: controls failed ({CONTROL_LIVE}={live_control}, "
            f"fake={dead_control}) - results would be untrustworthy",
            file=sys.stderr,
        )
        return 1

    exit_code = 0
    for domain in domains:
        try:
            status = classify(query(domain, args.proxy))
        except Exception as exc:  # noqa: BLE001 - network errors reported per-domain
            status = f"ERR_{type(exc).__name__}"
            exit_code = 1
        print(f"{status}\t{domain}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
