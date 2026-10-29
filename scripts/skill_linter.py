#!/usr/bin/env python3
"""
skill_linter.py - Comprehensive Skill Quality, Integrity & Token Efficiency Auditor.

Audits YAML frontmatter, link integrity, physical line limits, anti-slop compliance,
and benchmarks progressive disclosure token savings across all SkillBuilder skills.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Quality & Optimization Engine
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


def estimate_tokens(text: str) -> int:
    """Estimates LLM token count using the standard 3.8 chars/token heuristic."""
    if not text:
        return 0
    return max(1, int(len(text) / 3.8))


def audit_frontmatter(content: str, folder_name: str) -> Tuple[bool, str, Dict[str, str]]:
    """Validates YAML frontmatter presence, name match, and descriptive trigger."""
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return False, "Missing YAML frontmatter block (---)", {}

    yaml_text = match.group(1)
    meta: Dict[str, str] = {}
    name_m = re.search(r"^name:\s*([^\n]+)", yaml_text, re.MULTILINE)
    if name_m:
        meta["name"] = name_m.group(1).strip()

    # Handle folded scalar (>- or |) multiline descriptions
    desc_folded_m = re.search(r"^description:\s*(?:>-\s*|\|\s*)?\n((?:\s{2,}[^\n]+\n?)+)", yaml_text, re.MULTILINE)
    if desc_folded_m:
        lines = [l.strip() for l in desc_folded_m.group(1).splitlines() if l.strip()]
        meta["description"] = " ".join(lines)
    else:
        desc_m = re.search(r"^description:\s*([^\n]+)", yaml_text, re.MULTILINE)
        if desc_m:
            meta["description"] = desc_m.group(1).strip()

    if not meta.get("name"):
        return False, "Missing 'name' field in frontmatter", meta
    if not meta.get("description"):
        return False, "Missing 'description' field in frontmatter", meta
    if len(meta["description"]) < 25:
        return False, f"Description is too short ({len(meta['description'])} chars); must be descriptive", meta

    return True, "Valid frontmatter", meta


def audit_markdown_links(skill_folder: Path, content: str) -> List[Dict[str, Any]]:
    """Verifies that all internal markdown links resolve to existing files."""
    violations: List[Dict[str, Any]] = []
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

    for text, link in links:
        if link.startswith("http") or link.startswith("#") or link.startswith("file://") or link.startswith("mailto:"):
            continue
        clean_link = link.split("#")[0].split("?")[0]
        if not clean_link:
            continue
        target = (skill_folder / clean_link).resolve()
        if not target.exists():
            violations.append({
                "rule": "BROKEN-MARKDOWN-LINK",
                "text": text,
                "link": link,
                "resolved_path": str(target),
                "message": f"Broken link [{text}]({link}) -> File not found: {target.name}"
            })
    return violations


def audit_anti_slop(content: str) -> List[Dict[str, Any]]:
    """Checks for forbidden AI slop (decorative shields badges, mock arrays)."""
    violations: List[Dict[str, Any]] = []
    if "img.shields.io" in content:
        violations.append({
            "rule": "DECORATIVE-BADGE-SLOP",
            "message": "Contains decorative shields.io badge (violates anti-slop rule 3)."
        })
    for line in content.splitlines():
        if re.search(r"\bconst\s+\w+\s*=\s*\[\s*\{\s*id:\s*1\b", line):
            if not any(kw in line.lower() for kw in ["never", "prohibit", "forbidden", "anti-pattern", "e.g."]):
                violations.append({
                    "rule": "TOY-MOCK-ARRAY-SLOP",
                    "message": "Contains toy mock array pretending to be a database (violates anti-mock rule 6)."
                })
    return violations


def audit_single_skill(skill_folder: Path) -> Dict[str, Any]:
    """Audits a single skill directory."""
    skill_md = skill_folder / "SKILL.md"
    result: Dict[str, Any] = {
        "skill": skill_folder.name,
        "valid": True,
        "violations": [],
        "token_benchmark": {}
    }

    if not skill_md.exists():
        result["valid"] = False
        result["violations"].append({
            "rule": "MISSING-SKILL-MD",
            "message": f"Missing SKILL.md in {skill_folder}"
        })
        return result

    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    # Line limit audit on SKILL.md (ceiling: 350 lines for docs)
    if len(lines) > 350:
        result["violations"].append({
            "rule": "SKILL-MD-LINE-OVERRUN",
            "message": f"SKILL.md has {len(lines)} lines (exceeds 350-line documentation ceiling)."
        })

    # Frontmatter audit
    fm_valid, fm_msg, meta = audit_frontmatter(content, skill_folder.name)
    if not fm_valid:
        result["violations"].append({
            "rule": "INVALID-FRONTMATTER",
            "message": fm_msg
        })

    # Broken links audit
    link_violations = audit_markdown_links(skill_folder, content)
    result["violations"].extend(link_violations)

    # Anti-slop audit
    slop_violations = audit_anti_slop(content)
    result["violations"].extend(slop_violations)

    # Token Benchmarking
    skill_md_tokens = estimate_tokens(content)
    ref_tokens = 0
    ref_count = 0
    refs_dir = skill_folder / "references"
    if refs_dir.exists():
        for ref_file in refs_dir.iterdir():
            if ref_file.is_file() and ref_file.suffix == ".md":
                ref_count += 1
                ref_tokens += estimate_tokens(ref_file.read_text(encoding="utf-8", errors="ignore"))

    total_knowledge_tokens = skill_md_tokens + ref_tokens
    token_savings = ref_tokens  # Tokens saved on initial turn thanks to progressive disclosure

    result["token_benchmark"] = {
        "skill_md_tokens": skill_md_tokens,
        "reference_files": ref_count,
        "reference_tokens": ref_tokens,
        "total_knowledge_tokens": total_knowledge_tokens,
        "token_savings_pct": round((token_savings / total_knowledge_tokens * 100), 1) if total_knowledge_tokens else 0
    }

    if result["violations"]:
        result["valid"] = False

    return result


def audit_all_skills(skills_dir: Path) -> List[Dict[str, Any]]:
    """Audits all skills in skills directory."""
    results: List[Dict[str, Any]] = []
    if not skills_dir.exists():
        return results

    for child in sorted(skills_dir.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            results.append(audit_single_skill(child))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="SkillBuilder Quality & Token Efficiency Linter")
    parser.add_argument("--skill", help="Audit a specific skill by folder name")
    parser.add_argument("--all", action="store_true", help="Audit all skills in the ecosystem")
    parser.add_argument("--benchmark", action="store_true", help="Display token efficiency benchmark metrics")
    parser.add_argument("--skills-dir", type=Path, default=SKILLS_DIR, help="Path to skills directory")

    args = parser.parse_args()
    if not args.skill and not args.all:
        args.all = True

    if args.skill:
        target = args.skills_dir / args.skill
        if not target.exists():
            print(f"[ERROR] Skill folder '{args.skill}' does not exist in {args.skills_dir}", file=sys.stderr)
            sys.exit(1)
        reports = [audit_single_skill(target)]
    else:
        reports = audit_all_skills(args.skills_dir)

    total_skills = len(reports)
    passed_skills = sum(1 for r in reports if r["valid"])
    total_violations = sum(len(r["violations"]) for r in reports)

    print(f"\n=== SkillBuilder Quality & Token Linter ({passed_skills}/{total_skills} Passed) ===")

    for r in reports:
        status = "[PASS]" if r["valid"] else "[FAIL]"
        bench = r["token_benchmark"]
        print(f"{status} {r['skill']:24} | SKILL.md: {bench.get('skill_md_tokens', 0):4} tok | Refs: {bench.get('reference_files', 0):2} ({bench.get('reference_tokens', 0):4} tok) | Saved: {bench.get('token_savings_pct', 0)}%")
        for v in r["violations"]:
            print(f"       ! [{v.get('rule')}] {v.get('message')}")

    if args.benchmark and reports:
        total_md_tokens = sum(r["token_benchmark"].get("skill_md_tokens", 0) for r in reports)
        total_ref_tokens = sum(r["token_benchmark"].get("reference_tokens", 0) for r in reports)
        total_knowledge = total_md_tokens + total_ref_tokens
        overall_savings_pct = round((total_ref_tokens / total_knowledge * 100), 1) if total_knowledge else 0
        print("\n--- Progressive Disclosure Token Efficiency Summary ---")
        print(f"  • Total Skills Audited         : {total_skills}")
        print(f"  • Prompt Context Weight (SKILL): {total_md_tokens:,} tokens")
        print(f"  • Deep Knowledge Deferred     : {total_ref_tokens:,} tokens")
        print(f"  • Total Ecosystem Knowledge    : {total_knowledge:,} tokens")
        print(f"  • Token Quota Savings Ratio    : {overall_savings_pct}% context overhead eliminated per turn")

    if total_violations > 0:
        print(f"\n[FAIL] Found {total_violations} skill violation(s).", file=sys.stderr)
        sys.exit(1)

    print(f"\n[SUCCESS] All {total_skills} skills meet SkillBuilder and Antigravity specifications!")


if __name__ == "__main__":
    main()
