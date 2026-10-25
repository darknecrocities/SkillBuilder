#!/usr/bin/env python3
"""
verify_ui_tokens.py - Linter for UI design tokens, raw emoji prohibition in interactive elements,
and button accessibility attributes.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".tsx", ".jsx", ".html", ".vue", ".svelte"}

# Common emoji regex range
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF\U0001F600-\U0001F64F\U00002702-\U000027B0\U000024C2-\U0001F251]"
)

INTERACTIVE_TAG_PATTERN = re.compile(r"<(button|a|h[1-6]|nav)[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL)
ARBITRARY_SPACING_PATTERN = re.compile(r"\b[mp][trblxy]?-\[\d+px\]")


def audit_ui_content(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []

    # 1. Detect raw emojis in interactive elements
    for match in INTERACTIVE_TAG_PATTERN.finditer(content):
        tag_name = match.group(1)
        inner_text = match.group(2)
        if EMOJI_PATTERN.search(inner_text):
            line_no = content[:match.start()].count("\n") + 1
            violations.append({
                "file": file_path,
                "line": line_no,
                "rule": "RAW-EMOJI-IN-UI-CONTROL",
                "message": f"Raw emoji detected inside <{tag_name}>. Use semantic Lucide SVG icons instead.",
                "snippet": match.group(0)[:80].replace("\n", " ")
            })

    # 2. Check for missing button type attribute
    for match in re.finditer(r"<button\b([^>]*)>", content, re.IGNORECASE):
        attrs = match.group(1)
        if "type=" not in attrs.lower():
            line_no = content[:match.start()].count("\n") + 1
            violations.append({
                "file": file_path,
                "line": line_no,
                "rule": "MISSING-BUTTON-TYPE",
                "message": "<button> is missing explicit type attribute (type=\"button\" or type=\"submit\").",
                "snippet": match.group(0)[:80]
            })

    # 3. Check for arbitrary non-token spacing
    lines = content.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        if ARBITRARY_SPACING_PATTERN.search(line):
            violations.append({
                "file": file_path,
                "line": line_idx,
                "rule": "ARBITRARY-SPACING-TOKEN",
                "message": "Arbitrary pixel spacing detected. Use design token scale (e.g., p-2, p-4, m-6).",
                "snippet": line.strip()[:80]
            })

    return violations


def scan_directory(target_path: str) -> List[Dict[str, Any]]:
    all_violations: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CHECKED_EXTENSIONS:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as file_handle:
                        content = file_handle.read()
                        all_violations.extend(audit_ui_content(fp, content))
                except Exception as err:
                    all_violations.append({"file": fp, "line": 0, "rule": "READ-ERROR", "message": str(err)})
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit UI files for design token and iconography standards.")
    parser.add_argument("--path", "-p", default=".", help="Root path to audit")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            violations = audit_ui_content(target, f.read())
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== UI Token & Iconography Audit: {target} ===")
        if not violations:
            print("[PASS] All UI elements comply with design token and vector icon standards.")
        else:
            print(f"[FAIL] Found {len(violations)} UI violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
