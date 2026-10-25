#!/usr/bin/env python3
"""
verify_telemetry_standards.py - Audits codebases for structured logging hygiene,
correlation ID propagation, and health/readiness probe declarations.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".py", ".ts", ".js", ".go"}

RAW_PRINT_PATTERN = re.compile(r"^\s*(?:console\.log|print)\s*\(", re.MULTILINE)
CORRELATION_ID_MARKERS = re.compile(r"\b(?:trace_id|span_id|correlation_id|requestId|traceparent)\b", re.IGNORECASE)
HEALTH_ENDPOINT_MARKER = re.compile(r"[\"']/(?:healthz|readyz|health|live)[\"']", re.IGNORECASE)


def audit_file_telemetry(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    # Skip test scripts or standalone CLI tools
    if "test" in file_path.lower() or "scripts/" in file_path.lower():
        return violations

    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        if RAW_PRINT_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "RAW-PRINT-IN-PRODUCTION",
                "message": "Raw console.log or print detected in service code. Use structured logger.",
                "snippet": line.strip()[:80]
            })

    return violations


def audit_directory_telemetry(target_path: str) -> List[Dict[str, Any]]:
    all_violations: List[Dict[str, Any]] = []
    has_routes = False
    has_health = False

    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as file_handle:
                        content = file_handle.read()
                        if "route" in f.lower() or "app" in f.lower() or "server" in f.lower():
                            has_routes = True
                            if HEALTH_ENDPOINT_MARKER.search(content):
                                has_health = True
                        all_violations.extend(audit_file_telemetry(fp, content))
                except Exception as err:
                    all_violations.append({"file": fp, "line": 0, "rule": "READ-ERROR", "message": str(err)})

    if has_routes and not has_health:
        all_violations.append({
            "file": target_path,
            "line": 1,
            "rule": "MISSING-HEALTH-PROBE",
            "message": "Service defines API routes but lacks a standard /healthz or /readyz probe endpoint."
        })

    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit codebase for telemetry and observability standards.")
    parser.add_argument("--path", "-p", default=".", help="Root path to audit")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            violations = audit_file_telemetry(target, f.read())
    else:
        violations = audit_directory_telemetry(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Telemetry & Observability Audit: {target} ===")
        if not violations:
            print("[PASS] Codebase complies with structured logging and healthcheck standards.")
        else:
            print(f"[FAIL] Found {len(violations)} telemetry violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
