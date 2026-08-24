"""Load every rule in a real Mihomo core and fail on any parse error.

validate_rules.py checks structure and semantics, but only the core itself
proves a rule parses. `mihomo -t` is NOT enough: it skips rule-provider
payloads entirely (verified by negative control on 2026-08-17). This script
starts the core with file providers, waits for the initial load, then scans
the log for errors and warnings.

Usage: python tools/coretest.py --binary ./mihomo [--seconds 8]
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READY_MARKER = "Initial configuration complete"


def build_config(workdir: Path) -> int:
    order = re.findall(
        r"^  - RULE-SET,([a-z0-9_]+),(\S+)$",
        (ROOT / "examples" / "rules.yaml").read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    if not order:
        raise SystemExit("examples/rules.yaml has no RULE-SET lines")
    ruleset = workdir / "ruleset"
    ruleset.mkdir(parents=True)
    for name, _ in order:
        shutil.copy(ROOT / "rules" / f"{name}.yaml", ruleset / f"{name}.yaml")
    policies = sorted({policy for _, policy in order if policy != "DIRECT"})
    lines = [
        "mixed-port: 17890",
        "mode: rule",
        "log-level: info",
        "proxies:",
        "  - {name: dummy, type: socks5, server: 127.0.0.1, port: 1080}",
        "proxy-groups:",
    ]
    lines += [
        f"  - {{name: {policy}, type: select, proxies: [dummy, DIRECT]}}"
        for policy in policies
    ]
    lines.append("rule-providers:")
    for name, _ in order:
        lines += [
            f"  {name}:",
            "    type: file",
            "    behavior: classical",
            "    format: yaml",
            f"    path: ./ruleset/{name}.yaml",
        ]
    lines.append("rules:")
    lines += [f"  - RULE-SET,{name},{policy}" for name, policy in order]
    lines.append("  - MATCH,DIRECT")
    (workdir / "config.yaml").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    return len(order)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--seconds", type=int, default=8)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        providers = build_config(workdir)
        try:
            proc = subprocess.run(
                [args.binary, "-f", str(workdir / "config.yaml"), "-d", str(workdir)],
                capture_output=True,
                text=True,
                timeout=args.seconds,
            )
            output = (proc.stdout or "") + (proc.stderr or "")
        except subprocess.TimeoutExpired as exc:
            # The core runs forever; the timeout firing means it started fine.
            output = "".join(
                part.decode("utf-8", "replace") if isinstance(part, bytes) else part
                for part in ((exc.stdout or ""), (exc.stderr or ""))
            )

    problems = [
        line
        for line in output.splitlines()
        if re.search(r"level=(error|warning|fatal)", line)
        # The dummy proxy is unreachable by design; ignore dial failures to it.
        and "127.0.0.1:1080" not in line
    ]
    if READY_MARKER not in output:
        print("FAIL: core never reached initial-configuration-complete", file=sys.stderr)
        print(output[-3000:], file=sys.stderr)
        return 1
    if problems:
        print(f"FAIL: {len(problems)} error/warning lines:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"ok: core loaded {providers} providers with no errors or warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
