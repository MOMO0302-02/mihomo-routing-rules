from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "rules"
MANIFEST_PATH = ROOT / "manifest.json"
ALL_IN_ONE_PATH = ROOT / "examples" / "all-in-one.yaml"
ALLOWED_KINDS = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "PROCESS-NAME"}
FORBIDDEN_FILES = {"airport_site_custom.yaml", "recmata_service_direct_custom.yaml"}
SENSITIVE_PATTERNS = {
    "proxy URI": re.compile(r"(?i)\b(?:vless|vmess|trojan|ss|hysteria2?)://"),
    "UUID": re.compile(
        r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
        r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
    ),
    "credential assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]"
    ),
    "GitHub token": re.compile(r"\b(?:gh[opsu]_|github_pat_)[A-Za-z0-9_]+\b"),
    "subscription URL": re.compile(r"(?i)https?://[^\s]+/(?:api/)?v1/(?:client/)?subscribe"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_payload(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "payload:":
        raise ValueError(f"{path.name}: first line must be payload:")
    payload: list[str] = []
    for line_number, line in enumerate(lines[1:], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith("  - "):
            raise ValueError(f"{path.name}:{line_number}: invalid payload indentation")
        try:
            value = json.loads(line[4:])
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_number}: rule must be JSON quoted") from exc
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{path.name}:{line_number}: empty rule")
        kind, separator, target = value.partition(",")
        if kind not in ALLOWED_KINDS or not separator or not target.strip():
            raise ValueError(f"{path.name}:{line_number}: unsupported classical rule")
        payload.append(value)
    if not payload:
        raise ValueError(f"{path.name}: payload is empty")
    if len(payload) != len(set(payload)):
        raise ValueError(f"{path.name}: duplicate rules detected")
    return payload


def main() -> int:
    errors: list[str] = []
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"manifest error: {exc}", file=sys.stderr)
        return 1

    if manifest.get("schema") != 1:
        errors.append("manifest schema must be 1")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        errors.append("manifest files must be a non-empty object")
        files = {}

    actual_files = {path.name for path in RULES_DIR.glob("*.yaml")}
    manifest_files = set(files)
    if actual_files != manifest_files:
        errors.append(
            f"manifest/file set mismatch: missing={sorted(actual_files - manifest_files)}, "
            f"stale={sorted(manifest_files - actual_files)}"
        )
    forbidden = actual_files & FORBIDDEN_FILES
    if forbidden:
        errors.append(f"private rule files are forbidden: {sorted(forbidden)}")

    total = 0
    for filename in sorted(actual_files):
        path = RULES_DIR / filename
        try:
            payload = read_payload(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(str(exc))
            continue
        total += len(payload)
        entry = files.get(filename) or {}
        if entry.get("count") != len(payload):
            errors.append(f"{filename}: manifest count mismatch")
        if entry.get("sha256") != sha256(path):
            errors.append(f"{filename}: manifest SHA-256 mismatch")
        text = path.read_text(encoding="utf-8")
        for label, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{filename}: sensitive pattern detected ({label})")

    if manifest.get("total_rules") != total:
        errors.append("manifest total_rules mismatch")
    if manifest.get("public_categories") != len(actual_files):
        errors.append("manifest public_categories mismatch")

    try:
        all_in_one = ALL_IN_ONE_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"all-in-one example error: {exc}")
        all_in_one = ""
    for filename in sorted(actual_files):
        name = Path(filename).stem
        if f"  {name}:" not in all_in_one:
            errors.append(f"all-in-one example missing provider: {name}")
        if f"  - RULE-SET,{name}," not in all_in_one:
            errors.append(f"all-in-one example missing rule: {name}")
    for forbidden_name in FORBIDDEN_FILES:
        if Path(forbidden_name).stem in all_in_one:
            errors.append(f"all-in-one example contains private provider: {forbidden_name}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"ok: {len(actual_files)} public categories, {total} rules, "
        "manifest and sensitive-data checks passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
