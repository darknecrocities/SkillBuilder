#!/usr/bin/env python3
"""
export_multiplatform.py - Universal exporter converting DarkNecroStack skills and rules
into native configuration formats for Cursor (.cursor/rules/*.mdc, .cursorrules),
Claude Code (CLAUDE.md), Codex/OpenAI (CODEX.md), Windsurf (.windsurfrules), and Cline (.clinerules).
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

CURSOR_GLOB_MAP: Dict[str, str] = {
    "2d-mascot-motion": "*.riv,*.svg,*.tsx,*.dart,*.swift,*.kt",
    "brand-assets": "*.svg,*.json,*.tsx,*.html",
    "web-ui": "*.css,*.tsx,*.jsx,*.html",
    "mobile-ui": "*.swift,*.kt,*.dart,*.native.tsx",
    "mcp-engineering": "*mcp*,*.ts,*.py",
    "browser-media-wasm": "*.worker.*,*.ts,*.tsx",
    "local-first-data": "*.ts,*.tsx,*.py,*.sql",
    "computer-vision": "*.py,*.onnx,*.pt,*.ts",
    "vlm-multimodal": "*.py,*.ts,*.tsx",
    "local-llm": "Modelfile,*.gguf,*.py,*.ts,*.sh",
    "ai-integration": "*.py,*.ts,*.tsx,.env*",
    "testing": "*.test.*,*.spec.*,test_*.py",
    "darknecrostack": "*",
}


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
    if not skills_dir.exists():
        return []
    skills = []
    for skill_folder in sorted(skills_dir.iterdir()):
        if skill_folder.is_dir() and (skill_folder / "SKILL.md").exists():
            skills.append(parse_skill_metadata(skill_folder / "SKILL.md"))
    return skills


def export_cursor_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to .cursor/rules/*.mdc and root .cursorrules."""
    created_files = []
    cursor_rules_dir = target_dir / ".cursor" / "rules"
    cursor_rules_dir.mkdir(parents=True, exist_ok=True)

    skills = get_all_skills(repo_dir)
    for name, desc, body in skills:
        globs = CURSOR_GLOB_MAP.get(name, "*")
        mdc_path = cursor_rules_dir / f"{name}.mdc"
        mdc_content = f"---\ndescription: {desc}\nglobs: {globs}\nalwaysApply: false\n---\n\n{body}\n"
        mdc_path.write_text(mdc_content, encoding="utf-8")
        created_files.append(str(mdc_path))

    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""

    cursorrules_path = target_dir / ".cursorrules"
    cursorrules_content = (
        f"# DarkNecroStack Core Guidelines for Cursor AI\n\n"
        f"{core_rules}\n\n"
        f"## {len(skills)} Modular Skills Available\n"
        f"Detailed playbooks and rules are loaded from `.cursor/rules/*.mdc`.\n"
        f"Subagent bootstrap: `skills/darknecrostack/worker.md`.\n"
    )
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
    skills_summary = "\n".join(f"- **`/{name}`**: {desc}" for name, desc, _ in skills)

    content = f"""# CLAUDE.md - DarkNecroStack Engineering Guidelines for Claude Code

> Universal Engineering Discipline for Anthropic Claude Code & Claude Desktop.

{core_rules}

## Available DarkNecroStack Disciplines ({len(skills)} Skills)

{skills_summary}

## Code Generation, Multi-Agent Sync & Storage Safety Instructions
- Enforce the multi-tiered 500-line physical limit (target sweet spot: 150–250 lines; warning: 350 lines).
- Start every spawned subagent kickoff with: `Read <abs-path>/skills/darknecrostack/worker.md before anything else.`
- Zero fake mock databases: use SQLite, PostgreSQL, or structured file stores.
- Idempotent Single-Slot Backups (Zero Spam): Maintain one canonical backup per resource state keyed by SHA-256 digest in `.backups/backup_manifest.json`. Never create duplicate `.bak.1`, `.bak.2` copies when state is unchanged.
- Sensitive Deletion Human-in-the-Loop Gate: Halt and warn the user first before executing any `DROP`, `TRUNCATE`, unconditioned `DELETE`, bucket/collection purge, or sensitive file removal.
- Prohibit neon purple gradients, glowing borders, card-soup layouts, Corporate Memphis illustrations, and raw emojis in UI buttons.
- Keep commits under 1,000 changed lines with Documentation Impact disclosed.
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

> Production Engineering Standards for OpenAI Codex and ChatGPT (DarkNecroStack).

{core_rules}

## Skill Index ({len(skills)} Skills)
{skills_summary}

## Developer Directives
1. Multi-tiered maintainability: strict 500-line ceiling, 350-line warning threshold, and 150–250 line sweet spot.
2. Never interpolate variables into SQL queries (prevent SQL injection).
3. Zero decorative badges, shields.io icons, or synthetic AI marketing copy.
4. Autonomous research: when a library is broken, evaluate and recommend drop-in replacements.
5. Idempotent Single-Slot Backups: maintain a single SHA-256 content-hashed backup per resource state; never spam duplicate backup files across concurrent agent runs.
6. Sensitive Deletion Gate: always notify the user with impact scope and backup hash before deleting tables, columns, buckets, collections, or sensitive files.
"""
    codex_path.write_text(content, encoding="utf-8")
    return [str(codex_path)]


def export_windsurf_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to .windsurfrules for Windsurf / Cascade."""
    target_dir.mkdir(parents=True, exist_ok=True)
    windsurf_path = target_dir / ".windsurfrules"
    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    windsurf_path.write_text(f"# Windsurf & Cascade AI Rules (DarkNecroStack)\n\n{core_rules}\n", encoding="utf-8")
    return [str(windsurf_path)]


def export_cline_rules(repo_dir: Path, target_dir: Path) -> List[str]:
    """Export skills to .clinerules for Cline & Roo-Code."""
    target_dir.mkdir(parents=True, exist_ok=True)
    cline_path = target_dir / ".clinerules"
    agents_md = repo_dir / "AGENTS.md"
    core_rules = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    cline_path.write_text(f"# Cline & Roo-Code System Rules (DarkNecroStack)\n\n{core_rules}\n", encoding="utf-8")
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
    parser = argparse.ArgumentParser(description="Export DarkNecroStack rules to Cursor, Claude, Codex, Windsurf, or Cline.")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent), help="Root path of DarkNecroStack repository")
    parser.add_argument("--target", "-t", required=True, help="Target project directory to install rules into")
    parser.add_argument("--platform", "-p", choices=["cursor", "claude", "codex", "windsurf", "cline", "all"], default="all")
    args = parser.parse_args()

    repo_dir = Path(args.repo).resolve()
    target_dir = Path(args.target).resolve()
    if not repo_dir.exists():
        print(f"Error: DarkNecroStack repo directory '{repo_dir}' not found.", file=sys.stderr)
        return 1

    exporters = {
        "cursor": export_cursor_rules,
        "claude": export_claude_rules,
        "codex": export_codex_rules,
        "windsurf": export_windsurf_rules,
        "cline": export_cline_rules,
        "all": export_all,
    }
    created_files = exporters[args.platform](repo_dir, target_dir)
    print(f"=== Multi-Platform Export Successful ({len(created_files)} files created) ===")
    print(f"Target Directory: {target_dir}")
    for f in created_files:
        print(f"  + {os.path.relpath(f, target_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
