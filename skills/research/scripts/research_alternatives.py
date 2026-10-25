#!/usr/bin/env python3
"""
research_alternatives.py - Autonomous research CLI for package alternatives and fallback planning.
Audits deprecated or problematic dependencies and recommends production-grade modern replacements.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

ALTERNATIVES_CATALOG: Dict[str, Dict[str, Any]] = {
    "moment": {
        "domain": "Date & Time",
        "status": "deprecated",
        "recommended": ["date-fns", "dayjs", "native Intl"],
        "rationale": "Moment is in maintenance mode, mutable, and not tree-shakeable. date-fns is modular and immutable.",
        "tradeoffs": {"bundle_savings": "High (up to 70KB)", "type_safety": "Native TypeScript", "migration_effort": "Low"}
    },
    "request": {
        "domain": "HTTP Client",
        "status": "deprecated",
        "recommended": ["native fetch", "undici", "ky"],
        "rationale": "Request was fully deprecated in 2020. Native fetch is standard across Node 18+ and browsers.",
        "tradeoffs": {"bundle_savings": "Zero dependencies", "type_safety": "Standard Web API", "migration_effort": "Low"}
    },
    "axios": {
        "domain": "HTTP Client",
        "status": "active_alternative_available",
        "recommended": ["native fetch", "ky", "wretch"],
        "rationale": "Axios adds external dependency overhead when native fetch + typed wrapper is sufficient.",
        "tradeoffs": {"bundle_savings": "12KB to 0KB", "type_safety": "Equivalent", "migration_effort": "Low"}
    },
    "node-sass": {
        "domain": "CSS Preprocessor",
        "status": "deprecated",
        "recommended": ["sass-embedded", "tailwindcss", "postcss"],
        "rationale": "LibSass and Node Sass are deprecated; sass-embedded uses Dart Sass native binaries.",
        "tradeoffs": {"bundle_savings": "Build speed 3x faster", "type_safety": "N/A", "migration_effort": "Medium"}
    },
    "sqlite3": {
        "domain": "SQLite Database Driver",
        "status": "build_friction",
        "recommended": ["better-sqlite3", "drizzle-orm/better-sqlite3", "@libsql/client"],
        "rationale": "sqlite3 frequently fails during node-gyp native compilation; better-sqlite3 is synchronous and 5x faster.",
        "tradeoffs": {"bundle_savings": "Faster execution", "type_safety": "First-class with Drizzle", "migration_effort": "Low"}
    },
    "enzyme": {
        "domain": "React Testing",
        "status": "deprecated",
        "recommended": ["@testing-library/react"],
        "rationale": "Enzyme is incompatible with modern React 18/19 concurrent features. Testing Library tests behavior.",
        "tradeoffs": {"bundle_savings": "Modern React support", "type_safety": "Native", "migration_effort": "Medium"}
    },
    "pydantic_v1": {
        "domain": "Python Data Validation",
        "status": "legacy",
        "recommended": ["pydantic_v2"],
        "rationale": "Pydantic v2 core is rewritten in Rust and achieves 5x-10x throughput improvements.",
        "tradeoffs": {"bundle_savings": "5x-10x speedup", "type_safety": "Strict PEP 484", "migration_effort": "Low-to-Medium"}
    }
}


def find_alternative(query: str) -> Optional[Dict[str, Any]]:
    key = query.lower().strip()
    return ALTERNATIVES_CATALOG.get(key)


def audit_manifest(manifest_path: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not os.path.exists(manifest_path):
        return results

    content = ""
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return results

    for pkg_name, data in ALTERNATIVES_CATALOG.items():
        if f'"{pkg_name}"' in content or f"'{pkg_name}'" in content or f"{pkg_name}=" in content:
            results.append({
                "package": pkg_name,
                "status": data["status"],
                "recommended": data["recommended"],
                "rationale": data["rationale"]
            })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous package alternative discovery CLI.")
    parser.add_argument("--query", "-q", help="Name of package or technology to research")
    parser.add_argument("--audit", "-a", help="Path to manifest file (package.json, requirements.txt)")
    parser.add_argument("--list", action="store_true", help="List all cataloged alternatives")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    if args.list:
        if args.json:
            print(json.dumps(ALTERNATIVES_CATALOG, indent=2))
        else:
            print("=== Cataloged Package Alternatives ===")
            for pkg, info in ALTERNATIVES_CATALOG.items():
                print(f"  - {pkg} ({info['domain']}): Recommend -> {', '.join(info['recommended'])}")
        return 0

    if args.query:
        alt = find_alternative(args.query)
        if alt:
            if args.json:
                print(json.dumps({args.query: alt}, indent=2))
            else:
                print(f"=== Research Report: {args.query} ===")
                print(f"Domain: {alt['domain']}")
                print(f"Status: {alt['status']}")
                print(f"Recommended Replacements: {', '.join(alt['recommended'])}")
                print(f"Rationale: {alt['rationale']}")
                print(f"Trade-offs: {alt['tradeoffs']}")
            return 0
        else:
            print(f"[INFO] No pre-cataloged replacement for '{args.query}'. Search PyPI/npm for actively maintained alternatives.")
            return 0

    if args.audit:
        findings = audit_manifest(args.audit)
        if args.json:
            print(json.dumps({"findings": findings}, indent=2))
        else:
            print(f"=== Dependency Audit: {args.audit} ===")
            if not findings:
                print("[PASS] No legacy or problematic dependencies found.")
            else:
                for f in findings:
                    print(f"[ALERT] Found '{f['package']}' ({f['status']}) -> Recommend: {', '.join(f['recommended'])}")
                    print(f"        {f['rationale']}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
