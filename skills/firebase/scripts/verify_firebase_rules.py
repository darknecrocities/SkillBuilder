#!/usr/bin/env python3
"""
verify_firebase_rules.py - Audits Firebase Security Rules (firestore.rules, storage.rules)
and client bundles for insecure permissions and credential leaks.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

OPEN_RULE_PATTERN = re.compile(r'allow\s+(?:read\s*,\s*write|write|create|update|delete|read)\s*:\s*if\s+true\s*;', re.IGNORECASE)
UNSCOPED_DELETE_RULE_PATTERN = re.compile(
    r'allow\s+delete\s*:\s*if\s+(?:request\.auth\s*!=\s*null|isAuthenticated\(\))\s*;',
    re.IGNORECASE,
)
ADMIN_SDK_KEY_PATTERN = re.compile(r'firebase-adminsdk-[0-9a-z]+')
PRIVATE_KEY_JSON_PATTERN = re.compile(r'"private_key"\s*:\s*"-----BEGIN')


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_firebase_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if is_test_file(file_path) or "verify_firebase_rules" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    # 1. Exposed Firebase Admin SDK private key JSON
    if file_path.endswith(".json") and (ADMIN_SDK_KEY_PATTERN.search(content) or PRIVATE_KEY_JSON_PATTERN.search(content)):
        violations.append({
            "file": file_path,
            "line": 1,
            "rule": "FIREBASE-EXPOSED-ADMIN-KEY",
            "message": "Committed Firebase Admin SDK private key detected. Store credentials in Secret Manager."
        })

    # 2. Open wildcard permissions or unscoped delete rules in .rules files
    if file_path.endswith(".rules") or "firestore.rules" in file_path or "storage.rules" in file_path:
        approved_delete = "@user-approved-deletion" in content.lower()
        lines = content.splitlines()
        for idx, line in enumerate(lines, start=1):
            if OPEN_RULE_PATTERN.search(line):
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "FIREBASE-OPEN-WILDCARD-RULE",
                    "message": "Insecure open wildcard permission ('allow ...: if true;'). Restrict to authenticated users.",
                    "snippet": line.strip()[:80]
                })
            elif UNSCOPED_DELETE_RULE_PATTERN.search(line) and not approved_delete:
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "FIREBASE-UNSAFE-DELETE-RULE",
                    "message": "Unscoped hard delete ('allow delete: if request.auth != null;') allows any user to delete records. Use soft-deletes or strict owner/admin scoping.",
                    "snippet": line.strip()[:80]
                })

    return violations


def scan_firebase_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            if f.endswith((".rules", ".json", ".ts", ".js")):
                violations.extend(audit_firebase_file(fp))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Firebase security rules and configuration.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_firebase_file(target)
    else:
        violations = scan_firebase_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Firebase Rules & Security Audit: {target} ===")
        if not violations:
            print("[PASS] Firebase rules verified. Zero open permissions or admin key leaks.")
        else:
            print(f"[FAIL] Found {len(violations)} Firebase violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
