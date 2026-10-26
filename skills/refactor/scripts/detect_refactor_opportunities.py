#!/usr/bin/env python3
"""
detect_refactor_opportunities.py - Audits codebases for refactoring triggers:
files nearing the 500-line limit, oversized functions, and deep cyclomatic nesting.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".dart"}

MAX_FILE_WARNING_THRESHOLD = 350
MAX_FUNCTION_LINES = 40
MAX_NESTING_LEVEL = 3


def audit_file_complexity(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    total_lines = len(lines)
    if total_lines > MAX_FILE_WARNING_THRESHOLD:
        violations.append({
            "file": file_path,
            "line": total_lines,
            "rule": "FILE-NEARING-LINE-LIMIT",
            "message": f"File has {total_lines} lines (approaching 500-line ceiling). Decompose into submodules."
        })

    current_func: str = ""
    func_start_line: int = 0
    func_indent: int = 0

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip()
        stripped = line.strip()

        # Check deep nesting (indent level)
        if stripped and not stripped.startswith("//") and not stripped.startswith("#"):
            leading_spaces = len(line) - len(line.lstrip(" "))
            leading_tabs = len(line) - len(line.lstrip("\t"))
            effective_level = (leading_spaces // 4) + leading_tabs
            if effective_level > MAX_NESTING_LEVEL:
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "DEEP-LOGICAL-NESTING",
                    "message": f"Nesting level {effective_level} exceeds maximum recommended {MAX_NESTING_LEVEL}. Use guard clauses.",
                    "snippet": stripped[:80]
                })

        # Function definition detector
        func_match = re.search(r"^\s*(?:def|function|async\s+def|async\s+function|\w+\s*\([^)]*\)\s*[:{])\s*([a-zA-Z_]\w*)", line)
        if func_match:
            if current_func and (idx - func_start_line) > MAX_FUNCTION_LINES:
                violations.append({
                    "file": file_path,
                    "line": func_start_line,
                    "rule": "OVERSIZED-FUNCTION",
                    "message": f"Function '{current_func}' spans {idx - func_start_line} lines (limit: {MAX_FUNCTION_LINES}). Extract sub-helpers."
                })
            current_func = func_match.group(1)
            func_start_line = idx

    return violations


def scan_directory(target_path: str) -> List[Dict[str, Any]]:
    all_violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS:
                fp = os.path.join(root, f)
                all_violations.extend(audit_file_complexity(fp))
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit codebase for refactoring opportunities.")
    parser.add_argument("--path", "-p", default=".", help="Root path or file to audit")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_file_complexity(target)
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Refactoring Opportunities Audit: {target} ===")
        if not violations:
            print("[PASS] Codebase is well-factored with no oversized files or deep nesting.")
        else:
            print(f"[FAIL] Found {len(violations)} refactoring trigger(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
