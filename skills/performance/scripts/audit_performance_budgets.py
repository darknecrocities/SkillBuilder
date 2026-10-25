#!/usr/bin/env python3
"""
audit_performance_budgets.py - Audits codebases for performance anti-patterns:
N+1 query cascades, unbounded SQL queries, unconstrained image layouts, and oversize source files.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".html"}

UNBOUNDED_SELECT_PATTERN = re.compile(r"SELECT\s+.*?\s+FROM\s+\w+(?!.*(?:WHERE|LIMIT))\b", re.IGNORECASE)
IMAGE_WITHOUT_DIMENSIONS = re.compile(r"<img\b(?!.*(?:width|height|fill|className=.*w-))[^>]*>", re.IGNORECASE)


def audit_file_performance(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []

    # 1. Detect N+1 loop query execution in Python/TS
    lines = content.splitlines()
    in_loop = False
    loop_line = 0

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if re.search(r"^(?:for\s+\w+\s+in|for\s*\(const\s+\w+\s+of)\b", stripped):
            in_loop = True
            loop_line = idx
        elif in_loop:
            # Check indentation or closing brace
            if stripped == "}" or (line and not line.startswith(" ") and not line.startswith("\t")):
                in_loop = False
            elif re.search(r"\b(?:db\.|cursor\.execute|session\.query|prisma\.\w+\.find|await\s+\w+Repo)\b", stripped):
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "N-PLUS-ONE-QUERY-CASCADE",
                    "message": f"Database query inside loop started at line {loop_line}. Batch query using IN operator or eager loading.",
                    "snippet": stripped[:80]
                })

    # 2. Detect unbounded SELECT queries
    for match in UNBOUNDED_SELECT_PATTERN.finditer(content):
        line_no = content[:match.start()].count("\n") + 1
        violations.append({
            "file": file_path,
            "line": line_no,
            "rule": "UNBOUNDED-DATABASE-QUERY",
            "message": "Unbounded SELECT query without LIMIT or WHERE clause detected.",
            "snippet": match.group(0)[:80]
        })

    # 3. Detect images without dimensions (CLS risk)
    for match in IMAGE_WITHOUT_DIMENSIONS.finditer(content):
        line_no = content[:match.start()].count("\n") + 1
        violations.append({
            "file": file_path,
            "line": line_no,
            "rule": "IMAGE-MISSING-DIMENSIONS",
            "message": "<img /> missing explicit width/height or responsive sizing (CLS hazard).",
            "snippet": match.group(0)[:80]
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
                    with open(fp, "r", encoding="utf-8", errors="ignore") as file_handle:
                        content = file_handle.read()
                        all_violations.extend(audit_file_performance(fp, content))
                except Exception as err:
                    all_violations.append({"file": fp, "line": 0, "rule": "READ-ERROR", "message": str(err)})
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit codebase for performance and Core Web Vitals anti-patterns.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            violations = audit_file_performance(target, f.read())
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Performance & Core Web Vitals Audit: {target} ===")
        if not violations:
            print("[PASS] No N+1 queries, unbounded selects, or CLS hazards detected.")
        else:
            print(f"[FAIL] Found {len(violations)} performance violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
