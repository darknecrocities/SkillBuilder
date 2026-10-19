#!/usr/bin/env python3
"""
CLI utility to audit database migration scripts for zero-downtime safety,
hazardous locks, and missing indexes.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import os
import re
import sys
from typing import Dict, List


def audit_sql_file(content: str, filepath: str) -> List[Dict[str, str]]:
    issues = []

    # 1. Check for DROP TABLE
    drop_table_matches = re.finditer(r"\bDROP\s+TABLE\b", content, re.IGNORECASE)
    for match in drop_table_matches:
        line_no = content[:match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "DB-HAZARD-DROP-TABLE",
            "severity": "CRITICAL",
            "message": "DROP TABLE detected. Breaches zero-downtime expand-and-contract policy."
        })

    # 2. Check for CREATE INDEX without CONCURRENTLY (in PostgreSQL migrations)
    create_idx_matches = re.finditer(r"\bCREATE\s+INDEX\b", content, re.IGNORECASE)
    for match in create_idx_matches:
        surrounding = content[match.start():match.start() + 40]
        if "concurrently" not in surrounding.lower():
            line_no = content[:match.start()].count("\n") + 1
            issues.append({
                "file": filepath,
                "line": str(line_no),
                "rule": "DB-BLOCKING-INDEX-CREATION",
                "severity": "WARNING",
                "message": "CREATE INDEX should use CONCURRENTLY in production to prevent table write locks."
            })

    # 3. Check for ALTER TABLE DROP COLUMN
    drop_col_matches = re.finditer(r"\bALTER\s+TABLE\b[^\;]+?\bDROP\s+COLUMN\b", content, re.IGNORECASE)
    for match in drop_col_matches:
        line_no = content[:match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "DB-HAZARD-DROP-COLUMN",
            "severity": "WARNING",
            "message": "ALTER TABLE DROP COLUMN requires prior deprecation phase in code."
        })

    return issues


def audit_migrations(path: str) -> List[Dict[str, str]]:
    all_issues = []
    supported_exts = {".sql"}

    for root, _, files in os.walk(path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in supported_exts:
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                    file_issues = audit_sql_file(content, full_path)
                    all_issues.extend(file_issues)
                except Exception as e:
                    print(f"Warning: Failed reading {full_path}: {e}", file=sys.stderr)

    return all_issues


def main():
    parser = argparse.ArgumentParser(description="Audit database migrations for zero-downtime safety.")
    parser.add_argument("--path", "-p", type=str, default=".", help="Directory or SQL file path to audit")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        with open(args.path, "r", encoding="utf-8") as f:
            issues = audit_sql_file(f.read(), args.path)
    elif os.path.isdir(args.path):
        issues = audit_migrations(args.path)
    else:
        print(f"Error: Path '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)

    if not issues:
        print(f"[PASS] No migration hazards detected in: {args.path}")
        sys.exit(0)

    print(f"\n[FAIL] Detected {len(issues)} database migration issue(s):\n" + "=" * 60)
    for issue in issues:
        print(f"[{issue['severity']}] {issue['file']}:{issue['line']} - {issue['rule']}")
        print(f"  {issue['message']}")
    print("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
