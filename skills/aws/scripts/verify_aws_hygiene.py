#!/usr/bin/env python3
"""
verify_aws_hygiene.py - Audits repository for AWS security, S3 bucket hardening,
static credentials, and Lambda resilience.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}

AWS_KEY_PATTERN = re.compile(r'\bAKIA[0-9A-Z]{16}\b')
PUBLIC_S3_ACL = re.compile(r'acl\s*=\s*["\']public-read(?:-write)?["\']', re.IGNORECASE)
S3_BUCKET_CONSTRUCT = re.compile(r'(?:new\s+s3\.Bucket|resource\s+["\']aws_s3_bucket["\'])', re.IGNORECASE)
BLOCK_PUBLIC_ACCESS = re.compile(r'(?:blockPublicAccess|block_public_acls|BlockPublicAccess\.BLOCK_ALL)', re.IGNORECASE)
LAMBDA_HIGH_TIMEOUT = re.compile(r'(?:timeout|Duration\.seconds)\s*[:=]\s*(?:cdk\.Duration\.seconds\()?([6-9]\d{2,}|\d{4,})\b')


def is_test_file(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return any(p in norm for p in ["/tests/", "/test/", "test_", ".test.", ".spec."])


def audit_aws_file(file_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    if is_test_file(file_path) or "verify_aws_hygiene" in file_path:
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "READ-ERROR", "message": str(err)}]

    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # 1. Static Access Key Check
        if AWS_KEY_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "AWS-STATIC-ACCESS-KEY",
                "message": "Potential hardcoded AWS Access Key ID found. Use IAM Roles / IRSA.",
                "snippet": line.strip()[:80]
            })

        # 2. Public S3 ACL check
        if PUBLIC_S3_ACL.search(line):
            violations.append({
                "file": file_path,
                "line": idx,
                "rule": "AWS-S3-PUBLIC-EXPOSURE",
                "message": "Insecure public S3 ACL detected ('public-read'). Enforce private block.",
                "snippet": line.strip()[:80]
            })

        # 3. Unbounded Lambda timeout
        timeout_match = LAMBDA_HIGH_TIMEOUT.search(line)
        if timeout_match:
            seconds = int(timeout_match.group(1))
            if seconds > 300:
                violations.append({
                    "file": file_path,
                    "line": idx,
                    "rule": "AWS-LAMBDA-UNBOUNDED-TIMEOUT",
                    "message": f"Lambda timeout ({seconds}s) exceeds recommended bounds. Cap timeouts to prevent resource starvation.",
                    "snippet": line.strip()[:80]
                })

    # 4. S3 Bucket construct missing BlockPublicAccess
    if S3_BUCKET_CONSTRUCT.search(content) and not BLOCK_PUBLIC_ACCESS.search(content):
        violations.append({
            "file": file_path,
            "line": 1,
            "rule": "AWS-S3-MISSING-PUBLIC-BLOCK",
            "message": "S3 Bucket definition missing explicit BlockPublicAccess configuration."
        })

    return violations


def scan_aws_workspace(target_path: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            fp = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in {".py", ".ts", ".js", ".tf", ".json", ".yaml", ".yml"}:
                violations.extend(audit_aws_file(fp))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AWS security and architecture hygiene.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = audit_aws_file(target)
    else:
        violations = scan_aws_workspace(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== AWS Architecture Hygiene Audit: {target} ===")
        if not violations:
            print("[PASS] AWS architecture hygiene verified. Zero static keys or public storage risks.")
        else:
            print(f"[FAIL] Found {len(violations)} AWS hygiene violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
