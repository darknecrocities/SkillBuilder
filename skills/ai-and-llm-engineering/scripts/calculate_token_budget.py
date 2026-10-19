#!/usr/bin/env python3
"""
CLI utility to estimate token count, analyze prompt payload density,
and verify context budget compliance.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import json
import os
import sys
from typing import Dict


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    # Average heuristic for code and English prose: ~3.8 characters per token
    return max(1, int(len(text) / 3.8))


def analyze_payload(text: str, budget_limit: int = 8000) -> Dict[str, object]:
    chars = len(text)
    words = len(text.split())
    lines = text.count("\n") + 1
    est_tokens = estimate_tokens(text)
    utilization_pct = round((est_tokens / budget_limit) * 100, 2)

    return {
        "character_count": chars,
        "word_count": words,
        "line_count": lines,
        "estimated_tokens": est_tokens,
        "budget_limit": budget_limit,
        "budget_utilization_pct": utilization_pct,
        "status": "PASS" if est_tokens <= budget_limit else "EXCEEDED",
    }


def main():
    parser = argparse.ArgumentParser(description="Estimate token usage and analyze prompt density.")
    parser.add_argument("--text", "-t", type=str, help="Text string to evaluate")
    parser.add_argument("--file", "-f", type=str, help="File to evaluate")
    parser.add_argument("--budget", "-b", type=int, default=8000, help="Token budget ceiling (default: 8000)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    content = ""
    if args.text:
        content = args.text
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    else:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)

    analysis = analyze_payload(content, args.budget)

    if args.json:
        print(json.dumps(analysis, indent=2))
        return

    print("\nToken Budget Analysis:")
    print("=" * 40)
    print(f"Character Count:       {analysis['character_count']}")
    print(f"Word Count:            {analysis['word_count']}")
    print(f"Line Count:            {analysis['line_count']}")
    print(f"Estimated Tokens:      {analysis['estimated_tokens']}")
    print(f"Budget Limit:          {analysis['budget_limit']}")
    print(f"Budget Utilization:    {analysis['budget_utilization_pct']}%")
    print(f"Status:                [{analysis['status']}]")
    print("=" * 40)

    if analysis["status"] != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
