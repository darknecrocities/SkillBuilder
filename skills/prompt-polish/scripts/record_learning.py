#!/usr/bin/env python3
"""
CLI utility to dynamically record, persist, and query learned conventions,
user preferences, and architectural invariants across pairing sessions.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
from datetime import datetime
import json
import os
import re
import sys
from typing import Dict, List, Optional


DEFAULT_CONVENTIONS_FILE = ".agents/learned_conventions.md"


def get_conventions_file_path(custom_path: Optional[str] = None) -> str:
    if custom_path:
        return custom_path

    # Walk upwards looking for .agents or .git
    curr = os.getcwd()
    while curr != os.path.dirname(curr):
        agents_dir = os.path.join(curr, ".agents")
        if os.path.isdir(agents_dir):
            return os.path.join(agents_dir, "learned_conventions.md")
        if os.path.isdir(os.path.join(curr, ".git")):
            os.makedirs(agents_dir, exist_ok=True)
            return os.path.join(agents_dir, "learned_conventions.md")
        curr = os.path.dirname(curr)

    return os.path.join(os.getcwd(), DEFAULT_CONVENTIONS_FILE)


def load_conventions(filepath: str) -> List[Dict[str, str]]:
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    conventions = []
    # Match lines like: - **[CATEGORY-001] (YYYY-MM-DD)**: text
    pattern = re.compile(r"^\s*-\s+\*\*\[([A-Z]+-\d+)\]\s*\(([^\)]+)\)\*\*:\s*(.+)$", re.MULTILINE)
    for match in pattern.finditer(content):
        conventions.append({
            "id": match.group(1),
            "date": match.group(2),
            "rule": match.group(3).strip(),
            "category": match.group(1).split("-")[0],
        })
    return conventions


def record_convention(rule: str, category: str = "GENERAL", filepath: Optional[str] = None) -> Dict[str, str]:
    target_path = get_conventions_file_path(filepath)
    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)

    existing = load_conventions(target_path)
    clean_cat = category.upper()
    next_index = sum(1 for c in existing if c["category"] == clean_cat) + 1
    rule_id = f"{clean_cat}-{next_index:03d}"
    today = datetime.now().strftime("%Y-%m-%d")

    entry_line = f"- **[{rule_id}] ({today})**: {rule.strip()}\n"

    if not os.path.exists(target_path):
        header = "# Project Learned Conventions & User Preferences\n\n"
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(header + entry_line)
    else:
        with open(target_path, "a", encoding="utf-8") as f:
            f.write(entry_line)

    return {
        "id": rule_id,
        "date": today,
        "category": clean_cat,
        "rule": rule.strip(),
        "file": target_path,
    }


def main():
    parser = argparse.ArgumentParser(description="Record and query learned conventions across pairing sessions.")
    parser.add_argument("--record", "-r", type=str, help="Convention or user preference rule to record")
    parser.add_argument("--category", "-c", type=str, default="GENERAL", help="Rule category (STYLE, ARCHITECTURE, UI, DATABASE, TESTING, GENERAL)")
    parser.add_argument("--list", "-l", action="store_true", help="List all currently recorded conventions")
    parser.add_argument("--path", "-p", type=str, help="Path to learned_conventions.md file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    target_path = get_conventions_file_path(args.path)

    if args.record:
        entry = record_convention(args.record, args.category, target_path)
        if args.json:
            print(json.dumps(entry, indent=2))
        else:
            print(f"[SUCCESS] Recorded learned convention [{entry['id']}]: {entry['rule']}")
            print(f"Saved to: {entry['file']}")
        return

    if args.list:
        conventions = load_conventions(target_path)
        if args.json:
            print(json.dumps(conventions, indent=2))
        else:
            if not conventions:
                print(f"No learned conventions recorded in: {target_path}")
                return
            print(f"\nLearned Conventions ({target_path}):\n" + "=" * 60)
            for c in conventions:
                print(f"[{c['id']}] ({c['date']}): {c['rule']}")
            print("=" * 60)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
