#!/usr/bin/env python3
"""
verify_full_scale_orchestration.py - Audits repository readiness for Full-Scale Mode,
verifying the 32-skill registry, Autonomous Skill Resonance (ASR), and token budgeting.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

REQUIRED_SKILLS: Set[str] = {
    # Original 22 Skills
    "3d",
    "ai",
    "anti-slop",
    "api-design",
    "backend",
    "continuous-learning",
    "database",
    "devops",
    "frontend",
    "full-scale-mode",
    "fullstack",
    "git-workflow",
    "observability",
    "performance",
    "production-etiquette",
    "prompt-polish",
    "qa",
    "refactor",
    "research",
    "security",
    "ui",
    "world-class-engineering",
    # 10 Expanded Skills
    "aws",
    "data-pipelines",
    "firebase",
    "gcp",
    "i18n",
    "project-skills",
    "routing",
    "state-management",
    "supabase",
    "testing",
    # Mobile, Web UI & Local LLM Skills
    "local-llm",
    "mobile-ui",
    "web-ui"
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
            "message": f"Missing required skill(s) in registry ({len(missing_skills)} missing): {sorted(list(missing_skills))}",
            "file": str(skills_dir)
        })

    return violations


def detect_platform_target(repo_root: Path) -> str:
    """Classifies repository into 'mobile', 'web', 'universal', or 'auto'."""
    has_mobile = (
        any((repo_root / d).exists() for d in ["ios", "android", "expo"])
        or any((repo_root / f).exists() for f in ["app.json", "pubspec.yaml", "Podfile"])
    )
    has_web = (
        any((repo_root / f).exists() for f in [
            "tailwind.config.js", "tailwind.config.ts", "postcss.config.js",
            "next.config.js", "next.config.ts", "next.config.mjs",
            "vite.config.js", "vite.config.ts"
        ])
        or (repo_root / "styles").exists()
        or (repo_root / "public").exists()
    )
    if has_mobile and has_web:
        return "universal"
    if has_mobile:
        return "mobile"
    if has_web:
        return "web"
    return "auto"


def analyze_skill_resonance(repo_root: Path, target_platform: str = "auto") -> Dict[str, Any]:
    """Autonomous Skill Resonance (ASR): Fingerprints repository and activates resonant skills,
    applying Platform Domain Specialization (PDS) to prune cross-platform token waste."""
    activated_skills = {"prompt-polish", "qa", "security", "git-workflow", "world-class-engineering"}
    pruned_skills = set()

    # Determine effective platform
    if target_platform == "auto":
        platform = detect_platform_target(repo_root)
    else:
        platform = target_platform

    # Cloud & Serverless Ingress
    if any((repo_root / f).exists() for f in ["cloudbuild.yaml", "app.yaml"]) or (repo_root / "Dockerfile").exists():
        activated_skills.update(["gcp", "devops"])
    if any((repo_root / f).exists() for f in ["cdk.json", "template.yaml"]) or (repo_root / "terraform").exists():
        activated_skills.update(["aws", "devops"])
    if (repo_root / "firebase.json").exists() or (repo_root / "firestore.rules").exists():
        activated_skills.add("firebase")
    if (repo_root / "supabase").exists():
        activated_skills.update(["supabase", "database"])

    # Routing & Client Architecture
    if (repo_root / "app").exists() or (repo_root / "src" / "app").exists() or (repo_root / "routes").exists():
        activated_skills.update(["routing", "frontend", "state-management", "ui"])

    # Internationalization
    if any((repo_root / d).exists() for d in ["messages", "locales", "translations"]):
        activated_skills.add("i18n")

    # Data Pipelines
    if any((repo_root / f).exists() for f in ["duckdb", "pipeline", "pipelines"]):
        activated_skills.add("data-pipelines")

    # Local LLM & Quantized Inference
    if any((repo_root / f).exists() for f in ["Modelfile", "modelfile"]) or any((repo_root / d).exists() for d in ["models", "gguf"]):
        activated_skills.add("local-llm")

    # Platform Domain Specialization (PDS) & Token Quota Preservation (TQP)
    has_mobile_files = (
        any((repo_root / d).exists() for d in ["ios", "android", "expo"])
        or any((repo_root / f).exists() for f in ["app.json", "pubspec.yaml", "Podfile"])
    )
    has_web_files = (
        any((repo_root / f).exists() for f in [
            "tailwind.config.js", "tailwind.config.ts", "postcss.config.js",
            "next.config.js", "next.config.ts", "next.config.mjs",
            "vite.config.js", "vite.config.ts"
        ])
        or (repo_root / "styles").exists()
        or (repo_root / "public").exists()
    )

    if platform == "mobile":
        activated_skills.add("mobile-ui")
        if "web-ui" in activated_skills:
            activated_skills.remove("web-ui")
        pruned_skills.add("web-ui")
    elif platform == "web":
        activated_skills.add("web-ui")
        if "mobile-ui" in activated_skills:
            activated_skills.remove("mobile-ui")
        pruned_skills.add("mobile-ui")
    elif platform == "universal":
        if has_mobile_files:
            activated_skills.add("mobile-ui")
        if has_web_files:
            activated_skills.add("web-ui")
    else:  # auto / fallback
        if has_mobile_files:
            activated_skills.add("mobile-ui")
        if has_web_files:
            activated_skills.add("web-ui")

    # Token savings estimate: ~1,850 tokens per pruned specialized skill (~7,000 characters)
    token_quota_saved = len(pruned_skills) * 1850

    return {
        "platform_target": platform,
        "resonant_skills_count": len(activated_skills),
        "resonant_skills": sorted(list(activated_skills)),
        "pruned_skills": sorted(list(pruned_skills)),
        "token_quota_saved": token_quota_saved
    }


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
        "Phase 1", "Phase 2", "Phase 3"
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
    parser.add_argument(
        "--platform",
        choices=["auto", "mobile", "web", "universal"],
        default="auto",
        help="Specify or override target platform for Platform Domain Specialization (PDS)"
    )
    parser.add_argument(
        "--strict-platform",
        action="store_true",
        help="Enforce strict platform isolation (flags cross-platform skill bleed)"
    )
    parser.add_argument("--asr", action="store_true", help="Run Autonomous Skill Resonance analysis")
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
        if args.strict_platform:
            if "mobile-ui" in args.prompt and "web-ui" in args.prompt:
                all_violations.append({
                    "rule": "CROSS-PLATFORM-SKILL-BLEED",
                    "message": "Prompt mixes both /mobile-ui and /web-ui. Isolate tracks to prevent token waste."
                })

    # 3. Audit plan if provided
    if args.plan:
        plan_path = Path(args.plan).resolve()
        if plan_path.exists():
            plan_text = plan_path.read_text(encoding="utf-8")
            all_violations.extend(audit_phased_plan(plan_text))
            if args.strict_platform:
                if "/mobile-ui" in plan_text and "/web-ui" in plan_text and "Universal" not in plan_text:
                    all_violations.append({
                        "rule": "CROSS-PLATFORM-SKILL-BLEED",
                        "message": "Plan references both /mobile-ui and /web-ui without universal track partitioning."
                    })
        else:
            all_violations.append({
                "rule": "PLAN-NOT-FOUND",
                "message": f"Specified plan file not found: {plan_path}"
            })

    asr_data = analyze_skill_resonance(repo_root, target_platform=args.platform)

    if args.json:
        print(json.dumps({
            "total_violations": len(all_violations),
            "violations": all_violations,
            "required_skills_count": len(REQUIRED_SKILLS),
            "asr": asr_data
        }, indent=2))
    else:
        print(f"=== Full-Scale Mode Orchestration Audit: {repo_root} ===")
        print(f"Verified Skills in Registry: {len(REQUIRED_SKILLS)} required skills")
        if args.asr:
            print(f"Platform Domain Specialization: Target = [{asr_data['platform_target'].upper()}]")
            print(f"Autonomous Skill Resonance (ASR): Activated {asr_data['resonant_skills_count']} skills:")
            for s in asr_data['resonant_skills']:
                print(f"  • /{s}")
            if asr_data.get('pruned_skills'):
                print(f"Token Quota Preservation (TQP): Pruned {len(asr_data['pruned_skills'])} inapplicable skill(s):")
                for p in asr_data['pruned_skills']:
                    print(f"  ✕ /{p} (pruned to conserve context)")
                print(f"Estimated Token Savings: ~{asr_data['token_quota_saved']} tokens per subagent turn")
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
