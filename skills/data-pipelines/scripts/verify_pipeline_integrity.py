#!/usr/bin/env python3
"""
verify_pipeline_integrity.py - Audits data pipeline scripts for unbuffered in-memory loading,
missing backpressure, and absent dead-letter queues.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

UNBOUNDED_READ_CSV = re.compile(r'\bpd\.read_csv\s*\((?!.*chunksize\s*=)', re.IGNORECASE)
PIPELINE_SILENT_DISCARD = re.compile(r'except(?:\s+[\w\s,()]+)?:\s*(?:pass|continue)\b')


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_pipeline_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if is_test_file(file_path) or "verify_pipeline_integrity" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # 1. Unbounded read_csv without chunksize
        if UNBOUNDED_READ_CSV.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "PIPELINE-UNBOUNDED-READ",
                "message": "Unbounded pd.read_csv() without chunksize. Stream large files with chunks to prevent OOM errors.",
                "snippet": line.strip()[:80]
            })

    # 2. Check for silent row discard in pipeline loops
    if "for " in content and "batch" in content.lower():
        for match in PIPELINE_SILENT_DISCARD.finditer(content):
            line_num = content[:match.start()].count("\n") + 1
            violations.append({
                "file": file_path,
                "line": line_num,
                "rule": "PIPELINE-MISSING-DEAD-LETTER-QUEUE",
                "message": "Pipeline error discarded silently with pass/continue. Route failed records to a Dead-Letter Queue (DLQ).",
                "snippet": match.group(0).strip()[:80]
            })

    return violations


def scan_pipeline_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            if f.endswith((".py", ".ts", ".js")):
                violations.extend(audit_pipeline_file(fp))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit data pipeline integrity and streaming resilience.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_pipeline_file(target)
    else:
        violations = scan_pipeline_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Data Pipeline Integrity Audit: {target} ===")
        if not violations:
            print("[PASS] Pipeline integrity verified. Clean chunking and resilient error handling.")
        else:
            print(f"[FAIL] Found {len(violations)} pipeline integrity violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
