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
PROVIDERS_PATH = ROOT / "examples" / "rule-providers.yaml"
RULE_ORDER_PATH = ROOT / "examples" / "rules.yaml"
RULE_INDEX_PATH = ROOT / "RULES.md"
README_PATH = ROOT / "README.md"
RAW_PREFIX = (
    "https://raw.githubusercontent.com/MOMO0302-02/"
    "mihomo-routing-rules/release/rules/"
)
CDN_PREFIX = (
    "https://cdn.jsdelivr.net/gh/MOMO0302-02/"
    "mihomo-routing-rules@release/rules/"
)
DEVELOPMENT_RULE_URL = (
    "https://raw.githubusercontent.com/MOMO0302-02/"
    "mihomo-routing-rules/main/rules/"
)
ALLOWED_KINDS = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "PROCESS-NAME"}
FORBIDDEN_FILES = {"airport_site_custom.yaml", "recmata_service_direct_custom.yaml"}
ALLOWED_OVERLAP_GROUPS = {
    frozenset({"ai_custom", "openai_login_custom"}),
}
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
    suffix_targets = {
        rule.partition(",")[2]
        for rule in payload
        if rule.startswith("DOMAIN-SUFFIX,")
    }
    redundant_domains = [
        rule
        for rule in payload
        if rule.startswith("DOMAIN,")
        and any(
            rule.partition(",")[2] == suffix
            or rule.partition(",")[2].endswith(f".{suffix}")
            for suffix in suffix_targets
        )
    ]
    if redundant_domains:
        raise ValueError(
            f"{path.name}: DOMAIN rules are already covered by broader "
            f"DOMAIN-SUFFIX rules: {redundant_domains}"
        )
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
    privacy = manifest.get("privacy")
    if not isinstance(privacy, dict) or any(privacy.get(key) is not False for key in (
        "contains_proxy_nodes",
        "contains_subscription_urls",
        "contains_credentials",
    )):
        errors.append("manifest privacy flags must explicitly be false")
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
    rule_owners: dict[str, set[str]] = {}
    for filename in sorted(actual_files):
        path = RULES_DIR / filename
        try:
            payload = read_payload(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(str(exc))
            continue
        total += len(payload)
        for rule in payload:
            rule_owners.setdefault(rule, set()).add(path.stem)
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
    for rule, owners in sorted(rule_owners.items()):
        if len(owners) > 1 and frozenset(owners) not in ALLOWED_OVERLAP_GROUPS:
            errors.append(
                f"unexpected cross-category duplicate: {rule} in {sorted(owners)}"
            )

    public_documents: dict[Path, str] = {}
    for path in (
        ALL_IN_ONE_PATH,
        PROVIDERS_PATH,
        RULE_ORDER_PATH,
        RULE_INDEX_PATH,
        README_PATH,
    ):
        try:
            public_documents[path] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)} read error: {exc}")
            public_documents[path] = ""

    all_in_one = public_documents[ALL_IN_ONE_PATH]
    providers = public_documents[PROVIDERS_PATH]
    rule_order = public_documents[RULE_ORDER_PATH]
    rule_index = public_documents[RULE_INDEX_PATH]
    readme = public_documents[README_PATH]

    for path, text in public_documents.items():
        if DEVELOPMENT_RULE_URL in text:
            errors.append(
                f"{path.relative_to(ROOT)} references the development branch instead of release"
            )

    for filename in sorted(actual_files):
        name = Path(filename).stem
        entry = files.get(filename) or {}
        stable_url = f"{RAW_PREFIX}{filename}"
        cdn_url = f"{CDN_PREFIX}{filename}"
        if f"  {name}:" not in all_in_one:
            errors.append(f"all-in-one example missing provider: {name}")
        if f"  - RULE-SET,{name}," not in all_in_one:
            errors.append(f"all-in-one example missing rule: {name}")
        if stable_url not in all_in_one:
            errors.append(f"all-in-one example missing stable URL: {name}")
        if f"{name}:" not in providers or stable_url not in providers:
            errors.append(f"provider example missing stable provider: {name}")
        if f"  - RULE-SET,{name}," not in rule_order:
            errors.append(f"rule-order example missing rule: {name}")
        if f"`{name}` | {entry.get('count')} |" not in rule_index:
            errors.append(f"rule index missing provider/count: {name}")
        if stable_url not in rule_index:
            errors.append(f"rule index missing Raw URL: {name}")
        if cdn_url not in rule_index:
            errors.append(f"rule index missing CDN URL: {name}")
    for forbidden_name in FORBIDDEN_FILES:
        forbidden_stem = Path(forbidden_name).stem
        for path, text in public_documents.items():
            if forbidden_stem in text and path not in {README_PATH}:
                errors.append(
                    f"{path.relative_to(ROOT)} contains private provider: {forbidden_name}"
                )

    if "`main`" not in readme or "`release`" not in readme:
        errors.append("README must explain main and release branch roles")
    if RAW_PREFIX not in readme or CDN_PREFIX not in readme:
        errors.append("README must document Raw and CDN stable URL formats")

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
