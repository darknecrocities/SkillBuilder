#!/usr/bin/env python3
"""
verify_frontend_architecture.py - Audits frontend codebases for lifecycle memory safety,
AbortController signal propagation in effects, and error boundary presence.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".tsx", ".jsx", ".ts", ".js"}


def audit_component_file(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []

    # 1. Detect useEffect with fetch() without signal / abort
    use_effect_blocks = re.finditer(r"useEffect\s*\(\s*\(\)\s*=>\s*\{([^}]*)\}", content, re.DOTALL)
    for match in use_effect_blocks:
        body = match.group(1)
        if "fetch(" in body and "signal" not in body and "abort" not in body:
            line_no = content[:match.start()].count("\n") + 1
            violations.append({
                "file": file_path,
                "line": line_no,
                "rule": "UNPROTECTED-ASYNC-EFFECT",
                "message": "useEffect contains fetch() call without AbortController or signal propagation.",
                "snippet": match.group(0)[:80].replace("\n", " ")
            })

    # 2. Detect direct window object mutations
    for match in re.finditer(r"window\.(\w+)\s*=\s*", content):
        var_name = match.group(1)
        if var_name not in {"dataLayer", "__REDUX_DEVTOOLS_EXTENSION__"}:
            line_no = content[:match.start()].count("\n") + 1
            violations.append({
                "file": file_path,
                "line": line_no,
                "rule": "DIRECT-WINDOW-MUTATION",
                "message": f"Global window object mutation ('window.{var_name}') detected. Use explicit React context or state store.",
                "snippet": match.group(0)[:80]
            })

    return violations


def audit_directory(target_path: str) -> List[Dict[str, Any]]:
    all_violations: List[Dict[str, Any]] = []
    has_app_router = False
    has_error_boundary = False

    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        if os.path.basename(root) == "app":
            has_app_router = True
        for f in files:
            if f in {"error.tsx", "error.jsx", "error.js", "ErrorBoundary.tsx"}:
                has_error_boundary = True
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as file_handle:
                        content = file_handle.read()
                        all_violations.extend(audit_component_file(fp, content))
                except Exception as err:
                    all_violations.append({"file": fp, "line": 0, "rule": "READ-ERROR", "message": str(err)})

    if has_app_router and not has_error_boundary:
        all_violations.append({
            "file": target_path,
            "line": 1,
            "rule": "MISSING-APP-ERROR-BOUNDARY",
            "message": "Next.js App Router detected, but no root 'error.tsx' or ErrorBoundary found."
        })

    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit frontend source files for architectural patterns.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            violations = audit_component_file(target, f.read())
    else:
        violations = audit_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Frontend Architecture Audit: {target} ===")
        if not violations:
            print("[PASS] Frontend architecture complies with clean state and memory safety standards.")
        else:
            print(f"[FAIL] Found {len(violations)} architectural violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
