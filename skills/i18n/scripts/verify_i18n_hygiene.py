#!/usr/bin/env python3
"""
verify_i18n_hygiene.py - Audits UI templates for hardcoded natural language strings,
physical directional CSS properties, and ternary pluralizations.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

HARDCODED_JSX_TEXT = re.compile(r'>\s*([A-Z][a-zA-Z0-9\s]{5,}[!\?\.])\s*<')
PHYSICAL_CSS_DIRECTION = re.compile(r'\b(?:margin|padding)-(?:left|right)\s*:\s*[^;]+;', re.IGNORECASE)
TERNARY_PLURAL_PATTERN = re.compile(r'\w+\s*===\s*1\s*\?\s*["\'][^"\']+["\']\s*:\s*["\'][^"\']+["\']')


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_i18n_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if is_test_file(file_path) or "verify_i18n_hygiene" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # 1. Hardcoded JSX plain text
        if file_path.endswith((".tsx", ".jsx")) and not stripped.startswith(("//", "/*", "*")):
            match = HARDCODED_JSX_TEXT.search(line)
            if match and "t(" not in line and "{" not in match.group(1):
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "I18N-HARDCODED-UI-STRING",
                    "message": f"Hardcoded string '{match.group(1).strip()}' in JSX. Use translation hook: t('key').",
                    "snippet": line.strip()[:80]
                })

        # 2. Physical directional CSS property
        if file_path.endswith((".css", ".scss", ".tsx", ".jsx")):
            if PHYSICAL_CSS_DIRECTION.search(line):
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "I18N-PHYSICAL-CSS-DIRECTION",
                    "message": "Physical directional CSS property found. Use CSS logical properties (margin-inline-start, padding-inline-end).",
                    "snippet": line.strip()[:80]
                })

        # 3. Ternary pluralization anti-pattern
        if TERNARY_PLURAL_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "I18N-TERNARY-PLURALIZATION",
                "message": "Manual ternary pluralization detected. Use ICU MessageFormat plural syntax.",
                "snippet": line.strip()[:80]
            })

    return violations


def scan_i18n_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            if f.endswith((".tsx", ".jsx", ".css", ".scss")):
                violations.extend(audit_i18n_file(fp))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit internationalization and RTL hygiene.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_i18n_file(target)
    else:
        violations = scan_i18n_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Internationalization & RTL Hygiene Audit: {target} ===")
        if not violations:
            print("[PASS] Internationalization hygiene verified. Zero hardcoded text or physical directional styles.")
        else:
            print(f"[FAIL] Found {len(violations)} i18n violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
