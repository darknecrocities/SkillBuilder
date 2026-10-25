#!/usr/bin/env python3
"""
record_learning.py - CLI utility to record, persist, and query learned conventions,
user preferences, and architectural invariants across pairing sessions.
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
    pattern = re.compile(r"^\s*-\s+\*\*\[([A-Z]+-\d+)\]\s*\(([^\)]+)\)\*\*:\s*(.+)$", re.MULTILINE)
    for match in pattern.finditer(content):
        conventions.append({
            "id": match.group(1),
            "date": match.group(2),
            "text": match.group(3).strip()
        })
    return conventions


def save_convention(category: str, text: str, filepath: str) -> str:
    category = category.upper()
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

    existing = load_conventions(filepath)
    for conv in existing:
        if conv["text"].lower() == text.strip().lower():
            return f"Duplicate: already recorded as [{conv['id']}]."

    cat_count = sum(1 for c in existing if c["id"].startswith(category))
    new_id = f"{category}-{cat_count + 1:03d}"
    today = datetime.now().strftime("%Y-%m-%d")
    entry_line = f"- **[{new_id}] ({today})**: {text.strip()}\n"

    if not os.path.exists(filepath):
        header = "# Project Learned Conventions & Architectural Invariants\n\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + entry_line)
    else:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(entry_line)

    return f"Recorded convention [{new_id}] successfully."


def main() -> int:
    parser = argparse.ArgumentParser(description="Record and query learned conventions.")
    parser.add_argument("--category", "-c", default="ARCH", help="Category (UI, ARCH, API, DATA, SEC, QA)")
    parser.add_argument("--text", "-t", help="Concrete convention or invariant text to record")
    parser.add_argument("--list", "-l", action="store_true", help="List all recorded conventions")
    parser.add_argument("--file", "-f", help="Custom path to learned_conventions.md")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    filepath = get_conventions_file_path(args.file)

    if args.list:
        conventions = load_conventions(filepath)
        if args.json:
            print(json.dumps(conventions, indent=2))
        else:
            print(f"=== Learned Conventions ({len(conventions)}) from {filepath} ===")
            for c in conventions:
                print(f"  [{c['id']}] ({c['date']}): {c['text']}")
        return 0

    if args.text:
        msg = save_convention(args.category, args.text, filepath)
        print(msg)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
