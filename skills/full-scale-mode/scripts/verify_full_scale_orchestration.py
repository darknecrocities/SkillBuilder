#!/usr/bin/env python3
"""
verify_full_scale_orchestration.py - Audits repository readiness for Full-Scale Mode,
verifying skill registry completeness, phase planning standards, and subagent token budgeting.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

REQUIRED_SKILLS = {
    "world-class-engineering",
    "full-scale-mode",
    "anti-slop",
    "research",
    "qa",
    "ui",
    "3d",
    "frontend",
    "backend",
    "security",
    "fullstack",
    "database",
    "devops",
    "ai",
    "prompt-polish",
    "production-etiquette",
    "performance",
    "api-design",
    "observability",
    "continuous-learning",
    "refactor",
    "git-workflow"
}

BLOATED_FILLER_PATTERNS = re.compile(
    r"\b(?:hello\s+subagent|could\s+you\s+please\s+help|feel\s+free\s+to|hope\s+you\s+are\s+doing\s+well)\b",
    re.IGNORECASE
)


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, int(len(text) / 3.8))


def audit_skill_registry(repo_root: Path) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    skills_dir = repo_root / "skills"
    if not skills_dir.exists():
        return [{
            "rule": "MISSING-SKILLS-DIRECTORY",
            "message": "Root 'skills/' directory not found.",
            "file": str(skills_dir)
        }]

    existing_skills = {p.name for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    missing_skills = REQUIRED_SKILLS - existing_skills

    if missing_skills:
        violations.append({
            "rule": "INCOMPLETE-SKILL-REGISTRY",
            "message": f"Missing required skill(s) in registry: {sorted(list(missing_skills))}",
            "file": str(skills_dir)
        })

    return violations


def audit_subagent_prompt(prompt_text: str, budget_limit: int = 1500) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    token_count = estimate_tokens(prompt_text)

    if token_count > budget_limit:
        violations.append({
            "rule": "SUBAGENT-TOKEN-BUDGET-EXCEEDED",
            "message": f"Prompt estimated at {token_count} tokens, exceeding ceiling of {budget_limit}.",
            "tokens": token_count,
            "budget": budget_limit
        })

    filler_match = BLOATED_FILLER_PATTERNS.search(prompt_text)
    if filler_match:
        violations.append({
            "rule": "CONVERSATIONAL-TOKEN-BLOAT",
            "message": f"Conversational filler detected: '{filler_match.group(0)}'. Use dense directives.",
            "snippet": filler_match.group(0)
        })

    return violations


def audit_phased_plan(plan_content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []
    required_phases = [
        "Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6"
    ]
    for phase in required_phases:
        if not re.search(rf"\b{re.escape(phase)}\b", plan_content, re.IGNORECASE):
            violations.append({
                "rule": "MISSING-PROJECT-PHASE",
                "message": f"Implementation plan lacks required phase definition: '{phase}'."
            })
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit workspace for Full-Scale Mode orchestration & token standards."
    )
    parser.add_argument("--path", "-p", default=".", help="Root repository path")
    parser.add_argument("--prompt", type=str, help="Subagent prompt string to audit for token budget")
    parser.add_argument("--plan", type=str, help="Path to implementation plan markdown to audit")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero code on violations")
    args = parser.parse_args()

    repo_root = Path(args.path).resolve()
    all_violations: List[Dict[str, Any]] = []

    # 1. Audit registry
    all_violations.extend(audit_skill_registry(repo_root))

    # 2. Audit prompt if provided
    if args.prompt:
        all_violations.extend(audit_subagent_prompt(args.prompt))

    # 3. Audit plan if provided
    if args.plan:
        plan_path = Path(args.plan).resolve()
        if plan_path.exists():
            all_violations.extend(audit_phased_plan(plan_path.read_text(encoding="utf-8")))
        else:
            all_violations.append({
                "rule": "PLAN-NOT-FOUND",
                "message": f"Specified plan file not found: {plan_path}"
            })

    if args.json:
        print(json.dumps({
            "total_violations": len(all_violations),
            "violations": all_violations,
            "required_skills_count": len(REQUIRED_SKILLS)
        }, indent=2))
    else:
        print(f"=== Full-Scale Mode Orchestration Audit: {repo_root} ===")
        print(f"Verified Skills in Registry: {len(REQUIRED_SKILLS)} required skills")
        if not all_violations:
            print("[PASS] Workspace and orchestration inputs comply with Full-Scale standards.")
        else:
            print(f"[FAIL] Found {len(all_violations)} orchestration violation(s):")
            for v in all_violations:
                print(f"  - [{v.get('rule', 'UNKNOWN')}] {v.get('message', '')}")

    if args.strict and all_violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
