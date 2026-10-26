#!/usr/bin/env python3
"""
verify_routing_architecture.py - Audits file-based routing structures (Next.js App Router,
Remix, React Router v7) for missing boundaries, polluted entrypoints, and excessive layout nesting.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

DYNAMIC_SEGMENT_PATTERN = re.compile(r'\[[a-zA-Z0-9_\-\.]+\]')
PAGE_FILE_PATTERN = re.compile(r'page\.(?:tsx|jsx|js|ts)$')
LAYOUT_FILE_PATTERN = re.compile(r'layout\.(?:tsx|jsx|js|ts)$')
LOADING_FILE_PATTERN = re.compile(r'loading\.(?:tsx|jsx|js|ts)$')
ERROR_FILE_PATTERN = re.compile(r'error\.(?:tsx|jsx|js|ts)$')


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_routing_directory(route_root: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []

    for root, dirs, files in os.walk(route_root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        rel_path = os.path.relpath(root, route_root)
        segments = [s for s in rel_path.split(os.sep) if s and s != "."]

        # 1. Dynamic segment boundary check
        has_dynamic_segment = any(DYNAMIC_SEGMENT_PATTERN.search(s) for s in segments)
        if has_dynamic_segment:
            has_loading = any(LOADING_FILE_PATTERN.match(f) for f in files)
            has_error = any(ERROR_FILE_PATTERN.match(f) for f in files)
            has_page = any(PAGE_FILE_PATTERN.match(f) for f in files)

            if has_page and not has_loading:
                violations.append({
                    "file": root,
                    "line": 1,
                    "rule": "ROUTING-MISSING-LOADING-BOUNDARY",
                    "message": f"Dynamic route '{rel_path}' is missing a co-located loading.tsx boundary."
                })

            if has_page and not has_error:
                violations.append({
                    "file": root,
                    "line": 1,
                    "rule": "ROUTING-MISSING-ERROR-BOUNDARY",
                    "message": f"Dynamic route '{rel_path}' is missing a co-located error.tsx boundary."
                })

        # 2. Check layout depth
        layout_depth = sum(1 for s in segments if not s.startswith("("))
        if layout_depth > 4:
            violations.append({
                "file": root,
                "line": 1,
                "rule": "ROUTING-EXCESSIVE-LAYOUT-DEPTH",
                "message": f"Route segment depth ({layout_depth}) exceeds recommended ceiling of 4 nested layouts."
            })

        # 3. Check for polluted page.tsx entrypoints
        for f in files:
            if PAGE_FILE_PATTERN.match(f):
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as pf:
                        lines = pf.readlines()
                    if len(lines) > 100:
                        violations.append({
                            "file": fp,
                            "line": 1,
                            "rule": "ROUTING-POLLUTED-PAGE-ENTRYPOINT",
                            "message": f"page.tsx ({len(lines)} lines) exceeds 100 lines. Extract feature components to domain slice."
                        })
                except Exception:
                    pass

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit file-based routing architecture.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or app/ directory to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    # Detect app or src/app directory if present
    app_dir = target
    for candidate in [os.path.join(target, "app"), os.path.join(target, "src", "app")]:
        if os.path.isdir(candidate):
            app_dir = candidate
            break

    violations = audit_routing_directory(app_dir)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== File-Based Routing Architecture Audit: {app_dir} ===")
        if not violations:
            print("[PASS] Routing architecture verified. All dynamic routes have loading/error boundaries.")
        else:
            print(f"[FAIL] Found {len(violations)} routing architecture violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
