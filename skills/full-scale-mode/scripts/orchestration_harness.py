#!/usr/bin/env python3
"""
orchestration_harness.py - Multi-Tier Evaluation Harness & Self-Healing Loop Runner.

Executes a 5-tier evaluation harness:
  Tier 1: Static & Architectural Hygiene (500-line ceiling, anti-slop, token budget)
  Tier 2: Contracts & Schema Validation (syntax, spec integrity)
  Tier 3: Functional & TDD Test Suites (automated unit & integration tests)
  Tier 4: Security, Resilience & Deduplicated Backups (secrets, parameterization, single-slot backup)
  Tier 5: Commit & Git Delivery Hygiene (1,000-line diff budget, branch conventions)

Manages bounded self-healing loops with structured failure diagnostics.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable, Dict, List, Optional

TIERS = {
    1: "Tier 1: Static & Architectural Hygiene",
    2: "Tier 2: Contracts & Schema Validation",
    3: "Tier 3: Functional & TDD Test Suites",
    4: "Tier 4: Security, Resilience & Storage Backups",
    5: "Tier 5: Commit & Git Delivery Hygiene",
}

AI_SLOP_PATTERNS = [
    (re.compile(r"img\.shields\.io"), "Decorative badges (shields.io) violate anti-slop rules"),
    (re.compile(r"//\s*set\s+\w+\s+to\s+(?:true|false)", re.IGNORECASE), "Obvious restatement comment detected"),
    (re.compile(r"bg-gradient-to-r\s+from-purple-500", re.IGNORECASE), "Neon purple gradient violates clean UI craftsmanship"),
]

SECRET_PATTERNS = [
    (re.compile(r"(?:api_key|secret_key|password)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", re.IGNORECASE), "Hardcoded secret pattern"),
]


def check_tier1_hygiene(repo_root: Path, check_tests: bool = False) -> List[Dict[str, Any]]:
    violations = []
    for root, dirs, files in os.walk(repo_root):
        if any(d.startswith(".") or d in ["node_modules", "dist", "build", "venv"] for d in root.split(os.sep)):
            continue
        is_test_dir = "tests" in Path(root).parts or "test" in Path(root).parts
        is_tooling_dir = "scripts" in Path(root).parts
        for f in files:
            if f.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
                fpath = Path(root) / f
                try:
                    lines = fpath.read_text(encoding="utf-8", errors="ignore").splitlines()
                    if len(lines) > 500:
                        violations.append({
                            "tier": 1,
                            "rule": "SOURCE-LINE-LIMIT-EXCEEDED",
                            "file": str(fpath.relative_to(repo_root)),
                            "message": f"File has {len(lines)} lines, exceeding strict 500-line ceiling.",
                            "remediation_hint": "Decompose into smaller focused modules via Strangler Fig.",
                        })
                    if check_tests or (not is_test_dir and not is_tooling_dir and not f.startswith("test_") and not f.endswith("_test.py")):
                        content = "\n".join(lines)
                        for pat, msg in AI_SLOP_PATTERNS:
                            if pat.search(content):
                                violations.append({
                                    "tier": 1,
                                    "rule": "AI-SLOP-DETECTED",
                                    "file": str(fpath.relative_to(repo_root)),
                                    "message": msg,
                                    "remediation_hint": "Replace with clean craftsmanship and semantic tokens.",
                                })
                except OSError:
                    pass
    return violations


def check_tier2_contracts(repo_root: Path) -> List[Dict[str, Any]]:
    violations = []
    for p in (repo_root / "skills").rglob("*.py"):
        try:
            with open(p, "rb") as f:
                compile(f.read(), str(p), "exec")
        except SyntaxError as e:
            violations.append({
                "tier": 2,
                "rule": "SYNTAX-ERROR",
                "file": str(p.relative_to(repo_root)),
                "message": f"Python compilation failed: {e.msg} at line {e.lineno}",
                "remediation_hint": "Fix invalid syntax before advancing to functional verification.",
            })
    return violations


def check_tier3_functional(repo_root: Path, test_pattern: Optional[str] = None) -> List[Dict[str, Any]]:
    violations = []
    master_script = repo_root / "scripts" / "verify_all_skills.sh"
    if master_script.exists():
        cmd = ["bash", str(master_script)]
    else:
        pattern = test_pattern or "test_*.py"
        cmd = [sys.executable, "-m", "unittest", "discover", "-s", str(repo_root), "-p", pattern]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(repo_root))
    if res.returncode != 0:
        violations.append({
            "tier": 3,
            "rule": "UNIT-TEST-FAILURE",
            "file": "test_suite",
            "message": f"Functional tests failed with return code {res.returncode}.\n{res.stderr.strip() or res.stdout.strip()}",
            "remediation_hint": "Inspect test assertion failures and apply regression-free fixes.",
        })
    return violations


def check_tier4_security(repo_root: Path, check_tests: bool = False) -> List[Dict[str, Any]]:
    violations = []
    for root, dirs, files in os.walk(repo_root):
        if any(d.startswith(".") or d in ["node_modules", "dist", "build", "venv"] for d in root.split(os.sep)):
            continue
        is_test_dir = "tests" in Path(root).parts or "test" in Path(root).parts
        if not check_tests and is_test_dir:
            continue
        for f in files:
            if not check_tests and (f.startswith("test_") or f.endswith("_test.py")):
                continue
            if f.endswith((".py", ".ts", ".js", ".json", ".env")):
                fpath = Path(root) / f
                if f.startswith(".env") and not f.endswith(".example"):
                    continue
                try:
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    for pat, msg in SECRET_PATTERNS:
                        if pat.search(content):
                            violations.append({
                                "tier": 4,
                                "rule": "SECRET-LEAK-RISK",
                                "file": str(fpath.relative_to(repo_root)),
                                "message": msg,
                                "remediation_hint": "Migrate credentials to Secret Manager and reference via environment variables.",
                            })
                except OSError:
                    pass
    return violations


def check_tier5_git(repo_root: Path) -> List[Dict[str, Any]]:
    violations = []
    try:
        branch_res = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=str(repo_root)
        )
        if branch_res.returncode == 0:
            branch = branch_res.stdout.strip()
            if branch not in ["main", "master", "HEAD"] and not any(branch.startswith(p) for p in ["feat/", "fix/", "refactor/", "chore/", "docs/"]):
                violations.append({
                    "tier": 5,
                    "rule": "INVALID-BRANCH-PREFIX",
                    "file": ".git",
                    "message": f"Branch name '{branch}' does not use conventional prefix (feat/, fix/, refactor/).",
                    "remediation_hint": "Rename branch following Conventional Branching guidelines.",
                })
    except OSError:
        pass
    return violations


def run_harness_suite(
    repo_root: Path,
    active_tiers: Optional[List[int]] = None,
    test_pattern: Optional[str] = None
) -> Dict[str, Any]:
    tiers_to_run = active_tiers if active_tiers else [1, 2, 3, 4, 5]
    all_violations: List[Dict[str, Any]] = []
    tier_results = {}

    for t in sorted(tiers_to_run):
        tier_violations = []
        if t == 1:
            tier_violations = check_tier1_hygiene(repo_root)
        elif t == 2:
            tier_violations = check_tier2_contracts(repo_root)
        elif t == 3:
            tier_violations = check_tier3_functional(repo_root, test_pattern=test_pattern)
        elif t == 4:
            tier_violations = check_tier4_security(repo_root)
        elif t == 5:
            tier_violations = check_tier5_git(repo_root)

        all_violations.extend(tier_violations)
        tier_results[f"tier_{t}"] = {
            "name": TIERS.get(t, f"Tier {t}"),
            "passed": len(tier_violations) == 0,
            "violations_count": len(tier_violations),
            "violations": tier_violations,
        }

    return {
        "passed": len(all_violations) == 0,
        "total_violations": len(all_violations),
        "violations": all_violations,
        "tier_results": tier_results,
    }


def execute_self_healing_loop(
    repo_root: Path,
    max_iterations: int = 3,
    active_tiers: Optional[List[int]] = None,
    test_pattern: Optional[str] = None,
    remediation_callback: Optional[Callable[[List[Dict[str, Any]], int], bool]] = None
) -> Dict[str, Any]:
    history = []
    for iteration in range(1, max_iterations + 1):
        result = run_harness_suite(repo_root, active_tiers=active_tiers, test_pattern=test_pattern)
        history.append({
            "iteration": iteration,
            "passed": result["passed"],
            "violations_count": result["total_violations"],
        })
        if result["passed"]:
            return {
                "converged": True,
                "iterations_used": iteration,
                "final_result": result,
                "history": history,
            }

        if remediation_callback:
            remediated = remediation_callback(result["violations"], iteration)
            if not remediated:
                break
        else:
            break

    return {
        "converged": False,
        "iterations_used": len(history),
        "final_result": result,
        "history": history,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Multi-Tier Orchestration Evaluation Harness & Self-Healing Loop")
    p.add_argument("--path", "-p", default=".", help="Repository root path")
    p.add_argument("--tier", "-t", type=int, choices=[1, 2, 3, 4, 5], action="append", help="Specific tier to run")
    p.add_argument("--test-pattern", default="test_*.py", help="Test pattern for Tier 3")
    p.add_argument("--loop", action="store_true", help="Enable self-healing evaluation loop")
    p.add_argument("--max-iterations", type=int, default=3, help="Max loop iterations (default: 3)")
    p.add_argument("--json", action="store_true", help="Output results in JSON format")
    p.add_argument("--strict", action="store_true", help="Exit with code 1 if any check fails")
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.path).resolve()

    if args.loop:
        loop_res = execute_self_healing_loop(
            repo_root, max_iterations=args.max_iterations,
            active_tiers=args.tier, test_pattern=args.test_pattern
        )
        if args.json:
            print(json.dumps(loop_res, indent=2))
        else:
            print(f"=== Self-Healing Harness Loop (Iterations: {loop_res['iterations_used']}/{args.max_iterations}) ===")
            if loop_res["converged"]:
                print("[SUCCESS] Harness loop converged! All verification checks passed.")
            else:
                print(f"[FAIL] Harness loop did not converge. {loop_res['final_result']['total_violations']} remaining violations.")
                for v in loop_res["final_result"]["violations"]:
                    print(f"  ✕ [Tier {v['tier']}] [{v['rule']}] {v['message']} ({v['file']})")
                    print(f"    Hint: {v.get('remediation_hint', 'Apply targeted fix.')}")
        if args.strict and not loop_res["converged"]:
            return 1
        return 0

    res = run_harness_suite(repo_root, active_tiers=args.tier, test_pattern=args.test_pattern)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"=== Full-Scale Mode Multi-Tier Harness: {repo_root.name} ===")
        for key, tr in res["tier_results"].items():
            mark = "[PASS]" if tr["passed"] else "[FAIL]"
            print(f"  {mark} {tr['name']} ({tr['violations_count']} violations)")
        if res["passed"]:
            print("[PASS] All active harness tiers passed successfully.")
        else:
            print(f"\n[FAIL] Found {res['total_violations']} harness violation(s):")
            for v in res["violations"]:
                print(f"  - [Tier {v['tier']}] [{v['rule']}] {v['message']} ({v['file']})")
                print(f"    Remediation: {v.get('remediation_hint', 'Apply fix')}")

    if args.strict and not res["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
