#!/usr/bin/env python3
"""
CLI utility to audit backend route files for boundary validation schemas,
status code compliance, and error boundary usage.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import os
import re
import sys
from typing import Dict, List


def audit_route_file(content: str, filepath: str) -> List[Dict[str, str]]:
    issues = []

    # Check for mutating routes (post, put, patch)
    route_matches = re.finditer(r"\.(post|put|patch)\s*\(\s*['\"]([^'\"]+)['\"]", content, re.IGNORECASE)
    has_mutation_routes = False
    for r in route_matches:
        has_mutation_routes = True

    # Check for schema validation indicators (Zod or Pydantic)
    has_zod = bool(re.search(r"\b(safeParse|parse)\s*\(", content) or "z.object" in content)
    has_pydantic = bool("BaseModel" in content or "pydantic" in content or "validate(" in content)

    # Check for raw body usage without schema parsing
    uses_raw_body = bool(re.search(r"\breq\.body\b", content))

    if has_mutation_routes and uses_raw_body and not (has_zod or has_pydantic):
        issues.append({
            "file": filepath,
            "line": "1",
            "rule": "BE-MISSING-SCHEMA-VALIDATION",
            "severity": "ERROR",
            "message": "Mutating route handles 'req.body' without Zod or Pydantic schema validation."
        })

    # Check for raw catch returning empty or untyped response
    unhandled_catch = re.search(r"catch\s*\([^\)]*\)\s*\{\s*\}", content)
    if unhandled_catch:
        line_no = content[:unhandled_catch.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "BE-EMPTY-CATCH-BLOCK",
            "severity": "ERROR",
            "message": "Empty catch block suppresses errors silently."
        })

    return issues


def audit_routes(path: str) -> List[Dict[str, str]]:
    all_issues = []
    supported_exts = {".ts", ".js", ".py"}

    for root, _, files in os.walk(path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in supported_exts:
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                    file_issues = audit_route_file(content, full_path)
                    all_issues.extend(file_issues)
                except Exception as e:
                    print(f"Warning: Failed reading {full_path}: {e}", file=sys.stderr)

    return all_issues


def main():
    parser = argparse.ArgumentParser(description="Audit backend routes for schema validation.")
    parser.add_argument("--path", "-p", type=str, default=".", help="Directory or file path to audit")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        with open(args.path, "r", encoding="utf-8") as f:
            issues = audit_route_file(f.read(), args.path)
    elif os.path.isdir(args.path):
        issues = audit_routes(args.path)
    else:
        print(f"Error: Path '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)

    if not issues:
        print(f"[PASS] No backend contract or validation issues detected in: {args.path}")
        sys.exit(0)

    print(f"\n[FAIL] Detected {len(issues)} backend contract issue(s):\n" + "=" * 60)
    for issue in issues:
        print(f"[{issue['severity']}] {issue['file']}:{issue['line']} - {issue['rule']}")
        print(f"  {issue['message']}")
    print("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
