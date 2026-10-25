#!/usr/bin/env python3
"""
verify_app_functionality.py - Audits application code for runtime functionality,
network timeouts, error handling integrity, anti-mock persistence, and secret hygiene.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Quality Assurance Framework
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

IGNORED_DIRS = {
    ".git", "node_modules", "dist", "build", ".agents",
    "__pycache__", "venv", ".venv", ".gemini"
}
CHECKED_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".py", ".dart", ".swift", ".kt"}

# Rule Patterns
PYTHON_REQUEST_NO_TIMEOUT = re.compile(
    r"\brequests\.(?:get|post|put|delete|patch)\s*\((?!.*timeout\s*=)",
    re.IGNORECASE
)
EMPTY_CATCH_BLOCK = re.compile(
    r"(?:catch\s*\([^)]*\)\s*\{\s*\}|except(?:\s+[\w\s,]+)?:\s*pass\b)",
    re.MULTILINE
)
HARDCODED_SECRET = re.compile(
    r"(?:api[_-]?key|secret[_-]?key|auth[_-]?token|private[_-]?key)\s*[:=]\s*[\"'][A-Za-z0-9_\-\.]{24,}[\"']",
    re.IGNORECASE
)
FAKE_MOCK_STORAGE = re.compile(
    r"(?:const|let|var)\s+(?:mock|fake|dummy)[A-Z]\w*\s*=\s*\[",
    re.IGNORECASE
)


def is_test_file(file_path: str) -> bool:
    norm = file_path.lower().replace("\\", "/")
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_source_code(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    lines = content.splitlines()
    is_test = is_test_file(file_path)

    # 1. Empty catch/except block check
    for match in EMPTY_CATCH_BLOCK.finditer(content):
        # Calculate line number from character offset
        line_num = content[:match.start()].count("\n") + 1
        violations.append({
            "file": file_path,
            "line": line_num,
            "rule": "UNHANDLED-EMPTY-CATCH",
            "message": "Empty catch/except block swallows runtime errors without logging or handling.",
            "snippet": match.group(0).strip()[:80]
        })

    # Line-by-line checks
    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # 2. Python requests without timeout
        if file_path.endswith(".py") and "requests." in stripped:
            if PYTHON_REQUEST_NO_TIMEOUT.search(stripped):
                violations.append({
                    "file": file_path,
                    "line": line_idx,
                    "rule": "UNBOUNDED-NETWORK-CALL",
                    "message": "Outbound HTTP call missing mandatory timeout parameter.",
                    "snippet": stripped[:80]
                })

        # 3. Hardcoded secret token in non-test file
        if not is_test and HARDCODED_SECRET.search(stripped):
            violations.append({
                "file": file_path,
                "line": line_idx,
                "rule": "HARDCODED-SECRET-LITERAL",
                "message": "Potential hardcoded secret or API key literal detected.",
                "snippet": stripped[:80]
            })

        # 4. Fake mock storage pretending to be database in non-test file
        if not is_test and FAKE_MOCK_STORAGE.search(stripped):
            violations.append({
                "file": file_path,
                "line": line_idx,
                "rule": "FAKE-MOCK-STORAGE",
                "message": "Fake mock array simulating database in production code.",
                "snippet": stripped[:80]
            })

    return violations


def scan_directory(target_path: str) -> List[Dict[str, Any]]:
    all_violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as handle:
                        all_violations.extend(audit_source_code(fp, handle.read()))
                except Exception as err:
                    all_violations.append({
                        "file": fp,
                        "line": 0,
                        "rule": "READ-ERROR",
                        "message": str(err)
                    })
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit application source code for functional QA standards."
    )
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                violations = audit_source_code(target, f.read())
        except Exception as err:
            violations = [{"file": target, "line": 0, "rule": "READ-ERROR", "message": str(err)}]
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== App Functionality QA Audit: {target} ===")
        if not violations:
            print("[PASS] All source files comply with functional QA and resilience standards.")
        else:
            print(f"[FAIL] Found {len(violations)} functional QA violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
