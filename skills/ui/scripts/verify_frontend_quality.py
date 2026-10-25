#!/usr/bin/env python3
"""
CLI utility to audit frontend components (JSX/TSX/HTML) for accessibility (a11y)
and Anti-Vibe-Coding quality guardrails.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder
"""

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple


COMMON_UI_EMOJIS = r"[\U0001F680\U00002728\U0001F525\U0001F389\U0001F4A1\U00002699\U0001F916\U00002B50\U0001F6A7\U0001F4E6]"


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

    # 3. Check for inputs without id or aria-label
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

    # 4. Anti-Vibe-Coding: Check for raw emojis in UI text nodes
    # Exclude comments
    non_comment_content = re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", "", content)
    emoji_matches = re.finditer(COMMON_UI_EMOJIS, non_comment_content)
    for match in emoji_matches:
        line_no = content[:match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "UI-ANTI-VIBE-EMOJI",
            "severity": "ERROR",
            "message": "Raw emoji detected in UI text node. Use semantic SVG vector icons instead of emojis."
        })

    # 5. Anti-Vibe-Coding: Check for neon glowing drop-shadows or borders
    glow_match = re.search(r"(?:shadow-\[0_0_\d+px|drop-shadow-\[0_0_\d+px|shadow-green-500\/50|shadow-emerald-500)", content, re.IGNORECASE)
    if glow_match:
        line_no = content[:glow_match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "UI-ANTI-VIBE-GLOW",
            "severity": "ERROR",
            "message": "Neon glowing drop-shadow or border detected. Use clean neutral borders (1px) without glowing effects."
        })

    # 6. Anti-Vibe-Coding: Check for purple/indigo linear gradient tropes
    gradient_match = re.search(r"bg-gradient-to-[a-z]+\s+(?:from-purple|from-indigo|from-violet)", content, re.IGNORECASE)
    if gradient_match:
        line_no = content[:gradient_match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "UI-ANTI-VIBE-PURPLE-GRADIENT",
            "severity": "WARNING",
            "message": "Purple/indigo gradient trope detected. Use clean neutral palettes with purposeful functional accents."
        })

    # 7. Anti-Vibe-Coding: Check for sluggish transition-all or excessive transition durations
    sluggish_match = re.search(r"(?:transition-all\s+duration-(?:500|700|1000)|transition:\s*all\s+(?:0\.[5-9]|[1-9]\d*)\s*s|transition:\s*all\s+[5-9]\d{2,}\s*ms)", content, re.IGNORECASE)
    if sluggish_match:
        line_no = content[:sluggish_match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "UI-SLUGGISH-TRANSITION",
            "severity": "WARNING",
            "message": "Sluggish transition or blanket 'transition-all' with high duration detected. Use specific property transitions (e.g., transition-colors) with snappy durations (150-250ms) or spring physics."
        })

    # 8. Anti-Vibe-Coding: Check for tacky, excessive drop-shadows
    shadow_match = re.search(r"\b(?:shadow-2xl|drop-shadow-2xl)\b|shadow-\[0_2[0-9]px|shadow-\[0_3[0-9]px", content, re.IGNORECASE)
    if shadow_match:
        line_no = content[:shadow_match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "UI-TACKY-SHADOW",
            "severity": "WARNING",
            "message": "Heavy drop-shadow detected. Prefer crisp hairline specular borders (1px) and subtle depth (shadow-sm/md) over muddy 2XL blur shadows."
        })

    # 9. Anti-Vibe-Coding & A11y: Check for continuous CSS animation without motion-reduce fallback
    for anim_match in re.finditer(r"\b(animate-spin|animate-bounce|animate-ping)\b", content):
        line_start = content.rfind("\n", 0, anim_match.start())
        line_end = content.find("\n", anim_match.end())
        line_str = content[line_start if line_start != -1 else 0:line_end if line_end != -1 else len(content)]
        if "motion-reduce" not in line_str:
            line_no = content[:anim_match.start()].count("\n") + 1
            issues.append({
                "file": filepath,
                "line": str(line_no),
                "rule": "UI-MOTION-NO-FALLBACK",
                "severity": "WARNING",
                "message": f"Continuous animation '{anim_match.group(1)}' lacks a 'motion-reduce:animate-none' fallback for accessibility."
            })
            break

    # 10. Anti-Slop: Check for generic AI 3-card soup placeholder pattern
    card_soup_match = re.search(r"(?:grid-cols-3|grid-cols-1\s+md:grid-cols-3)[^>]*>[\s\S]*?(?:Feature\s+[1-3]|Card\s+[1-3]|Title\s+[1-3]|Benefit\s+[1-3])", content, re.IGNORECASE)
    if card_soup_match:
        line_no = content[:card_soup_match.start()].count("\n") + 1
        issues.append({
            "file": filepath,
            "line": str(line_no),
            "rule": "UI-GENERIC-CARD-SOUP",
            "severity": "WARNING",
            "message": "Generic AI 3-card soup pattern detected with placeholder cards. Use domain-specific asymmetrical layouts or purposeful data grids."
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
    parser = argparse.ArgumentParser(description="Audit frontend files for a11y & anti-vibe-coding quality.")
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
        print(f"[PASS] No frontend quality, a11y, or anti-vibe-coding violations detected in: {args.path}")
        sys.exit(0)

    print(f"\n[FAIL] Detected {len(issues)} frontend quality issue(s):\n" + "=" * 60)
    for issue in issues:
        print(f"[{issue['severity']}] {issue['file']}:{issue['line']} - {issue['rule']}")
        print(f"  {issue['message']}")
    print("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
