#!/usr/bin/env python3
"""
verify_local_first_hygiene.py - Audits local-first storage and public/private data boundaries.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", "venv", ".venv"}
CHECKED_EXTS = {".ts", ".tsx", ".js", ".jsx", ".py"}


def audit_data_file(file_path: Path) -> List[Dict[str, str]]:
    """Check for direct raw generated-data imports in UI routes and unguarded JSON storage."""
    issues: List[Dict[str, str]] = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    norm_path = str(file_path).replace("\\", "/")

    is_ui_or_route = any(seg in norm_path for seg in ("/app/", "/pages/", "/components/"))
    if is_ui_or_route and re.search(r"data/generated/", content):
        issues.append({
            "file": str(file_path),
            "rule": "DATA-BOUNDARY-BYPASS",
            "message": "UI/route imports raw generated data directly instead of typed access layer.",
        })
    if "indexedDB.open(" in content and "onupgradeneeded" not in content:
        issues.append({
            "file": str(file_path),
            "rule": "IDB-MISSING-MIGRATION-HANDLER",
            "message": "indexedDB.open() missing onupgradeneeded schema migration handler.",
        })
    return issues


def scan_directory(target_path: Path) -> List[Dict[str, str]]:
    """Scan file or directory for local-first and data-boundary violations."""
    if target_path.is_file():
        return audit_data_file(target_path)

    violations: List[Dict[str, str]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for fname in sorted(files):
            if Path(fname).suffix.lower() in CHECKED_EXTS:
                violations.extend(audit_data_file(Path(root) / fname))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit local-first storage and public/private data boundaries.")
    parser.add_argument("--path", "-p", default=".", help="Path to inspect")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    findings = scan_directory(Path(args.path).resolve())
    print(f"=== Local-First & Data Boundary Audit: {args.path} ===")
    if not findings:
        print("[PASS] Data boundaries and local-first migrations comply.")
        return 0
    for f in findings:
        print(f"  - {f['file']} [{f['rule']}] {f['message']}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
