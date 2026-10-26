#!/usr/bin/env python3
"""
audit_security_hygiene.py - Scans source code for potential secret leaks, dangerous shell execution,
SQL query interpolation, silent error swallowing, ReDoS risks, and unescaped HTML injection.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".sh", ".env.example"}

# Line-level security rules
LINE_SECURITY_RULES: List[Tuple[str, str, str]] = [
    ("HARDCODED-GOOGLE-API-KEY", r"AIza[0-9A-Za-z\-_]{35}", "Potential Google Cloud / Gemini API key found."),
    ("HARDCODED-AWS-KEY", r"\bAKIA[0-9A-Z]{16}\b", "Potential AWS Access Key ID found."),
    ("HARDCODED-GITHUB-TOKEN", r"\bghp_[0-9A-Za-z]{36}\b", "Potential GitHub Personal Access Token found."),
    ("UNSAFE-SQL-INTERPOLATION", r"(?:execute|query)\s*\(\s*f?[\"'].*(?:SELECT|INSERT|UPDATE|DELETE)\b.*\{", "SQL query constructed with string interpolation. Use parameterized queries."),
    ("UNSAFE-EVAL-EXEC", r"\b(?:eval|exec)\s*\(", "Dangerous dynamic code execution (eval/exec) detected."),
    ("UNSAFE-SHELL-TRUE", r"subprocess\.\w+\([^)]*shell\s*=\s*True", "Python subprocess invoked with shell=True. High risk of command injection."),
    ("UNSANITIZED-HTML-INJECTION", r"dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html:(?!.*DOMPurify)", "React dangerouslySetInnerHTML used without DOMPurify sanitization."),
    ("SENSITIVE-STACK-LEAK", r"\bres(?:\.status\(\d+\))?\.(?:send|json)\([^)]*(?:err|error)\.stack", "Potential stack trace leak in HTTP response payload. Sanitize errors to RFC 7807."),
    ("INSECURE-CORS-WILDCARD", r"(?:origin\s*:\s*[\"']\*[\"'].*credentials\s*:\s*true|credentials\s*:\s*true.*origin\s*:\s*[\"']\*[\"'])", "Insecure CORS wildcard with credentials enabled."),
    ("VULNERABLE-REDOS", r"\(\s*\[?[a-zA-Z0-9_\-\.\+]+\]?\+\s*\)\+", "Potential catastrophic backtracking regex (ReDoS risk). Avoid nested unbounded quantifiers.")
]

# Multiline pattern rules (e.g., empty catch or except blocks spanning multiple lines)
MULTILINE_SECURITY_RULES: List[Tuple[str, re.Pattern, str]] = [
    (
        "SILENT-ERROR-SWALLOWING",
        re.compile(r"(?:catch\s*\([^)]*\)\s*\{\s*\}|except(?:\s+[\w\s,()]+)?:\s*pass\b)", re.MULTILINE),
        "Silent error swallowing (empty catch block or except: pass) conceals system faults."
    )
]


def is_test_file(file_path: str) -> bool:
    """Returns True if the file is a test suite or test fixture."""
    norm = file_path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_file(file_path: str, allow_test_files: bool = False) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    # Skip checking this validator itself, its test suite, or test files unless explicitly requested
    if "audit_security_hygiene" in file_path:
        return violations
    if not allow_test_files and is_test_file(file_path):
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    # Check multiline rules across content
    for rule_id, pattern, desc in MULTILINE_SECURITY_RULES:
        for match in pattern.finditer(content):
            line_num = content[:match.start()].count("\n") + 1
            violations.append({
                "file": file_path,
                "line": line_num,
                "rule": rule_id,
                "message": desc,
                "snippet": match.group(0).strip().replace("\n", " ")[:90]
            })

    # Check line-level rules
    lines = content.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        for rule_id, pattern_str, desc in LINE_SECURITY_RULES:
            if re.search(pattern_str, line):
                violations.append({
                    "file": file_path,
                    "line": line_idx,
                    "rule": rule_id,
                    "message": desc,
                    "snippet": line.strip()[:90]
                })

    return violations


def scan_directory(target_path: str, allow_test_files: bool = False) -> List[Dict[str, Any]]:
    all_violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS or f == ".env.example":
                fp = os.path.join(root, f)
                all_violations.extend(audit_file(fp, allow_test_files=allow_test_files))
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit source code for security vulnerabilities.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    parser.add_argument("--include-tests", action="store_true", help="Include test files in audit")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_file(target, allow_test_files=args.include_tests)
    else:
        violations = scan_directory(target, allow_test_files=args.include_tests)

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
