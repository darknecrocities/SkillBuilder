#!/usr/bin/env python3
"""
CLI utility to audit frontend components (JSX/TSX/HTML) for accessibility (a11y)
and common frontend quality defects.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple


def audit_component_content(content: str, filepath: str) -> List[Dict[str, str]]:
    issues = []

    # 1. Check for unlabelled images: <img ... without alt=
    img_tags = re.finditer(r"<img\b([^>]*)>", content, re.IGNORECASE)
    for match in img_tags:
        attrs = match.group(1)
        if "alt=" not in attrs.lower():
            line_no = content[:match.start()].count("\n") + 1
            issues.append({
                "file": filepath,
                "line": str(line_no),
                "rule": "A11Y-IMG-ALT",
                "severity": "ERROR",
                "message": "Image element is missing an 'alt' attribute."
            })

    # 2. Check for empty or icon-only buttons without aria-label
    button_tags = re.finditer(r"<button\b([^>]*)>([\s\S]*?)</button>", content, re.IGNORECASE)
    for match in button_tags:
        attrs = match.group(1)
        body = match.group(2).strip()
        text_without_tags = re.sub(r"<[^>]+>", "", body).strip()
        if not text_without_tags and "aria-label" not in attrs.lower() and "aria-labelledby" not in attrs.lower():
            line_no = content[:match.start()].count("\n") + 1
            issues.append({
                "file": filepath,
                "line": str(line_no),
                "rule": "A11Y-BUTTON-NAME",
                "severity": "WARNING",
                "message": "Button appears to lack accessible text or aria-label."
            })

    # 3. Check for inputs without id
    input_tags = re.finditer(r"<input\b([^>]*)>", content, re.IGNORECASE)
    for match in input_tags:
        attrs = match.group(1)
        if "type=\"hidden\"" not in attrs.lower() and "id=" not in attrs.lower() and "aria-label" not in attrs.lower():
            line_no = content[:match.start()].count("\n") + 1
            issues.append({
                "file": filepath,
                "line": str(line_no),
                "rule": "A11Y-INPUT-LABEL",
                "severity": "WARNING",
                "message": "Input element lacks an 'id' or 'aria-label' for label pairing."
            })

    return issues


def audit_directory(path: str) -> List[Dict[str, str]]:
    all_issues = []
    supported_exts = {".tsx", ".jsx", ".html", ".vue"}

    for root, _, files in os.walk(path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in supported_exts:
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                    file_issues = audit_component_content(content, full_path)
                    all_issues.extend(file_issues)
                except Exception as e:
                    print(f"Warning: Failed reading {full_path}: {e}", file=sys.stderr)

    return all_issues


def main():
    parser = argparse.ArgumentParser(description="Audit frontend files for a11y & quality issues.")
    parser.add_argument("--path", "-p", type=str, default=".", help="Directory or file path to audit")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        with open(args.path, "r", encoding="utf-8") as f:
            issues = audit_component_content(f.read(), args.path)
    elif os.path.isdir(args.path):
        issues = audit_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)

    if not issues:
        print(f"[PASS] No frontend quality or accessibility violations detected in: {args.path}")
        sys.exit(0)

    print(f"\n[FAIL] Detected {len(issues)} frontend quality issue(s):\n" + "=" * 60)
    for issue in issues:
        print(f"[{issue['severity']}] {issue['file']}:{issue['line']} - {issue['rule']}")
        print(f"  {issue['message']}")
    print("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
