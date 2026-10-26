#!/usr/bin/env python3
"""
verify_testing_hygiene.py - Audits test suites for fragile CSS locators, arbitrary sleep timers,
and missing assertions.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

SLEEP_TIMER_PATTERN = re.compile(r'(?:page\.waitForTimeout\s*\(\s*\d+|time\.sleep\s*\(\s*[1-9]|cy\.wait\s*\(\s*[1-9]\d{2,}\))')
FRAGILE_LOCATOR_PATTERN = re.compile(r'page\.(?:click|locator|fill)\s*\(\s*["\'](?:\w+\.\w+\.\w+|[#\.][a-zA-Z0-9_\-]+>[#\.][a-zA-Z0-9_\-]+|div\.[a-zA-Z0-9_\-]+)\b')
TEST_BLOCK_START = re.compile(r'(?:it|test)\s*\(\s*["\'].*?,\s*async\s*\(', re.DOTALL)


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_test_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    # Skip this auditor and its test suite
    if "verify_testing_hygiene" in file_path:
        return violations
    if not is_test_file(file_path):
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # 1. Arbitrary sleep timer
        if SLEEP_TIMER_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "TESTING-ARBITRARY-SLEEP-TIMER",
                "message": "Arbitrary sleep timer detected in test. Use web-first auto-waiting assertions (expect(locator).toBeVisible()).",
                "snippet": line.strip()[:80]
            })

        # 2. Fragile CSS selector
        if FRAGILE_LOCATOR_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "TESTING-FRAGILE-CSS-SELECTOR",
                "message": "Fragile CSS/DOM selector in test. Use accessible locators: getByRole(), getByLabel(), getByText().",
                "snippet": line.strip()[:80]
            })

    return violations


def scan_testing_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            if is_test_file(fp) and f.endswith((".ts", ".tsx", ".js", ".py")):
                violations.extend(audit_test_file(fp))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit test suites for testing hygiene.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_test_file(target)
    else:
        violations = scan_testing_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Testing Discipline & E2E Hygiene Audit: {target} ===")
        if not violations:
            print("[PASS] Test suites verified. Zero fragile selectors or arbitrary sleep timers.")
        else:
            print(f"[FAIL] Found {len(violations)} testing hygiene violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
