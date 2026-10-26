#!/usr/bin/env python3
"""
verify_gcp_hygiene.py - Audits repository for GCP security, Cloud Run hygiene,
and container best practices.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

SERVICE_ACCOUNT_KEY_PATTERN = re.compile(r'"type"\s*:\s*"service_account"')
HARDCODED_GCP_PROJECT = re.compile(r'\bprojects/(?:\d{10,14}|[a-z][a-z0-9-]{5,28})\b')
ROOT_USER_PATTERN = re.compile(r'^\s*USER\s+(?:root|0)\b', re.IGNORECASE)
NON_ROOT_USER_PATTERN = re.compile(r'^\s*USER\s+(?!(?:root|0)\b)\w+', re.IGNORECASE)
HEALTHZ_PROBE_PATTERN = re.compile(r'/(?:healthz|health|status)\b')


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_gcp_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if is_test_file(file_path) or "verify_gcp_hygiene" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    # 1. Exposed Service Account Key File
    if file_path.endswith(".json") and SERVICE_ACCOUNT_KEY_PATTERN.search(content):
        violations.append({
            "file": file_path,
            "line": 1,
            "rule": "GCP-EXPOSED-SERVICE-ACCOUNT-KEY",
            "message": "Raw GCP Service Account private key JSON detected. Use Workload Identity."
        })

    # 2. Dockerfile non-root check
    base_name = os.path.basename(file_path).lower()
    if "dockerfile" in base_name:
        lines = content.splitlines()
        has_non_root = any(NON_ROOT_USER_PATTERN.search(line) for line in lines)
        has_root = any(ROOT_USER_PATTERN.search(line) for line in lines)
        if has_root or not has_non_root:
            violations.append({
                "file": file_path,
                "line": 1,
                "rule": "GCP-CONTAINER-ROOT-USER",
                "message": "Cloud Run container must specify a non-root user (e.g., USER 10001)."
            })

    # 3. Hardcoded GCP project IDs in source
    for idx, line in enumerate(content.splitlines(), start=1):
        if HARDCODED_GCP_PROJECT.search(line) and not line.strip().startswith("//") and not line.strip().startswith("#"):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "GCP-HARDCODED-PROJECT-ID",
                "message": "Hardcoded GCP project identifier detected. Read from process.env or metadata server.",
                "snippet": line.strip()[:80]
            })

    return violations


def scan_gcp_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    has_server_file = False
    has_health_probe = False

    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in {".py", ".ts", ".js", ".json", ".yaml", ".yml"} or "dockerfile" in f.lower():
                violations.extend(audit_gcp_file(fp))

            if f in {"server.ts", "server.js", "app.py", "main.py", "index.ts"}:
                has_server_file = True
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as sf:
                        if HEALTHZ_PROBE_PATTERN.search(sf.read()):
                            has_health_probe = True
                except Exception:
                    pass

    if has_server_file and not has_health_probe and not is_test_file(target_path):
        violations.append({
            "file": target_path,
            "line": 1,
            "rule": "GCP-MISSING-HEALTH-CHECK",
            "message": "Cloud Run service entrypoint missing /healthz or /status liveness probe."
        })

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit GCP Cloud Run and architecture hygiene.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_gcp_file(target)
    else:
        violations = scan_gcp_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== GCP Architecture Hygiene Audit: {target} ===")
        if not violations:
            print("[PASS] GCP architecture hygiene verified. Zero credential leaks or container defects.")
        else:
            print(f"[FAIL] Found {len(violations)} GCP hygiene violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
