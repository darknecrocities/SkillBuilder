#!/usr/bin/env python3
"""
session_start_health.py - Antigravity SessionStart health check.
Verifies repository environment readiness, backup manifest state, and SkillBuilder initialization.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Antigravity Automation Engine
"""

import json
import os
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    manifest_path = repo_root / ".backups" / "backup_manifest.json"

    # Ensure canonical backup manifest directory exists
    if not manifest_path.exists():
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps({"version": "1.0", "backups": {}}, indent=2) + "\n", encoding="utf-8")

    skills_dir = repo_root / "skills"
    skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()]) if skills_dir.exists() else 0

    print(f"[SkillBuilder v3.2.0] Session initialized. {skill_count} modular skills active with Antigravity Automation & Lifecycle Hooks.")
    sys.exit(0)


if __name__ == "__main__":
    main()
