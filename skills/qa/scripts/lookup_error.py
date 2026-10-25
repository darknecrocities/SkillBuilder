#!/usr/bin/env python3
"""
CLI utility to search the Master Software Engineering Error Catalog for rapid diagnosis
and battle-tested remediations.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional


def load_error_catalog(catalog_path: Optional[str] = None) -> List[Dict[str, str]]:
    if not catalog_path:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        catalog_path = os.path.join(base_dir, "../references/master-error-catalog.md")

    if not os.path.exists(catalog_path):
        return []

    with open(catalog_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    # Split by error header: ### [ERR-...
    raw_sections = re.split(r"\n###\s+\[(ERR-[A-Z]+-\d+)\]", content)

    # First chunk is preamble
    for i in range(1, len(raw_sections), 2):
        err_id = raw_sections[i].strip()
        body = raw_sections[i + 1] if (i + 1) < len(raw_sections) else ""
        
        # Parse fields
        title_match = re.search(r"^\s*([^\n]+)", body)
        title = title_match.group(1).strip() if title_match else err_id

        cat_match = re.search(r"-\s+\*\*Category\*\*:\s*([^\n]+)", body)
        category = cat_match.group(1).strip() if cat_match else "General"

        sym_match = re.search(r"-\s+\*\*Symptom\*\*:\s*([^\n]+)", body)
        symptom = sym_match.group(1).strip() if sym_match else ""

        root_match = re.search(r"-\s+\*\*Root Cause\*\*:\s*([^\n]+)", body)
        root_cause = root_match.group(1).strip() if root_match else ""

        res_match = re.search(r"-\s+\*\*Resolution\*\*:\s*([\s\S]*?)(?=-\s+\*\*Regression Prevention\*\*|$)", body)
        resolution = res_match.group(1).strip() if res_match else ""

        entries.append({
            "id": f"[{err_id}]",
            "title": title,
            "category": category,
            "symptom": symptom,
            "root_cause": root_cause,
            "resolution": resolution,
            "full_text": f"### [{err_id}] {body.strip()}"
        })

    return entries


def search_errors(entries: List[Dict[str, str]], query: str, category: Optional[str] = None) -> List[Dict[str, str]]:
    results = []
    query_lower = query.lower()
    cat_lower = category.lower() if category else None

    for entry in entries:
        if cat_lower and cat_lower not in entry["category"].lower():
            continue

        searchable = f"{entry['id']} {entry['title']} {entry['category']} {entry['symptom']} {entry['root_cause']} {entry['resolution']}".lower()
        if query_lower in searchable or any(term in searchable for term in query_lower.split()):
            results.append(entry)

    return results


def main():
    parser = argparse.ArgumentParser(description="Search master error catalog for diagnoses and fixes.")
    parser.add_argument("--query", "-q", type=str, required=True, help="Search terms (e.g. 'deadlock', 'hydration')")
    parser.add_argument("--category", "-c", type=str, help="Filter by category (Frontend, Backend, Database, Cloud, AI)")
    parser.add_argument("--catalog", type=str, help="Custom path to master-error-catalog.md")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    entries = load_error_catalog(args.catalog)
    matches = search_errors(entries, args.query, args.category)

    if args.json:
        print(json.dumps(matches, indent=2))
        return

    if not matches:
        print(f"No error catalog entries matched query: '{args.query}'")
        sys.exit(0)

    print(f"\nFound {len(matches)} matching error record(s):\n" + "=" * 60)
    for m in matches:
        print(f"\nID: {m['id']} {m['title']}")
        print(f"Category: {m['category']}")
        print(f"Symptom: {m['symptom']}")
        print(f"Root Cause: {m['root_cause']}")
        print(f"Resolution:\n{m['resolution']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
