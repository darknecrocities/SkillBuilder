#!/usr/bin/env python3
"""
verify_full_scale_orchestration.py - Audits repository readiness for Full-Scale Mode,
verifying the 36-skill registry, cross-agent sync, Autonomous Skill Resonance (ASR),
Orchestration Memory, and Harness Engineering standards.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set

REQUIRED_SKILLS: Set[str] = {
    "3d", "ai", "anti-slop", "antigravity-automation", "api-design", "aws", "backend", "continuous-learning",
    "data-pipelines", "database", "devops", "firebase", "frontend", "full-scale-mode",
    "fullstack", "gcp", "git-workflow", "i18n", "local-llm", "mobile-ui", "observability",
    "performance", "production-etiquette", "project-skills", "prompt-polish", "qa",
    "refactor", "research", "routing", "security", "state-management", "supabase",
    "testing", "ui", "web-ui", "world-class-engineering",
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


def audit_cross_skill_sync(repo_root: Path) -> List[Dict[str, Any]]:
    """Verifies that AGENTS.md, rules/AGENTS.md, plugin.json, and core orchestrators stay synchronized."""
    violations: List[Dict[str, Any]] = []
    root_agents = repo_root / "AGENTS.md"
    rules_agents = repo_root / "rules" / "AGENTS.md"
    if root_agents.exists() and rules_agents.exists():
        if root_agents.read_text(encoding="utf-8") != rules_agents.read_text(encoding="utf-8"):
            violations.append({
                "rule": "CROSS-SKILL-SYNC-DRIFT",
                "message": "AGENTS.md and rules/AGENTS.md have drifted out of sync.",
                "file": str(rules_agents),
            })

    sync_checks = [
        (repo_root / "plugin.json", "36 modular skills"),
        (repo_root / "skills" / "full-scale-mode" / "SKILL.md", "36 modular engineering skills"),
        (repo_root / "skills" / "world-class-engineering" / "SKILL.md", "The 36 Modular Engineering Skills"),
    ]
    for fpath, expected_phrase in sync_checks:
        if fpath.exists() and expected_phrase.lower() not in fpath.read_text(encoding="utf-8").lower():
            violations.append({
                "rule": "CROSS-SKILL-SYNC-DRIFT",
                "message": f"{fpath.name} is missing synchronized registry phrase '{expected_phrase}'.",
                "file": str(fpath),
            })
    return violations


def audit_orchestration_memory(repo_root: Path) -> List[Dict[str, Any]]:
    """Audits .agents/memory/orchestration_state.json for schema compliance if present."""
    violations: List[Dict[str, Any]] = []
    mem_file = repo_root / ".agents" / "memory" / "orchestration_state.json"
    if not mem_file.exists():
        return violations

    try:
        data = json.loads(mem_file.read_text(encoding="utf-8"))
        required_fields = ["version", "session_id", "current_stage", "triad_phase", "milestones", "file_registry"]
        for rf in required_fields:
            if rf not in data:
                violations.append({
                    "rule": "INVALID-ORCHESTRATION-MEMORY",
                    "message": f"Memory state missing required field: '{rf}'",
                    "file": str(mem_file)
                })
        valid_stages = ["DISCOVER", "PLAN", "BUILD", "VERIFY", "LOOP", "RELEASE"]
        if data.get("current_stage") not in valid_stages:
            violations.append({
                "rule": "INVALID-ORCHESTRATION-STAGE",
                "message": f"Unknown orchestration stage: '{data.get('current_stage')}'",
                "file": str(mem_file)
            })
    except json.JSONDecodeError:
        violations.append({
            "rule": "CORRUPT-ORCHESTRATION-MEMORY",
            "message": "orchestration_state.json contains invalid JSON syntax.",
            "file": str(mem_file)
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

    platform = detect_platform_target(repo_root) if target_platform == "auto" else target_platform

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

    # Internationalization & Pipelines
    if any((repo_root / d).exists() for d in ["messages", "locales", "translations"]):
        activated_skills.add("i18n")
    if any((repo_root / f).exists() for f in ["duckdb", "pipeline", "pipelines"]):
        activated_skills.add("data-pipelines")

    # Local LLM & Quantized Inference
    if any((repo_root / f).exists() for f in ["Modelfile", "modelfile"]) or any((repo_root / d).exists() for d in ["models", "gguf"]):
        activated_skills.add("local-llm")

    # PDS Platform Domain Specialization
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
        activated_skills.discard("web-ui")
        pruned_skills.add("web-ui")
    elif platform == "web":
        activated_skills.add("web-ui")
        activated_skills.discard("mobile-ui")
        pruned_skills.add("mobile-ui")
    else:  # universal or auto
        if has_mobile_files:
            activated_skills.add("mobile-ui")
        if has_web_files:
            activated_skills.add("web-ui")

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
    """Validates that implementation plan covers either the 3-Phase Triad or 5-Stage Lifecycle."""
    violations: List[Dict[str, Any]] = []
    has_3phases = all(re.search(rf"\bPhase {i}\b", plan_content, re.IGNORECASE) for i in [1, 2, 3])
    has_5stages = all(re.search(rf"\bStage {i}\b", plan_content, re.IGNORECASE) for i in range(1, 6))

    if not (has_3phases or has_5stages):
        violations.append({
            "rule": "MISSING-PROJECT-PHASE",
            "message": "Plan must define either 3 Triad Phases (Phase 1-3) or 5 Orchestration Stages (Stage 1-5)."
        })
    return violations


def build_parser() -> argparse.ArgumentParser:
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
    parser.add_argument("--memory", action="store_true", help="Audit orchestration memory hygiene")
    parser.add_argument("--harness", action="store_true", help="Run multi-tier evaluation harness")
    parser.add_argument("--json", action="store_true", help="Output findings in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero code on violations")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.path).resolve()
    all_violations: List[Dict[str, Any]] = []

    # 1. Audit registry & cross-skill synchronization
    all_violations.extend(audit_skill_registry(repo_root))
    all_violations.extend(audit_cross_skill_sync(repo_root))

    # 2. Audit orchestration memory if requested or present
    if args.memory or (repo_root / ".agents" / "memory" / "orchestration_state.json").exists():
        all_violations.extend(audit_orchestration_memory(repo_root))

    # 3. Audit prompt if provided
    if args.prompt:
        all_violations.extend(audit_subagent_prompt(args.prompt))
        if args.strict_platform and "mobile-ui" in args.prompt and "web-ui" in args.prompt:
            all_violations.append({
                "rule": "CROSS-PLATFORM-SKILL-BLEED",
                "message": "Prompt mixes both /mobile-ui and /web-ui. Isolate tracks to prevent token waste."
            })

    # 4. Audit plan if provided
    if args.plan:
        plan_path = Path(args.plan).resolve()
        if plan_path.exists():
            plan_text = plan_path.read_text(encoding="utf-8")
            all_violations.extend(audit_phased_plan(plan_text))
            if args.strict_platform and "/mobile-ui" in plan_text and "/web-ui" in plan_text and "Universal" not in plan_text:
                all_violations.append({
                    "rule": "CROSS-PLATFORM-SKILL-BLEED",
                    "message": "Plan references both /mobile-ui and /web-ui without universal track partitioning."
                })
        else:
            all_violations.append({
                "rule": "PLAN-NOT-FOUND",
                "message": f"Specified plan file not found: {plan_path}"
            })

    # 5. Run evaluation harness if requested
    if args.harness:
        sys.path.insert(0, str(repo_root / "skills" / "full-scale-mode" / "scripts"))
        try:
            from orchestration_harness import run_harness_suite
            harness_res = run_harness_suite(repo_root)
            all_violations.extend(harness_res.get("violations", []))
        except ImportError:
            all_violations.append({
                "rule": "HARNESS-IMPORT-ERROR",
                "message": "Could not import orchestration_harness runner.",
                "file": str(repo_root)
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
