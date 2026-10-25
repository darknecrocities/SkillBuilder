#!/usr/bin/env python3
"""
CLI utility to clean, structure, and polish raw user prompts into token-efficient
engineering specifications.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Optional


CONVERSATIONAL_FILLERS = [
    r"^hey\b",
    r"^hello\b",
    r"^hi\b",
    r"^please\b",
    r"^kindly\b",
    r"^can you\b",
    r"^could you\b",
    r"^i want you to\b",
    r"^i need you to\b",
    r"^i would like you to\b",
    r"^i was wondering if you could\b",
    r"^make me a\b",
    r"^build me a\b",
    r"^create me a\b",
]


def strip_conversational_filler(text: str) -> str:
    cleaned = text.strip()
    for pattern in CONVERSATIONAL_FILLERS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned


def extract_keywords(text: str) -> List[str]:
    keywords = []
    stack_terms = [
        "react", "next.js", "tailwind", "flutter", "vue", "angular",
        "node", "typescript", "python", "fastapi", "go", "golang",
        "postgresql", "sqlite", "mysql", "redis", "docker", "gcp",
        "aws", "gemini", "jwt", "rest", "graphql", "grpc"
    ]
    lower = text.lower()
    for term in stack_terms:
        if re.search(r"\b" + re.escape(term) + r"\b", lower):
            keywords.append(term)
    return keywords


def polish_prompt(raw_text: str) -> Dict[str, object]:
    stripped = strip_conversational_filler(raw_text)
    detected_tech = extract_keywords(raw_text)
    
    first_sentence = raw_text.split(".")[0].strip()
    if not first_sentence:
        first_sentence = raw_text.strip()
        
    objective = strip_conversational_filler(first_sentence)
    if not objective.endswith("."):
        objective += "."
    objective = objective.capitalize()

    spec = {
        "raw_prompt": raw_text,
        "objective": objective,
        "detected_stack": detected_tech,
        "token_savings_estimate_percent": max(10, min(50, int((len(raw_text) - len(stripped)) / (len(raw_text) or 1) * 100) + 15)),
        "formatted_spec": (
            f"## Objective\n{objective}\n\n"
            f"## Detected Tech Stack\n{', '.join(detected_tech) if detected_tech else 'General / Standard'}\n\n"
            "## Quality & Verification Gates\n"
            "- [ ] Unit tests for core logic\n"
            "- [ ] Strict schema validation\n"
            "- [ ] Source file line ceiling (< 500 lines)\n"
            "- [ ] Zero mock data (real persistence)\n"
        )
    }
    return spec


def main():
    parser = argparse.ArgumentParser(description="Polish raw prompts into structured engineering specs.")
    parser.add_argument("--text", "-t", type=str, help="Raw prompt string to polish")
    parser.add_argument("--file", "-f", type=str, help="Path to file containing raw prompt")
    parser.add_argument("--output", "-o", type=str, help="Path to write formatted specification")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")

    args = parser.parse_args()

    raw_text = ""
    if args.text:
        raw_text = args.text
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        if not sys.stdin.isatty():
            raw_text = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)

    if not raw_text.strip():
        print("Error: Empty prompt input provided.", file=sys.stderr)
        sys.exit(1)

    result = polish_prompt(raw_text)

    if args.json:
        output_str = json.dumps(result, indent=2)
    else:
        output_str = str(result["formatted_spec"])

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"Polished prompt written to: {args.output}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
