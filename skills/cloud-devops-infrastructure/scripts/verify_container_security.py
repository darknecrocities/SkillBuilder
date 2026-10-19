#!/usr/bin/env python3
"""
CLI utility to audit Dockerfiles for multi-stage structure, non-root USER execution,
and secret leakage risks.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import os
import re
import sys
from typing import Dict, List


def audit_dockerfile_content(content: str, filepath: str) -> List[Dict[str, str]]:
    issues = []

    # 1. Check for USER directive
    has_user_directive = bool(re.search(r"^\s*USER\s+[^\s]+", content, re.MULTILINE | re.IGNORECASE))
    if not has_user_directive:
        issues.append({
            "file": filepath,
            "line": "1",
            "rule": "DOCKER-ROOT-USER",
            "severity": "CRITICAL",
            "message": "Dockerfile does not declare a non-root USER directive. Containers must run as an unprivileged user."
        })

    # 2. Check for multi-stage build (FROM ... AS ...)
    from_matches = re.findall(r"^\s*FROM\s+[^\s]+", content, re.MULTILINE | re.IGNORECASE)
    has_multistage = len(from_matches) > 1 or bool(re.search(r"^\s*FROM\s+.*?\s+AS\s+", content, re.MULTILINE | re.IGNORECASE))
    if not has_multistage:
        issues.append({
            "file": filepath,
            "line": "1",
            "rule": "DOCKER-SINGLE-STAGE",
            "severity": "WARNING",
            "message": "Dockerfile appears to be single-stage. Separate build dependencies from runtime using multi-stage builds."
        })

    # 3. Check for copying .env files
    copy_env = re.search(r"^\s*COPY\s+.*?\.env\b", content, re.MULTILINE | re.IGNORECASE)
    if copy_env:
        line_no = content[:copy_env.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "DOCKER-LEAKED-ENV",
            "severity": "CRITICAL",
            "message": "Dockerfile copies .env into container image context. Never embed secrets in images."
        })

    return issues


def audit_dockerfiles(path: str) -> List[Dict[str, str]]:
    all_issues = []

    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return audit_dockerfile_content(f.read(), path)

    for root, _, files in os.walk(path):
        for f in files:
            if f.lower().startswith("dockerfile"):
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                    all_issues.extend(audit_dockerfile_content(content, full_path))
                except Exception as e:
                    print(f"Warning: Failed reading {full_path}: {e}", file=sys.stderr)

    return all_issues


def main():
    parser = argparse.ArgumentParser(description="Audit Dockerfiles for security best practices.")
    parser.add_argument("--path", "-p", type=str, default=".", help="Path to Dockerfile or directory")
    args = parser.parse_args()

    issues = audit_dockerfiles(args.path)

    if not issues:
        print(f"[PASS] Dockerfile security verification passed for: {args.path}")
        sys.exit(0)

    print(f"\n[FAIL] Detected {len(issues)} container security issue(s):\n" + "=" * 60)
    for issue in issues:
        print(f"[{issue['severity']}] {issue['file']}:{issue['line']} - {issue['rule']}")
        print(f"  {issue['message']}")
    print("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
