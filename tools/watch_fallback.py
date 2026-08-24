"""Watch a running Mihomo core and collect hosts that fall to the MATCH rule.

The single best signal that this rule set has a gap is a real connection
landing on the config's fallback (rule "Match") when its host obviously
belongs to some category - that is exactly how the Datadog regional-intake
leak was found by eye in the client's connections panel. This tool automates
that eye: it polls the core's external controller, aggregates fallback
hosts, then checks each against this repository's rules and prints the ones
no rule would catch - ready-made triage candidates.

Works out of the box with Clash Party / Mihomo Party on Windows: those
clients drive the core over a named pipe instead of a TCP controller, and
this tool auto-discovers that pipe (no settings change needed). A TCP
external controller (--controller http://127.0.0.1:9090 [--secret xxx])
works too, for clients that expose one.

Usage:
  python tools/watch_fallback.py                          # watch until Ctrl+C
  python tools/watch_fallback.py --duration 300           # watch 5 minutes
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FALLBACK_RULES = {"Match", "MATCH"}
PIPE_DIR = "//./pipe/"


def discover_pipe() -> str | None:
    """Find the Mihomo Party admin pipe (Windows only; name carries a PID)."""
    try:
        names = os.listdir(PIPE_DIR)
    except OSError:
        return None
    for name in names:
        if "mihomo-admin" in name:
            return PIPE_DIR + name.replace("\\", "/")
    return None


def http_over_pipe(pipe_path: str, request_path: str) -> bytes:
    """One HTTP/1.1 request over a named pipe; returns the body bytes."""
    with open(pipe_path, "r+b", buffering=0) as pipe:
        pipe.write(
            f"GET {request_path} HTTP/1.1\r\nHost: mihomo\r\n"
            "Connection: close\r\n\r\n".encode("ascii")
        )
        raw = b""
        try:
            while True:
                chunk = pipe.read(65536)
                if not chunk:
                    break
                raw += chunk
        except OSError:
            pass  # server closing its end reads as an error on some systems
    header, _, body = raw.partition(b"\r\n\r\n")
    if b"chunked" in header.lower():
        decoded = b""
        while body:
            size_line, _, body = body.partition(b"\r\n")
            size = int(size_line.split(b";")[0], 16)
            if size == 0:
                break
            decoded += body[:size]
            body = body[size + 2:]
        return decoded
    return body


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


def fetch_connections(controller: str, secret: str | None, pipe: str | None) -> list[dict]:
    if pipe:
        body = http_over_pipe(pipe, "/connections")
        return json.loads(body.decode("utf-8")).get("connections") or []
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
    parser.add_argument("--no-pipe", action="store_true", help="禁用命名管道自动发现，只用 --controller")
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--duration", type=float, default=0, help="秒；0 = 直到 Ctrl+C")
    args = parser.parse_args()

    pipe = None if args.no_pipe else discover_pipe()
    if pipe:
        print(f"已发现客户端命名管道，直接接入：{pipe}")

    payloads = load_rules()
    fallback_hits: collections.Counter[str] = collections.Counter()
    seen_total: set[str] = set()
    started = time.monotonic()

    source = pipe or args.controller
    print(f"watching {source} 每 {args.interval}s 采样，Ctrl+C 结束并出报告 ...")
    try:
        while True:
            try:
                for conn in fetch_connections(args.controller, args.secret, pipe):
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
