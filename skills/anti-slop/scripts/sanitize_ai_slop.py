#!/usr/bin/env python3
"""
sanitize_ai_slop.py - CLI tool to detect and report AI slop anti-patterns.
Checks for decorative badges, fake mock databases, neon gradients, obvious comments,
and synthetic marketing buzzwords.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Tuple

SLOP_PATTERNS: List[Tuple[str, str, str]] = [
    ("ShieldsBadge", r"img\.shields\.io|badge\.svg", "Decorative shields.io badge found"),
    ("FakeMockArray", r"(const|let|var)\s+(mock\w+|fake\w+|dummy\w+)\s*=\s*\[", "Fake mock array simulating persistent state"),
    ("ObviousComment", r"(//|#)\s*(set\s+loading\s+to|increment\s+\w+\s+by|handle\s+click|return\s+the\s+result)", "Obvious redundant comment"),
    ("NeonVibeGradient", r"(from-purple-\d00\s+to-indigo-\d00|shadow-\[0_0_)", "Neon vibe-coding gradient or glow border"),
    ("MarketingBuzzword", r"(revolutionary\s+ai[- ]powered|seamless\s+and\s+intuitive|next-gen(?:eration)?\s+paradigm)", "Synthetic AI marketing buzzword"),
]

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", ".gemini", "__pycache__", "venv", ".venv"}
CHECKED_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".py", ".md", ".html", ".css", ".dart"}


def scan_file(file_path: str) -> List[Dict[str, any]]:
    violations: List[Dict[str, any]] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as err:
        return [{"file": file_path, "line": 0, "rule": "ReadError", "message": str(err)}]

    for line_idx, line in enumerate(lines, start=1):
        for rule_id, pattern, desc in SLOP_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append({
                    "file": file_path,
                    "line": line_idx,
                    "rule": rule_id,
                    "message": desc,
                    "snippet": line.strip()[:100]
                })
    return violations


def scan_directory(target_path: str) -> List[Dict[str, any]]:
    all_violations: List[Dict[str, any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS:
                fp = os.path.join(root, f)
                all_violations.extend(scan_file(fp))
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan codebase for AI slop anti-patterns.")
    parser.add_argument("--path", "-p", default=".", help="Root path to scan (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero status code if slop is found")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        violations = scan_file(target)
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== Anti-AI-Slop Inspection: {target} ===")
        if not violations:
            print("[PASS] No AI slop markers detected. Codebase is clean and high-density.")
        else:
            print(f"[FAIL] Found {len(violations)} AI slop violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                print(f"    Snippet: {v.get('snippet', '')}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
