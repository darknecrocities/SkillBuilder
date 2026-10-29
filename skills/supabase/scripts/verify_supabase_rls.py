#!/usr/bin/env python3
"""
verify_supabase_rls.py - Audits SQL migrations for Row Level Security (RLS) enforcement
and client code for service_role key leaks.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Set

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

CREATE_TABLE_PATTERN = re.compile(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:public\.)?([a-zA-Z0-9_]+)', re.IGNORECASE)
ENABLE_RLS_PATTERN = re.compile(r'ALTER\s+TABLE\s+(?:public\.)?([a-zA-Z0-9_]+)\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY', re.IGNORECASE)
PERMISSIVE_POLICY_PATTERN = re.compile(r'CREATE\s+POLICY\s+.*?USING\s*\(\s*true\s*\)', re.IGNORECASE)
DESTRUCTIVE_SUPABASE_SQL_PATTERN = re.compile(
    r'\b(?:DROP\s+TABLE|TRUNCATE\s+(?:TABLE\s+)?[a-zA-Z0-9_\.]+|DELETE\s+FROM\s+storage\.(?:objects|buckets))\b',
    re.IGNORECASE,
)
SERVICE_ROLE_CLIENT_PATTERN = re.compile(r'(?:NEXT_PUBLIC_SUPABASE_SERVICE_ROLE|supabaseServiceRoleKey|service_role_key|service_role\b)', re.IGNORECASE)


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_supabase_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if is_test_file(file_path) or "verify_supabase_rls" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    # 1. SQL Migration checks
    if file_path.endswith(".sql"):
        created_tables: Set[str] = set()
        rls_tables: Set[str] = set()

        for match in CREATE_TABLE_PATTERN.finditer(content):
            created_tables.add(match.group(1).lower())

        for match in ENABLE_RLS_PATTERN.finditer(content):
            rls_tables.add(match.group(1).lower())

        for table in created_tables:
            if table not in rls_tables:
                violations.append({
                    "file": file_path,
                    "line": 1,
                    "rule": "SUPABASE-MISSING-RLS",
                    "message": f"Table '{table}' created without 'ALTER TABLE ... ENABLE ROW LEVEL SECURITY;'."
                })

        for match in PERMISSIVE_POLICY_PATTERN.finditer(content):
            line_num = content[:match.start()].count("\n") + 1
            violations.append({
                "file": file_path,
                "line": line_num,
                "rule": "SUPABASE-PERMISSIVE-POLICY",
                "message": "Insecure permissive RLS policy with 'USING (true)' detected."
            })

        approved_delete = "@user-approved-deletion" in content.lower() and "@verified-backup-sha256" in content.lower()
        if not approved_delete:
            for match in DESTRUCTIVE_SUPABASE_SQL_PATTERN.finditer(content):
                line_num = content[:match.start()].count("\n") + 1
                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule": "SUPABASE-UNSAFE-DESTRUCTIVE-SQL",
                    "message": "Destructive Supabase SQL (DROP/TRUNCATE/storage purge) requires prior user confirmation and verified backup SHA-256."
                })

    # 2. Client-side service role exposure
    if file_path.endswith((".ts", ".tsx", ".js", ".jsx")) and ("client" in file_path.lower() or "components" in file_path.lower()):
        for idx, line in enumerate(content.splitlines(), start=1):
            if SERVICE_ROLE_CLIENT_PATTERN.search(line) and not line.strip().startswith("//"):
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "SUPABASE-EXPOSED-SERVICE-KEY",
                    "message": "Potential exposure of Supabase service_role key in client component.",
                    "snippet": line.strip()[:80]
                })

    return violations


def scan_supabase_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            if f.endswith((".sql", ".ts", ".tsx", ".js", ".jsx")):
                violations.extend(audit_supabase_file(fp))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Supabase RLS and client security.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_supabase_file(target)
    else:
        violations = scan_supabase_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Supabase Architecture & RLS Audit: {target} ===")
        if not violations:
            print("[PASS] Supabase RLS verified. All tables enforce row-level security.")
        else:
            print(f"[FAIL] Found {len(violations)} Supabase violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
