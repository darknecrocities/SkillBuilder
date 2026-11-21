#!/usr/bin/env python3
"""
skill_linter.py - Comprehensive Skill Quality, Depth & Anti-Boilerplate Auditor.

Audits YAML frontmatter, link integrity, physical line limits, anti-slop compliance,
reference density (--strict-depth), boilerplate repetition, and progressive-disclosure
token savings across all DarkNecroStack skills.
"""

import argparse
from collections import Counter
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MIN_REF_TOKENS = 100
DEFERRED_DIRS = ("references", "principles", "playbooks")


def estimate_tokens(text: str) -> int:
    """Estimate LLM token count using the standard 3.8 chars/token heuristic."""
    if not text:
        return 0
    return max(1, int(len(text) / 3.8))


def audit_frontmatter(content: str, folder_name: str) -> Tuple[bool, str, Dict[str, str]]:
    """Validate YAML frontmatter presence, name, and descriptive trigger."""
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return False, "Missing YAML frontmatter block (---)", {}

    yaml_text = match.group(1)
    meta: Dict[str, str] = {}
    name_m = re.search(r"^name:\s*([^\n]+)", yaml_text, re.MULTILINE)
    if name_m:
        meta["name"] = name_m.group(1).strip()

    desc_folded_m = re.search(r"^description:\s*(?:>-\s*|\|\s*)?\n((?:\s{2,}[^\n]+\n?)+)", yaml_text, re.MULTILINE)
    if desc_folded_m:
        meta["description"] = " ".join(l.strip() for l in desc_folded_m.group(1).splitlines() if l.strip())
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
    """Verify all internal markdown links resolve to existing files."""
    violations: List[Dict[str, Any]] = []
    for text, link in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content):
        if link.startswith(("http", "#", "file://", "mailto:")):
            continue
        clean_link = link.split("#")[0].split("?")[0]
        if not clean_link:
            continue
        target = (skill_folder / clean_link).resolve()
        if not target.exists():
            violations.append({
                "rule": "BROKEN-MARKDOWN-LINK",
                "message": f"Broken link [{text}]({link}) -> File not found: {target.name}",
            })
    return violations


def audit_anti_slop(content: str) -> List[Dict[str, Any]]:
    """Check for forbidden AI slop (decorative shields badges, mock arrays)."""
    violations: List[Dict[str, Any]] = []
    if "img.shields.io" in content:
        violations.append({"rule": "DECORATIVE-BADGE-SLOP", "message": "Contains decorative shields.io badge."})
    for line in content.splitlines():
        if re.search(r"\bconst\s+\w+\s*=\s*\[\s*\{\s*id:\s*1\b", line):
            if not any(kw in line.lower() for kw in ("never", "prohibit", "forbidden", "anti-pattern", "e.g.")):
                violations.append({"rule": "TOY-MOCK-ARRAY-SLOP", "message": "Contains toy mock array pretending to be a database."})
    return violations


def audit_boilerplate_repetition(content: str) -> List[Dict[str, Any]]:
    """Detect templated copy-paste skill bloat where identical numbered steps repeat across headings."""
    normalized_bullets: Counter[str] = Counter()
    for line in content.splitlines():
        stripped = line.strip()
        if re.match(r"^\d+\.\s+", stripped) and len(stripped) > 45:
            # Strip **topic** emphasis so templated repetition across sections is caught
            canonical = re.sub(r"\*\*[^*]+\*\*", "<TOPIC>", stripped)
            normalized_bullets[canonical] += 1

    repeated = [(pat, count) for pat, count in normalized_bullets.items() if count >= 4]
    if repeated:
        top_pat, top_count = repeated[0]
        return [{
            "rule": "BOILERPLATE-REPETITION-SLOP",
            "message": f"Templated instruction repeated {top_count}x ('{top_pat[:60]}...'); replace repetition with concrete domain guidance.",
        }]
    return []


def collect_deferred_docs(skill_folder: Path) -> Tuple[int, int, List[Dict[str, Any]]]:
    """Count deferred reference/principle/playbook docs and check density."""
    ref_count = 0
    ref_tokens = 0
    shallow_violations: List[Dict[str, Any]] = []
    for sub in DEFERRED_DIRS:
        sub_dir = skill_folder / sub
        if not sub_dir.exists():
            continue
        for md_file in sorted(sub_dir.iterdir()):
            if md_file.is_file() and md_file.suffix == ".md":
                text = md_file.read_text(encoding="utf-8", errors="ignore")
                tokens = estimate_tokens(text)
                ref_count += 1
                ref_tokens += tokens
                if sub == "references" and tokens < MIN_REF_TOKENS:
                    shallow_violations.append({
                        "rule": "SHALLOW-STUB-REFERENCE",
                        "message": f"{sub}/{md_file.name} has only {tokens} tokens (< {MIN_REF_TOKENS} density floor).",
                    })
    return ref_count, ref_tokens, shallow_violations


def audit_single_skill(skill_folder: Path, strict_depth: bool = False) -> Dict[str, Any]:
    """Audit a single skill directory."""
    skill_md = skill_folder / "SKILL.md"
    result: Dict[str, Any] = {"skill": skill_folder.name, "valid": True, "violations": [], "token_benchmark": {}}

    if not skill_md.exists():
        result["valid"] = False
        result["violations"].append({"rule": "MISSING-SKILL-MD", "message": f"Missing SKILL.md in {skill_folder}"})
        return result

    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()
    if len(lines) > 350:
        result["violations"].append({"rule": "SKILL-MD-LINE-OVERRUN", "message": f"SKILL.md has {len(lines)} lines (> 350 cap)."})

    fm_valid, fm_msg, _meta = audit_frontmatter(content, skill_folder.name)
    if not fm_valid:
        result["violations"].append({"rule": "INVALID-FRONTMATTER", "message": fm_msg})

    result["violations"].extend(audit_markdown_links(skill_folder, content))
    result["violations"].extend(audit_anti_slop(content))
    result["violations"].extend(audit_boilerplate_repetition(content))

    skill_md_tokens = estimate_tokens(content)
    ref_count, ref_tokens, shallow_violations = collect_deferred_docs(skill_folder)
    if strict_depth:
        if ref_count == 0:
            result["violations"].append({"rule": "MISSING-DEFERRED-REFERENCES", "message": "Skill lacks deferred references/principles/playbooks."})
        result["violations"].extend(shallow_violations)

    total_knowledge = skill_md_tokens + ref_tokens
    result["token_benchmark"] = {
        "skill_md_tokens": skill_md_tokens,
        "reference_files": ref_count,
        "reference_tokens": ref_tokens,
        "total_knowledge_tokens": total_knowledge,
        "token_savings_pct": round((ref_tokens / total_knowledge * 100), 1) if total_knowledge else 0,
    }
    if result["violations"]:
        result["valid"] = False
    return result


def audit_all_skills(skills_dir: Path, strict_depth: bool = False) -> List[Dict[str, Any]]:
    """Audit all skills in skills directory."""
    if not skills_dir.exists():
        return []
    return [
        audit_single_skill(child, strict_depth=strict_depth)
        for child in sorted(skills_dir.iterdir())
        if child.is_dir() and not child.name.startswith(".")
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="DarkNecroStack Quality, Depth & Anti-Boilerplate Linter")
    parser.add_argument("--skill", help="Audit a specific skill by folder name")
    parser.add_argument("--all", action="store_true", help="Audit all skills in the ecosystem")
    parser.add_argument("--benchmark", action="store_true", help="Display token efficiency benchmark metrics")
    parser.add_argument("--strict-depth", action="store_true", help="Enforce reference density >= 100 tokens")
    parser.add_argument("--skills-dir", type=Path, default=SKILLS_DIR, help="Path to skills directory")

    args = parser.parse_args()
    if not args.skill and not args.all:
        args.all = True

    if args.skill:
        target = args.skills_dir / args.skill
        if not target.exists():
            print(f"[ERROR] Skill folder '{args.skill}' does not exist in {args.skills_dir}", file=sys.stderr)
            sys.exit(1)
        reports = [audit_single_skill(target, strict_depth=args.strict_depth)]
    else:
        reports = audit_all_skills(args.skills_dir, strict_depth=args.strict_depth)

    total_skills = len(reports)
    passed_skills = sum(1 for r in reports if r["valid"])
    total_violations = sum(len(r["violations"]) for r in reports)

    print(f"\n=== DarkNecroStack Quality & Token Linter ({passed_skills}/{total_skills} Passed) ===")
    for r in reports:
        status = "[PASS]" if r["valid"] else "[FAIL]"
        bench = r["token_benchmark"]
        print(
            f"{status} {r['skill']:24} | SKILL.md: {bench.get('skill_md_tokens', 0):4} tok "
            f"| Refs: {bench.get('reference_files', 0):2} ({bench.get('reference_tokens', 0):5} tok) "
            f"| Saved: {bench.get('token_savings_pct', 0)}%"
        )
        for v in r["violations"]:
            print(f"       ! [{v.get('rule')}] {v.get('message')}")

    if args.benchmark and reports:
        total_md = sum(r["token_benchmark"].get("skill_md_tokens", 0) for r in reports)
        total_ref = sum(r["token_benchmark"].get("reference_tokens", 0) for r in reports)
        total_all = total_md + total_ref
        ratio = round((total_ref / total_all * 100), 1) if total_all else 0
        print("\n--- Progressive Disclosure Token Efficiency Summary ---")
        print(f"  * Total Skills Audited         : {total_skills}")
        print(f"  * Prompt Context Weight (SKILL): {total_md:,} tokens")
        print(f"  * Deep Knowledge Deferred      : {total_ref:,} tokens")
        print(f"  * Total Ecosystem Knowledge    : {total_all:,} tokens")
        print(f"  * Token Quota Savings Ratio    : {ratio}% context overhead eliminated per turn")

    if total_violations > 0:
        print(f"\n[FAIL] Found {total_violations} skill violation(s).", file=sys.stderr)
        sys.exit(1)
    print(f"\n[SUCCESS] All {total_skills} skills meet DarkNecroStack and Antigravity specifications!")


if __name__ == "__main__":
    main()
