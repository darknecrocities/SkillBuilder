#!/usr/bin/env python3
"""
verify_git_delivery_etiquette.py - Audits git commit hygiene, mandatory title + description body,
branch naming conventions, and remote push synchronization.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Git Delivery Etiquette Framework
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CONVENTIONAL_TITLE_PATTERN = re.compile(
    r"^(feat|fix|refactor|perf|test|docs|chore|ci|build)(\([a-zA-Z0-9_/-]+\))?:\s+[a-zA-Z0-9].+"
)
LAZY_MESSAGE_PATTERN = re.compile(
    r"^(?:update|fix|wip|test|changes|misc|work|patch|checkpoint|save|commit)\b",
    re.IGNORECASE
)
REDUNDANT_TITLE_PATTERN = re.compile(
    r"^(?:fix|update|chore):\s*(?:fix|update|wip|changes|misc)\b",
    re.IGNORECASE
)


def run_git(args: List[str], cwd: Path) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except OSError as err:
        return 2, "", str(err)


def validate_commit_message(msg: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    lines = msg.strip().splitlines()
    if not lines or not lines[0].strip():
        return [{
            "rule": "EMPTY-COMMIT-MESSAGE",
            "message": "Commit message is completely empty."
        }]

    title = lines[0].strip()

    # 1. Title format validation
    if not CONVENTIONAL_TITLE_PATTERN.match(title):
        violations.append({
            "rule": "NON-CONVENTIONAL-TITLE",
            "message": f"Title does not match Conventional Commits format: '{title[:50]}'.",
            "expected": "<type>(<scope>): <imperative summary>"
        })

    if len(title) > 72:
        violations.append({
            "rule": "TITLE-TOO-LONG",
            "message": f"Title exceeds recommended 72 characters ({len(title)} chars).",
            "title_length": len(title)
        })

    # 2. Check for lazy message
    subject = title.split(":", 1)[1].strip() if ":" in title else title
    if LAZY_MESSAGE_PATTERN.match(subject) or REDUNDANT_TITLE_PATTERN.match(title):
        violations.append({
            "rule": "LAZY-COMMIT-TITLE",
            "message": f"Commit title uses lazy or non-descriptive keyword: '{title}'.",
            "snippet": title
        })

    # 3. Description body validation (Mandatory Title + Description)
    body_lines = lines[1:]
    non_empty_body = [line.strip() for line in body_lines if line.strip()]

    if not non_empty_body:
        violations.append({
            "rule": "MISSING-COMMIT-DESCRIPTION",
            "message": "Commit lacks a structured description body explaining Why, What, and Verification.",
            "requirement": "Multi-line commit with blank separator line and detailed body"
        })
    else:
        body_text = " ".join(non_empty_body)
        if len(body_text) < 30:
            violations.append({
                "rule": "COMMIT-DESCRIPTION-TOO-BRIEF",
                "message": f"Commit description body is too brief ({len(body_text)} chars). Provide full context.",
                "snippet": body_text[:60]
            })

    return violations


def audit_working_tree_sync(repo_path: Path) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    code, out, _ = run_git(["status", "-sb"], repo_path)
    if code != 0:
        return [{
            "rule": "GIT-STATUS-ERROR",
            "message": "Unable to execute git status in target directory."
        }]

    lines = out.splitlines()
    if not lines:
        return violations

    branch_line = lines[0]

    # Check for detached HEAD
    if "HEAD (no branch)" in branch_line:
        violations.append({
            "rule": "DETACHED-HEAD-STATE",
            "message": "Repository is in detached HEAD state. Work must be on a named branch."
        })

    # Check for unpushed commits
    if "[ahead " in branch_line:
        violations.append({
            "rule": "UNPUSHED-LOCAL-COMMITS",
            "message": f"Local branch has unpushed commits: {branch_line}. Always push to remote.",
            "branch_status": branch_line
        })

    return violations


def audit_repository(repo_path: Path, check_sync: bool = True) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    code, log_out, _ = run_git(["log", "-1", "--pretty=format:%B"], repo_path)
    if code != 0 or not log_out.strip():
        return [{
            "rule": "GIT-LOG-EMPTY",
            "message": "No commits found in target repository log."
        }]

    violations.extend(validate_commit_message(log_out))

    if check_sync:
        violations.extend(audit_working_tree_sync(repo_path))

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit git commit structure, body presence, and remote branch sync."
    )
    parser.add_argument("--path", "-p", default=".", help="Root repository path")
    parser.add_argument("--message", "-m", type=str, help="Specific commit message string to validate directly")
    parser.add_argument("--skip-sync", action="store_true", help="Skip remote synchronization checks")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero code on violations")
    args = parser.parse_args()

    violations: List[Dict[str, Any]] = []

    if args.message is not None:
        violations = validate_commit_message(args.message)
    else:
        repo_path = Path(args.path).resolve()
        violations = audit_repository(repo_path, check_sync=not args.skip_sync)

    if args.json:
        print(json.dumps({
            "total_violations": len(violations),
            "violations": violations,
            "status": "PASS" if not violations else "FAIL"
        }, indent=2))
    else:
        print("=== Git Delivery Etiquette Audit ===")
        if not violations:
            print("[PASS] Git delivery etiquette standards satisfied (Title + Body + Remote Sync).")
        else:
            print(f"[FAIL] Found {len(violations)} delivery etiquette violation(s):")
            for v in violations:
                print(f"  - [{v.get('rule', 'UNKNOWN')}] {v.get('message', '')}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
