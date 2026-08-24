"""Watch a running Mihomo core and collect hosts that fall to the MATCH rule.

The single best signal that this rule set has a gap is a real connection
landing on the config's fallback (rule "Match") when its host obviously
belongs to some category - that is exactly how the Datadog regional-intake
leak was found by eye in the client's connections panel. This tool automates
that eye: it polls the core's external controller, aggregates fallback
hosts, then checks each against this repository's rules and prints the ones
no rule would catch - ready-made triage candidates.

Requires the client to expose the external controller (Clash Party:
设置 -> 外部控制, default http://127.0.0.1:9090).

Usage:
  python tools/watch_fallback.py                          # watch until Ctrl+C
  python tools/watch_fallback.py --duration 300           # watch 5 minutes
  python tools/watch_fallback.py --controller http://127.0.0.1:9090 --secret xxx
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FALLBACK_RULES = {"Match", "MATCH"}


def load_rules() -> dict[str, list[str]]:
    return {
        path.stem: [
            json.loads(line[4:])
            for line in path.read_text(encoding="utf-8").splitlines()[1:]
            if line.strip()
        ]
        for path in sorted((ROOT / "rules").glob("*.yaml"))
    }


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


def fetch_connections(controller: str, secret: str | None) -> list[dict]:
    request = urllib.request.Request(f"{controller.rstrip('/')}/connections")
    if secret:
        request.add_header("Authorization", f"Bearer {secret}")
    # The controller lives on localhost; never send this through a proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8")).get("connections") or []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controller", default="http://127.0.0.1:9090")
    parser.add_argument("--secret", default=None)
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--duration", type=float, default=0, help="秒；0 = 直到 Ctrl+C")
    args = parser.parse_args()

    payloads = load_rules()
    fallback_hits: collections.Counter[str] = collections.Counter()
    seen_total: set[str] = set()
    started = time.monotonic()

    print(f"watching {args.controller} 每 {args.interval}s 采样，Ctrl+C 结束并出报告 ...")
    try:
        while True:
            try:
                for conn in fetch_connections(args.controller, args.secret):
                    meta = conn.get("metadata") or {}
                    host = (meta.get("host") or "").lower().rstrip(".")
                    if not host or not re.fullmatch(r"[a-z0-9.-]+", host):
                        continue
                    seen_total.add(host)
                    if conn.get("rule") in FALLBACK_RULES:
                        fallback_hits[host] += 1
            except Exception as exc:  # noqa: BLE001 - keep watching through hiccups
                print(f"  (采样失败: {type(exc).__name__}: {exc})")
            if args.duration and time.monotonic() - started >= args.duration:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass

    print(f"\n观察到 {len(seen_total)} 个主机，其中 {len(fallback_hits)} 个落到兜底 Match")
    uncovered = [
        (count, host)
        for host, count in fallback_hits.items()
        if first_match(host, payloads) is None
    ]
    covered = [
        (count, host, first_match(host, payloads))
        for host, count in fallback_hits.items()
        if first_match(host, payloads) is not None
    ]
    if uncovered:
        print("\n== 本库无任何规则覆盖（收录候选，按出现次数排序）==")
        for count, host in sorted(uncovered, reverse=True):
            print(f"  {count:4d}  {host}")
    if covered:
        print("\n== 本库有规则但客户端仍走了兜底（配置未引用对应分类？）==")
        for count, host, category in sorted(covered, reverse=True):
            print(f"  {count:4d}  {host}  [{category}]")
    if not fallback_hits:
        print("兜底干净——观察期内没有任何连接漏进 Match。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
