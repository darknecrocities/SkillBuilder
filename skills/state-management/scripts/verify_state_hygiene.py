#!/usr/bin/env python3
"""
verify_state_hygiene.py - Audits React/TypeScript state management for boolean explosions,
raw query keys, and un-memoized store subscriptions.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

UNMEMOIZED_STORE_PATTERN = re.compile(r'const\s+(?:\{[^}]+\}|\w+)\s*=\s*use[A-Z]\w*Store\s*\(\s*\);')
RAW_STRING_QUERY_KEY_PATTERN = re.compile(r'useQuery\s*\(\s*(?:\{[^}]*queryKey\s*:\s*["\'][^"\']+["\']|["\'][^"\']+["\'])')
BOOLEAN_FLAG_NAMES = {"isloading", "iserror", "issuccess", "isfetching", "isempty", "haserror", "issubmitting"}


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_state_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if is_test_file(file_path) or "verify_state_hygiene" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    lines = content.splitlines()
    detected_boolean_flags = set()

    for idx, line in enumerate(lines, start=1):
        # 1. Un-memoized root store subscription
        if UNMEMOIZED_STORE_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "STATE-UNMEMOIZED-STORE-SUBSCRIPTION",
                "message": "Direct un-memoized store subscription detected. Pass a granular selector callback: useStore(s => s.item).",
                "snippet": line.strip()[:80]
            })

        # 2. Raw string query key in TanStack Query
        if RAW_STRING_QUERY_KEY_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "STATE-RAW-STRING-QUERY-KEY",
                "message": "Raw string query key detected in useQuery. Use query key array or a Query Key Factory.",
                "snippet": line.strip()[:80]
            })

        # Check for boolean explosion flags
        if "useState" in line:
            for flag in BOOLEAN_FLAG_NAMES:
                if re.search(rf'\b{flag}\b', line, re.IGNORECASE):
                    detected_boolean_flags.add(flag)

    # 3. Flag boolean explosion if 3 or more async state booleans are declared
    if len(detected_boolean_flags) >= 3:
        violations.append({
            "file": file_path,
            "line": 1,
            "rule": "STATE-BOOLEAN-EXPLOSION",
            "message": f"Boolean explosion detected ({len(detected_boolean_flags)} flags: {', '.join(sorted(detected_boolean_flags))}). Replace with a state machine enum ('idle' | 'loading' | 'success' | 'error')."
        })

    return violations


def scan_state_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            if f.endswith((".ts", ".tsx", ".js", ".jsx")):
                violations.extend(audit_state_file(fp))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit state management hygiene.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_state_file(target)
    else:
        violations = scan_state_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== State Management Hygiene Audit: {target} ===")
        if not violations:
            print("[PASS] State management hygiene verified. Clean selectors and deterministic state flow.")
        else:
            print(f"[FAIL] Found {len(violations)} state management violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
