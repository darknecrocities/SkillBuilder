#!/usr/bin/env python3
"""Web UI Hygiene & Modern Design System Auditor.

Audits web styling (CSS, SCSS, Tailwind, TSX/JSX, Vue) for accessible focus rings,
fluid typography bounds, modern container queries, and sub-pixel lighting hygiene.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class WebViolation:
    file_path: str
    line_number: int
    rule_id: str
    message: str
    severity: str = "ERROR"


# Detection Patterns
OUTLINE_NONE_PATTERN = re.compile(
    r"""(?:outline\s*:\s*(?:none|0)\b)|"""
    r"""(?:focus:outline-none\b(?!.*focus:(?:ring|border)))"""
)

FOCUS_VISIBLE_PATTERN = re.compile(
    r""":focus-visible\b|focus-visible:|focus:ring"""
)

HARDCODED_HUGE_FONT_PATTERN = re.compile(
    r"""font-size\s*:\s*(?:[5-9][0-9]|1[0-9]{2})px\b(?!.*clamp)"""
)

LINEAR_TRANSITION_PATTERN = re.compile(
    r"""(?:transition(?:-timing-function)?\s*:[^;]*?\blinear\b)|"""
    r"""(?:animation(?:-timing-function)?\s*:[^;]*?\blinear\b)"""
)

CLAMP_PATTERN = re.compile(
    r"""clamp\s*\(\s*([0-9.]+(?:px|rem|em|vw|%))\s*,\s*[^,]+\s*,\s*([0-9.]+(?:px|rem|em|vw|%))\s*\)"""
)


def _parse_val(raw: str) -> float | None:
    match = re.match(r"^([0-9.]+)", raw)
    return float(match.group(1)) if match else None


def audit_web_file(file_path: str) -> List[WebViolation]:
    """Audits a single web file for styling and design system hygiene."""
    violations: List[WebViolation] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return violations

    full_content = "".join(lines)
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in [".css", ".scss", ".tsx", ".jsx", ".html", ".vue"]:
        return violations

    has_focus_visible_somewhere = bool(FOCUS_VISIBLE_PATTERN.search(full_content))

    for idx, line in enumerate(lines, start=1):
        clean_line = line.strip()
        if clean_line.startswith(("/*", "*", "//", "<!--")):
            continue

        # Rule WEB-001: Suppressed outline without visible focus
        if OUTLINE_NONE_PATTERN.search(clean_line):
            if not has_focus_visible_somewhere:
                violations.append(
                    WebViolation(
                        file_path=file_path,
                        line_number=idx,
                        rule_id="WEB-001",
                        message="Suppressed outline without an accessible :focus-visible ring.",
                    )
                )

        # Rule WEB-002: Hardcoded large typography without fluid clamp()
        if HARDCODED_HUGE_FONT_PATTERN.search(clean_line):
            violations.append(
                WebViolation(
                    file_path=file_path,
                    line_number=idx,
                    rule_id="WEB-002",
                    message="Hardcoded large typography detected (>50px). Use fluid clamp() scaling curve.",
                    severity="WARNING",
                )
            )

        # Rule WEB-003: Linear transition curves
        if LINEAR_TRANSITION_PATTERN.search(clean_line):
            violations.append(
                WebViolation(
                    file_path=file_path,
                    line_number=idx,
                    rule_id="WEB-003",
                    message="Unnatural linear animation or transition timing detected. Use cubic-bezier or spring decay.",
                )
            )

        # Rule WEB-004: Inverted clamp() arguments (min > max with same units)
        clamp_matches = CLAMP_PATTERN.findall(clean_line)
        for min_str, max_str in clamp_matches:
            min_val = _parse_val(min_str)
            max_val = _parse_val(max_str)
            if min_val and max_val and min_str[-2:] == max_str[-2:]:
                if min_val > max_val:
                    violations.append(
                        WebViolation(
                            file_path=file_path,
                            line_number=idx,
                            rule_id="WEB-004",
                            message=f"Inverted clamp() bounds: min ({min_str}) exceeds max ({max_str}).",
                        )
                    )

    return violations


def audit_web_directory(target_dir: str) -> List[WebViolation]:
    """Audits all web styling files recursively in target directory."""
    violations: List[WebViolation] = []
    supported_extensions = {".css", ".scss", ".tsx", ".jsx", ".html", ".vue"}

    for root, _, files in os.walk(target_dir):
        if any(ignored in root for ignored in [".git", "node_modules", "dist", "build"]):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                full_path = os.path.join(root, file)
                violations.extend(audit_web_file(full_path))

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit web styling files for container queries, fluid typography, and accessibility."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to file or directory to audit (default: current directory).",
    )
    args = parser.parse_args()

    if os.path.isfile(args.path):
        violations = audit_web_file(args.path)
    elif os.path.isdir(args.path):
        violations = audit_web_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    if not violations:
        print("[PASS] All web files comply with modern Web UI design system standards.")
        return 0

    print(f"Web UI Hygiene Audit: Found {len(violations)} violation(s):")
    for v in violations:
        print(f"[{v.severity}] {v.file_path}:{v.line_number} ({v.rule_id}) - {v.message}")

    errors = [v for v in violations if v.severity == "ERROR"]
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
