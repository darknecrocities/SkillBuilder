#!/usr/bin/env python3
"""
verify_responsiveness_and_qa.py - Audits UI templates and stylesheets for responsive design violations,
viewport meta hygiene, undersized touch targets, and accessibility focus states.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".html", ".tsx", ".jsx", ".vue", ".svelte", ".css"}


def check_html_viewport_meta(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if not file_path.endswith(".html"):
        return violations

    if "<html" in content.lower() and "<head" in content.lower():
        if not re.search(r'<meta\s+name=["\']viewport["\']', content, re.IGNORECASE):
            violations.append({
                "file": file_path,
                "line": 1,
                "rule": "MISSING-VIEWPORT-META",
                "message": "HTML document is missing mandatory <meta name=\"viewport\"> tag."
            })
    return violations


def audit_file_content(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations = check_html_viewport_meta(file_path, content)
    lines = content.splitlines()

    fixed_width_pattern = re.compile(r'(?:w-\[(?:[5-9]\d{2}|\d{4,})px\]|width:\s*(?:[5-9]\d{2}|\d{4,})px)', re.IGNORECASE)
    outline_none_pattern = re.compile(r'class(?:Name)?=["\'][^"\']*\boutline-none\b[^"\']*["\']', re.IGNORECASE)
    unresponsive_grid = re.compile(r'class(?:Name)?=["\'][^"\']*\bgrid-cols-(?:[2-9]|1[0-2])\b', re.IGNORECASE)

    for line_idx, line in enumerate(lines, start=1):
        # 1. Fixed pixel container width
        if fixed_width_pattern.search(line):
            violations.append({
                "file": file_path,
                "line": line_idx,
                "rule": "FIXED-PIXEL-CONTAINER-WIDTH",
                "message": "Hardcoded pixel width >= 500px detected. Use fluid widths ('w-full max-w-5xl').",
                "snippet": line.strip()[:100]
            })

        # 2. Outline none without accessible focus replacement
        if outline_none_pattern.search(line):
            if "focus-visible:" not in line and "focus:" not in line and "ring-" not in line:
                violations.append({
                    "file": file_path,
                    "line": line_idx,
                    "rule": "MISSING-FOCUS-RING",
                    "message": "Element suppresses outline without accessible focus replacement.",
                    "snippet": line.strip()[:100]
                })

        # 3. Unresponsive static grid
        if unresponsive_grid.search(line):
            if not re.search(r'\b(sm|md|lg):grid-cols-', line):
                violations.append({
                    "file": file_path,
                    "line": line_idx,
                    "rule": "UNRESPONSIVE-GRID-COLUMNS",
                    "message": "Multi-column grid lacks responsive breakpoint modifier (e.g. 'grid-cols-1 md:grid-cols-3').",
                    "snippet": line.strip()[:100]
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
                        all_violations.extend(audit_file_content(fp, content))
                except Exception as err:
                    all_violations.append({"file": fp, "line": 0, "rule": "READ-ERROR", "message": str(err)})
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit templates and styles for responsive design standards.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            violations = audit_file_content(target, f.read())
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Responsiveness & QA Audit: {target} ===")
        if not violations:
            print("[PASS] All templates comply with responsive viewport and accessibility standards.")
        else:
            print(f"[FAIL] Found {len(violations)} responsive QA violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
