#!/usr/bin/env python3
"""
sanitize_ai_slop.py - CLI tool to detect and report AI slop anti-patterns.
Checks for decorative badges, fake mock databases, neon gradients, obvious comments,
synthetic marketing buzzwords, stripped focus rings, low-contrast grey copy, and emoji controls.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

SLOP_PATTERNS: List[Tuple[str, str, str]] = [
    ("ShieldsBadge", r"img\.shields\.io|badge\.svg", "Decorative shields.io badge found"),
    ("FakeMockArray", r"(const|let|var)\s+(mock\w+|fake\w+|dummy\w+)\s*=\s*\[", "Fake mock array simulating persistent state"),
    ("ObviousComment", r"(//|#)\s*(set\s+loading\s+to|increment\s+\w+\s+by|handle\s+click|return\s+the\s+result)", "Obvious redundant comment"),
    ("NeonVibeGradient", r"(from-purple-\d00\s+(?:via-\w+-\d00\s+)?to-(?:indigo|pink)-\d00|shadow-\[0_0_)", "Neon vibe-coding gradient or glow border"),
    ("MarketingBuzzword", r"(revolutionary\s+ai[- ]powered|seamless\s+and\s+intuitive|next-gen(?:eration)?\s+paradigm|unlock\s+the\s+power\s+of)", "Synthetic AI marketing buzzword"),
    ("AILogoTrope", r"(swirling[- ]gradient[- ](?:ribbon|sphere)|floating[- ]isometric[- ](?:cube|hexagon)|corporate[- ]memphis)", "Generic AI logo or illustration trope marker detected"),
    ("FuzzyNeonHalo", r"box-shadow:\s*0\s+0\s+(?:4\d|5\d|[6-9]\d|\d{3,})px", "Excessive fuzzy neon halo shadow without physical falloff"),
    ("StrippedFocusOutline", r"outline:\s*none\s*;|focus:outline-none(?!.*focus-visible:)", "Stripped focus outline without accessible focus-visible replacement"),
    ("EmojiControlSlop", r"<(?:button|a|h1|h2|h3)\b[^>]*>[^<\n]*[\U0001F300-\U0001FAFF]", "Raw Unicode emoji inside interactive control or heading; use Lucide SVG"),
    ("LowContrastDarkText", r"text-zinc-500\b[^\"'\n]*bg-zinc-950|bg-zinc-950\b[^\"'\n]*text-zinc-500", "Low-contrast zinc-500 text on zinc-950 canvas (fails WCAG AA 4.5:1)"),
]

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", ".gemini", "__pycache__", "venv", ".venv"}
CHECKED_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".py", ".md", ".html", ".css", ".dart", ".swift", ".kt"}


def scan_file(file_path: str) -> List[Dict[str, Any]]:
    """Scan a single source or markdown file for AI slop markers."""
    violations: List[Dict[str, Any]] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except OSError as err:
        return [{"file": file_path, "line": 0, "rule": "ReadError", "message": str(err)}]

    for line_idx, line in enumerate(lines, start=1):
        for rule_id, pattern, desc in SLOP_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append({
                    "file": file_path,
                    "line": line_idx,
                    "rule": rule_id,
                    "message": desc,
                    "snippet": line.strip()[:100],
                })
    return violations


def scan_directory(target_path: str) -> List[Dict[str, Any]]:
    """Walk target_path recursively and collect all AI slop violations."""
    all_violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in sorted(files):
            if os.path.splitext(f)[1].lower() in CHECKED_EXTENSIONS:
                all_violations.extend(scan_file(os.path.join(root, f)))
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan codebase for AI slop anti-patterns.")
    parser.add_argument("--path", "-p", default=".", help="Root path to scan (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero status code if slop is found")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    violations = scan_file(target) if os.path.isfile(target) else scan_directory(target)

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

    return 1 if (args.strict and violations) else 0


if __name__ == "__main__":
    sys.exit(main())
