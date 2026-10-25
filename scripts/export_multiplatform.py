#!/usr/bin/env python3
"""
export_multiplatform.py - Universal exporter converting SkillBuilder skills and rules
into native configuration formats for Cursor (.cursor/rules/*.mdc, .cursorrules),
Claude Code (CLAUDE.md), Codex/OpenAI (CODEX.md), Windsurf (.windsurfrules), and Cline (.clinerules).
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def parse_skill_metadata(skill_path: Path) -> Tuple[str, str, str]:
    """Parse name, description, and body content from SKILL.md."""
    content = skill_path.read_text(encoding="utf-8", errors="ignore")
    name = skill_path.parent.name
    description = ""
    body = content

    frontmatter_match = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if frontmatter_match:
        yaml_block = frontmatter_match.group(1)
        body = frontmatter_match.group(2).strip()

        name_match = re.search(r"^name:\s*([^\n]+)", yaml_block, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip()

        desc_match = re.search(r"^description:\s*([^\n]+)", yaml_block, re.MULTILINE)
        if desc_match:
            description = desc_match.group(1).strip()

    return name, description, body


def get_all_skills(repo_dir: Path) -> List[Tuple[str, str, str]]:
    """Collect all valid skills from skills/ directory."""
    skills_dir = repo_dir / "skills"
    skills = []
    if not skills_dir.exists():
        return skills

    for skill_folder in sorted(skills_dir.iterdir()):
        if skill_folder.is_dir():
            skill_md = skill_folder / "SKILL.md"
            if skill_md.exists():
                name, desc, body = parse_skill_metadata(skill_md)
                skills.append((name, desc, body))
    return skills


def export_cursor_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to .cursor/rules/*.mdc and root .cursorrules."""
    created_files = []
    cursor_rules_dir = target_dir / ".cursor" / "rules"
    cursor_rules_dir.mkdir(parents=True, exist_ok=True)

    skills = get_all_skills(repo_dir)
    for name, desc, body in skills:
        mdc_path = cursor_rules_dir / f"{name}.mdc"
        mdc_content = f"""---
description: {desc}
globs: *
alwaysApply: false
---

{body}
"""
        mdc_path.write_text(mdc_content, encoding="utf-8")
        created_files.append(str(mdc_path))

    # Also generate a consolidated .cursorrules
    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""

    cursorrules_path = target_dir / ".cursorrules"
    cursorrules_content = f"""# SkillBuilder Core Guidelines for Cursor AI

{core_rules}

## 20 Modular Skills Available
Detailed rules are loaded from `.cursor/rules/*.mdc`.
"""
    cursorrules_path.write_text(cursorrules_content, encoding="utf-8")
    created_files.append(str(cursorrules_path))

    return created_files


def export_claude_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to CLAUDE.md for Claude Code CLI and Anthropic models."""
    target_dir.mkdir(parents=True, exist_ok=True)
    claude_path = target_dir / "CLAUDE.md"

    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    skills = get_all_skills(repo_dir)

    skills_summary_lines = []
    for name, desc, _ in skills:
        skills_summary_lines.append(f"- **`/{name}`**: {desc}")
    skills_summary = "\n".join(skills_summary_lines)

    content = f"""# CLAUDE.md - SkillBuilder Engineering Guidelines for Claude Code

> Universal Engineering Discipline for Anthropic Claude Code & Claude Desktop.

{core_rules}

## Available SkillBuilder Disciplines (20 Skills)

{skills_summary}

## Code Generation & Review Instructions
- Enforce the 500-line physical limit on all generated source files.
- Zero fake mock databases: use SQLite, PostgreSQL, or structured file stores.
- Prohibit neon purple gradients, glowing borders, card-soup layouts, and raw emojis in UI buttons.
- Keep commits under 1,000 changed lines.
"""
    claude_path.write_text(content, encoding="utf-8")
    return [str(claude_path)]


def export_codex_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to CODEX.md for OpenAI models, Custom Instructions, and Codex."""
    target_dir.mkdir(parents=True, exist_ok=True)
    codex_path = target_dir / "CODEX.md"

    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    skills = get_all_skills(repo_dir)

    skills_summary = "\n".join(f"- `/{name}`: {desc}" for name, desc, _ in skills)

    content = f"""# CODEX.md - OpenAI & ChatGPT System Instructions

> Production Engineering Standards for OpenAI Codex, GPT-4o, and ChatGPT.

{core_rules}

## Skill Index (20 Skills)
{skills_summary}

## Developer Directives
1. Strict 500-line maximum on all source files.
2. Never interpolate variables into SQL queries (prevent SQL injection).
3. Zero decorative badges, shields.io icons, or synthetic AI marketing copy.
4. Autonomous research: when a library is broken, evaluate and recommend drop-in replacements.
"""
    codex_path.write_text(content, encoding="utf-8")
    return [str(codex_path)]


def export_windsurf_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to .windsurfrules for Windsurf / Cascade."""
    target_dir.mkdir(parents=True, exist_ok=True)
    windsurf_path = target_dir / ".windsurfrules"

    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    content = f"# Windsurf & Cascade AI Rules\n\n{core_rules}\n"
    windsurf_path.write_text(content, encoding="utf-8")
    return [str(windsurf_path)]


def export_cline_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to .clinerules for Cline & Roo-Code."""
    target_dir.mkdir(parents=True, exist_ok=True)
    cline_path = target_dir / ".clinerules"

    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    content = f"# Cline & Roo-Code System Rules\n\n{core_rules}\n"
    cline_path.write_text(content, encoding="utf-8")
    return [str(cline_path)]


def export_all(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export all platform configurations (Cursor, Claude, Codex, Windsurf, Cline)."""
    created: List[str] = []
    created.extend(export_cursor_rules(repo_dir, target_dir))
    created.extend(export_claude_rules(repo_dir, target_dir))
    created.extend(export_codex_rules(repo_dir, target_dir))
    created.extend(export_windsurf_rules(repo_dir, target_dir))
    created.extend(export_cline_rules(repo_dir, target_dir))
    return created


def main() -> int:
    parser = argparse.ArgumentParser(description="Export SkillBuilder rules to Cursor, Claude, Codex, Windsurf, or Cline.")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent), help="Root path of SkillBuilder repository")
    parser.add_argument("--target", "-t", required=True, help="Target project directory to install rules into")
    parser.add_argument("--platform", "-p", choices=["cursor", "claude", "codex", "windsurf", "cline", "all"], default="all", help="Target platform to export for")
    args = parser.parse_args()

    repo_dir = Path(args.repo).resolve()
    target_dir = Path(args.target).resolve()

    if not repo_dir.exists():
        print(f"Error: SkillBuilder repo directory '{repo_dir}' not found.", file=sys.stderr)
        return 1

    created_files: List[str] = []

    if args.platform in {"cursor", "all"}:
        created_files.extend(export_cursor_rules(repo_dir, target_dir))
    if args.platform in {"claude", "all"}:
        created_files.extend(export_claude_rules(repo_dir, target_dir))
    if args.platform in {"codex", "all"}:
        created_files.extend(export_codex_rules(repo_dir, target_dir))
    if args.platform in {"windsurf", "all"}:
        created_files.extend(export_windsurf_rules(repo_dir, target_dir))
    if args.platform in {"cline", "all"}:
        created_files.extend(export_cline_rules(repo_dir, target_dir))

    print(f"=== Multi-Platform Export Successful ({len(created_files)} files created) ===")
    print(f"Target Directory: {target_dir}")
    for f in created_files:
        rel = os.path.relpath(f, target_dir)
        print(f"  + {rel}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
