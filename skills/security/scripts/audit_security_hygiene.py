#!/usr/bin/env python3
"""
audit_security_hygiene.py - Scans source code for potential secret leaks, dangerous shell execution,
SQL query interpolation, and unescaped HTML injection.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".sh", ".env.example"}

SECURITY_RULES: List[Tuple[str, str, str]] = [
    ("HARDCODED-GOOGLE-API-KEY", r"AIza[0-9A-Za-z\-_]{35}", "Potential Google Cloud / Gemini API key found."),
    ("HARDCODED-AWS-KEY", r"\bAKIA[0-9A-Z]{16}\b", "Potential AWS Access Key ID found."),
    ("HARDCODED-GITHUB-TOKEN", r"\bghp_[0-9A-Za-z]{36}\b", "Potential GitHub Personal Access Token found."),
    ("UNSAFE-SQL-INTERPOLATION", r"(?:execute|query)\s*\(\s*f?[\"'].*(?:SELECT|INSERT|UPDATE|DELETE)\b.*\{", "SQL query constructed with string interpolation. Use parameterized queries."),
    ("UNSAFE-EVAL-EXEC", r"\b(?:eval|exec)\s*\(", "Dangerous dynamic code execution (eval/exec) detected."),
    ("UNSAFE-SHELL-TRUE", r"subprocess\.\w+\([^)]*shell\s*=\s*True", "Python subprocess invoked with shell=True. High risk of command injection."),
    ("UNSANITIZED-HTML-INJECTION", r"dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html:(?!.*DOMPurify)", "React dangerouslySetInnerHTML used without DOMPurify sanitization.")
]


def audit_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    # Skip checking this validator itself or its test suite
    if "audit_security_hygiene" in file_path or "test_audit_security_hygiene" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    for line_idx, line in enumerate(lines, start=1):
        for rule_id, pattern, desc in SECURITY_RULES:
            if re.search(pattern, line):
                violations.append({
                    "file": file_path,
                    "line": line_idx,
                    "rule": rule_id,
                    "message": desc,
                    "snippet": line.strip()[:90]
                })

    return violations


def scan_directory(target_path: str) -> List[Dict[str, Any]]:
    all_violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS or f == ".env.example":
                fp = os.path.join(root, f)
                all_violations.extend(audit_file(fp))
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit source code for security vulnerabilities.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_file(target)
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Security Hygiene Audit: {target} ===")
        if not violations:
            print("[PASS] No security vulnerabilities or credential leaks detected.")
        else:
            print(f"[FAIL] Found {len(violations)} security violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
