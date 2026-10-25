#!/usr/bin/env python3
"""
verify_end_to_end_integration.py - Audits full-stack route handlers for real database persistence,
boundary schema validation, and absence of fake mock data flags.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".ts", ".js", ".py"}

PERSISTENCE_MARKERS = re.compile(
    r"\b(?:db\.|prisma\.|drizzle\.|repository\.|cursor\.execute|session\.query|connection\.query|supabase\.)",
    re.IGNORECASE
)
SCHEMA_VALIDATION_MARKERS = re.compile(
    r"\b(?:zod|pydantic|schema\.parse|schema\.safeParse|validator\.validate|BaseModel)\b",
    re.IGNORECASE
)
MOCK_FLAGS = re.compile(
    r"\b(?:USE_MOCK_DATA|isMockMode|MOCK_DATABASE|useDummyData)\s*[:=]\s*(?:true|True|1)\b"
)


def audit_route_file(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []

    # 1. Check for mock toggle flags
    for line_idx, line in enumerate(content.splitlines(), start=1):
        if MOCK_FLAGS.search(line):
            violations.append({
                "file": file_path,
                "line": line_idx,
                "rule": "MOCK-TOGGLE-FLAG-DETECTED",
                "message": "Fake mock toggle flag detected. Fullstack features must connect to real persistence.",
                "snippet": line.strip()[:80]
            })

    # 2. Check route handlers for missing validation or persistence
    is_route_file = any(kw in os.path.basename(file_path).lower() for kw in ["route", "controller", "api", "handler"])
    if is_route_file:
        has_mutation_endpoint = bool(re.search(r"\b(POST|PUT|PATCH|post|put|patch)\b", content))
        if has_mutation_endpoint:
            if not SCHEMA_VALIDATION_MARKERS.search(content):
                violations.append({
                    "file": file_path,
                    "line": 1,
                    "rule": "MISSING-SCHEMA-VALIDATION",
                    "message": "Mutation endpoint (POST/PUT/PATCH) detected without request schema validation (Zod/Pydantic)."
                })
            if not PERSISTENCE_MARKERS.search(content) and "test" not in file_path.lower():
                violations.append({
                    "file": file_path,
                    "line": 1,
                    "rule": "MISSING-REAL-PERSISTENCE",
                    "message": "Route handler appears to lack database persistence or repository integration."
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
                        all_violations.extend(audit_route_file(fp, content))
                except Exception as err:
                    all_violations.append({"file": fp, "line": 0, "rule": "READ-ERROR", "message": str(err)})
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit full-stack route handlers for persistence and validation.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            violations = audit_route_file(target, f.read())
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Fullstack End-to-End Audit: {target} ===")
        if not violations:
            print("[PASS] Fullstack routes comply with real persistence and schema validation standards.")
        else:
            print(f"[FAIL] Found {len(violations)} integration violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
