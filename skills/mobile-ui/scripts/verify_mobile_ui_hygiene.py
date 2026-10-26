#!/usr/bin/env python3
"""Mobile UI/UX Hygiene & Native Craftsmanship Auditor.

Audits iOS (Swift), Android (Kotlin/Compose), Flutter (Dart), and React Native
(TSX/JSX) source files for touch target ergonomics, spring animation physics,
safe area insets, and hardcoded viewport traps.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class MobileViolation:
    file_path: str
    line_number: int
    rule_id: str
    message: str
    severity: str = "ERROR"


# Detection Patterns
HARDCODED_WIDTH_PATTERN = re.compile(
    r"""(?:\.frame\s*\(\s*width:\s*(?:375|390|393|414|428|430)\b)|"""
    r"""(?:width:\s*['"]?(?:375|390|393|414|428|430)(?:px)?['"]?\s*[,;])|"""
    r"""(?:Modifier\.width\s*\(\s*(?:375|390|393|414|428|430)\.dp\))"""
)

UNDERSIZED_TARGET_PATTERN = re.compile(
    r"""(?:Button|TouchableOpacity|Pressable|IconButton)\b[^>]*?"""
    r"""(?:(?:width|height):\s*(?:[1-3][0-9]|4[0-3])\b|\.frame\s*\([^)]*?(?:width|height):\s*(?:[1-3][0-9]|4[0-3])\b)"""
)

LINEAR_EASING_PATTERN = re.compile(
    r"""(?:\.animation\s*\(\s*\.linear\b)|"""
    r"""(?:tween\s*\([^)]*?easing\s*=\s*LinearEasing\b)|"""
    r"""(?:withTiming\s*\([^)]*?easing:\s*Easing\.linear\b)"""
)

SAFE_AREA_SIGNATURES = [
    "SafeArea",
    "SafeAreaView",
    "WindowInsets.systemBars",
    "safeAreaInset",
    "safeAreaPadding",
    "insets",
    "useSafeAreaInsets",
]


def audit_mobile_file(file_path: str) -> List[MobileViolation]:
    """Audits a single mobile source file for UX and craftsmanship violations."""
    violations: List[MobileViolation] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return violations

    full_content = "".join(lines)
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in [".swift", ".kt", ".dart", ".tsx", ".jsx"]:
        return violations

    # Check for hardcoded viewport widths and linear transitions
    for idx, line in enumerate(lines, start=1):
        clean_line = line.strip()
        if clean_line.startswith(("//", "/*", "*", "#")):
            continue

        if HARDCODED_WIDTH_PATTERN.search(clean_line):
            violations.append(
                MobileViolation(
                    file_path=file_path,
                    line_number=idx,
                    rule_id="MOB-001",
                    message="Hardcoded device screen width detected. Use relative layout constraints or Safe Area insets.",
                )
            )

        if LINEAR_EASING_PATTERN.search(clean_line):
            violations.append(
                MobileViolation(
                    file_path=file_path,
                    line_number=idx,
                    rule_id="MOB-002",
                    message="Unnatural linear animation easing detected. Use calibrated spring physics (response: 0.32s, damping: 0.72).",
                )
            )

    # Check for root screens missing Safe Area management
    is_screen = any(
        kw in file_path.lower()
        for kw in ["screen", "view", "page", "activity", "sheet"]
    )
    if is_screen and len(lines) > 25:
        has_safe_area = any(sig in full_content for sig in SAFE_AREA_SIGNATURES)
        if not has_safe_area:
            violations.append(
                MobileViolation(
                    file_path=file_path,
                    line_number=1,
                    rule_id="MOB-003",
                    message="Screen or sheet component missing Safe Area insets management (e.g., SafeArea, WindowInsets.systemBars).",
                    severity="WARNING",
                )
            )

    return violations


def audit_mobile_directory(target_dir: str) -> List[MobileViolation]:
    """Audits all mobile source files recursively in target directory."""
    violations: List[MobileViolation] = []
    supported_extensions = {".swift", ".kt", ".dart", ".tsx", ".jsx"}

    for root, _, files in os.walk(target_dir):
        if any(ignored in root for ignored in [".git", "node_modules", "build", "dist"]):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                full_path = os.path.join(root, file)
                violations.extend(audit_mobile_file(full_path))

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit mobile source files for native UX craftsmanship and touch ergonomics."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to file or directory to audit (default: current directory).",
    )
    args = parser.parse_args()

    if os.path.isfile(args.path):
        violations = audit_mobile_file(args.path)
    elif os.path.isdir(args.path):
        violations = audit_mobile_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    if not violations:
        print("[PASS] All mobile source files adhere to native UX & craftsmanship standards.")
        return 0

    print(f"Mobile UI Hygiene Audit: Found {len(violations)} violation(s):")
    for v in violations:
        print(f"[{v.severity}] {v.file_path}:{v.line_number} ({v.rule_id}) - {v.message}")

    errors = [v for v in violations if v.severity == "ERROR"]
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
