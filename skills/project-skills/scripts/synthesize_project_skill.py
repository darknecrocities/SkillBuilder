#!/usr/bin/env python3
"""
synthesize_project_skill.py - Autonomous Project Skill Synthesis Protocol (SSP).
Introspects repository manifests, frameworks, and architecture to mint a custom project skill.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def detect_project_profile(root_path: Path) -> Dict[str, Any]:
    profile: Dict[str, Any] = {
        "name": root_path.name.lower().replace(" ", "-"),
        "ecosystem": "generic",
        "frameworks": [],
        "persistence": "none",
        "testing": "none",
        "directories": []
    }

    # Inspect package.json
    pkg_json = root_path / "package.json"
    if pkg_json.exists():
        profile["ecosystem"] = "node"
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "name" in data and data["name"]:
                    profile["name"] = data["name"].split("/")[-1]
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "next" in deps: profile["frameworks"].append("Next.js")
                if "react" in deps: profile["frameworks"].append("React")
                if "express" in deps: profile["frameworks"].append("Express")
                if "@supabase/supabase-js" in deps: profile["persistence"] = "Supabase"
                if "firebase" in deps or "firebase-admin" in deps: profile["persistence"] = "Firebase"
                if "@prisma/client" in deps: profile["persistence"] = "Prisma"
                if "drizzle-orm" in deps: profile["persistence"] = "Drizzle"
                if "vitest" in deps: profile["testing"] = "Vitest"
                elif "jest" in deps: profile["testing"] = "Jest"
        except Exception:
            pass

    # Inspect Python manifests
    if (root_path / "pyproject.toml").exists() or (root_path / "requirements.txt").exists():
        profile["ecosystem"] = "python"
        req_file = root_path / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text(encoding="utf-8", errors="ignore").lower()
            if "fastapi" in content: profile["frameworks"].append("FastAPI")
            if "django" in content: profile["frameworks"].append("Django")
            if "sqlalchemy" in content: profile["persistence"] = "SQLAlchemy"
            if "pytest" in content: profile["testing"] = "pytest"

    # Inspect Flutter pubspec.yaml
    if (root_path / "pubspec.yaml").exists():
        profile["ecosystem"] = "flutter"
        profile["frameworks"].append("Flutter")
        profile["testing"] = "flutter_test"

    # Detect top-level directories
    for child in root_path.iterdir():
        if child.is_dir() and not child.name.startswith((".", "node_modules", "dist", "build", "venv")):
            profile["directories"].append(child.name)

    profile["directories"].sort()
    return profile


def generate_skill_markdown(profile: Dict[str, Any]) -> str:
    name = profile["name"]
    frameworks = ", ".join(profile["frameworks"]) or "Standard Library"
    persistence = profile["persistence"] if profile["persistence"] != "none" else "File System / API"
    testing = profile["testing"] if profile["testing"] != "none" else "Unit Testing Suite"
    dirs = ", ".join(profile["directories"]) or "Flat Root Layout"

    return f"""---
name: {name}-domain
description: Tailored architectural invariants, conventions, and verification gates for {name}.
---

# {name.title()} Domain Engineering Standard

> **Ecosystem**: {profile['ecosystem'].title()}  
> **Frameworks**: {frameworks}  
> **Persistence**: {persistence}  
> **Testing Strategy**: {testing}

This project-specific skill was synthesized via the **Skill Synthesis Protocol (SSP)**.
It establishes mandatory architectural invariants, domain conventions, and verification gates for this repository.

---

## 1. Project Invariants & Non-Negotiables
- **Physical Line Limits**: Strictly enforce the 500-line ceiling per source file (target sweet spot: 150–250 lines).
- **Anti-Mock Mandate**: All services and features must be wired to real persistence ({persistence}); zero toy mock arrays.
- **Architectural Boundary**: Respect top-level directory isolation: `{dirs}`.
- **Defensive Error Handling**: Sanitize internal exceptions to RFC 7807 Problem Details; zero silent error swallowing.

---

## 2. Directory Layout & Key Modules
{chr(10).join(f"- `{d}/`: Core domain slice and modules." for d in profile["directories"][:8])}

---

## 3. Project Verification Checklist
Run prior to completing tasks or opening pull requests:
```bash
# Automated Test Suite
{f"npm test" if profile["ecosystem"] == "node" else "pytest" if profile["ecosystem"] == "python" else "flutter test" if profile["ecosystem"] == "flutter" else "make test"}

# 500-Line Source File Limit Audit
python3 skills/world-class-engineering/scripts/check_source_line_limits.py --path . --show-tiers
```
"""


def mint_project_skill(root_path: Path, profile: Dict[str, Any]) -> Path:
    target_dir = root_path / ".agents" / "skills" / f"{profile['name']}-domain"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "SKILL.md"
    content = generate_skill_markdown(profile)
    target_file.write_text(content, encoding="utf-8")
    return target_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthesize and mint tailored project skills.")
    parser.add_argument("--path", "-p", default=".", help="Root directory of target project")
    parser.add_argument("--mint", action="store_true", help="Mint SKILL.md into .agents/skills/")
    parser.add_argument("--json", action="store_true", help="Output profile in JSON format")
    args = parser.parse_args()

    root_path = Path(os.path.abspath(args.path))
    profile = detect_project_profile(root_path)

    if args.json:
        print(json.dumps(profile, indent=2))
        return 0

    if args.mint:
        minted_path = mint_project_skill(root_path, profile)
        print(f"[MINTED] Project Skill successfully synthesized: {minted_path}")
        return 0

    print(generate_skill_markdown(profile))
    return 0


if __name__ == "__main__":
    sys.exit(main())
