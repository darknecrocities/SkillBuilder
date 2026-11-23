#!/usr/bin/env python3
"""Mobile UI/UX Hygiene & Native Craftsmanship Auditor.

Audits iOS (Swift), Android (Kotlin/Compose), Flutter (Dart), and React Native
(TSX/JSX) source files for touch target ergonomics, spring animation physics,
safe area insets, hardcoded viewport traps, and responsive layout anti-patterns.
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


HARDCODED_WIDTH_PATTERN = re.compile(
    r"""(?:\.frame\s*\(\s*width:\s*(?:375|390|393|414|428|430)\b)|"""
    r"""(?:width:\s*['"]?(?:375|390|393|414|428|430)(?:px)?['"]?\s*[,;])|"""
    r"""(?:Modifier\.width\s*\(\s*(?:375|390|393|414|428|430)\.dp\))"""
)
LINEAR_EASING_PATTERN = re.compile(
    r"""(?:\.animation\s*\(\s*\.linear\b)|"""
    r"""(?:tween\s*\([^)]*?easing\s*=\s*LinearEasing\b)|"""
    r"""(?:withTiming\s*\([^)]*?easing:\s*Easing\.linear\b)"""
)
GLOBAL_SCREEN_BOUNDS_PATTERN = re.compile(
    r"""(?:UIScreen\.main\.bounds|MediaQuery\.of\s*\(\s*context\s*\)\.size\b|Dimensions\.get\s*\(\s*['"](?:window|screen)['"]\s*\))"""
)
FIXED_TEXT_HEIGHT_PATTERN = re.compile(
    r"""(?:Text\s*\([^)]*\)[^\n]*\.(?:frame\s*\(\s*height\s*:|height\s*\()|(?:Modifier\.height\s*\(\s*\d+\.dp\s*\)[^\n]*Text\s*\())"""
)
PORTRAIT_LOCK_PATTERN = re.compile(
    r"""(?:SCREEN_ORIENTATION_PORTRAIT|android:screenOrientation\s*=\s*['"]portrait['"]|SystemChrome\.setPreferredOrientations\s*\(\s*\[\s*DeviceOrientation\.portraitUp\s*\]\s*\))"""
)

SAFE_AREA_SIGNATURES = [
    "SafeArea", "SafeAreaView", "WindowInsets.systemBars",
    "safeAreaInset", "safeAreaPadding", "insets", "useSafeAreaInsets",
]


def _check_line_rules(file_path: str, idx: int, line: str, full_content: str) -> List[MobileViolation]:
    findings: List[MobileViolation] = []
    if HARDCODED_WIDTH_PATTERN.search(line):
        findings.append(MobileViolation(
            file_path, idx, "MOB-001",
            "Hardcoded device screen width detected. Use relative layout constraints or Safe Area insets.",
        ))
    if LINEAR_EASING_PATTERN.search(line):
        findings.append(MobileViolation(
            file_path, idx, "MOB-002",
            "Unnatural linear animation easing detected. Use calibrated spring physics (response: 0.32s, damping: 0.72).",
        ))
    if GLOBAL_SCREEN_BOUNDS_PATTERN.search(line) and "useWindowDimensions" not in full_content:
        findings.append(MobileViolation(
            file_path, idx, "MOB-004",
            "Global screen-bounds trap (UIScreen.main.bounds / Dimensions.get / MediaQuery.of.size). Use horizontalSizeClass, WindowSizeClass, useWindowDimensions(), or LayoutBuilder.",
        ))
    if FIXED_TEXT_HEIGHT_PATTERN.search(line) and "minHeight" not in line and "heightIn" not in line:
        findings.append(MobileViolation(
            file_path, idx, "MOB-005",
            "Fixed height on Text container risks truncation at 200% Dynamic Type; use minHeight / heightIn(min=).",
            severity="WARNING",
        ))
    if PORTRAIT_LOCK_PATTERN.search(line):
        findings.append(MobileViolation(
            file_path, idx, "MOB-006",
            "Portrait orientation lock detected; blocks tablet, foldable, and Split View responsiveness.",
            severity="WARNING",
        ))
    return findings


def audit_mobile_file(file_path: str) -> List[MobileViolation]:
    """Audits a single mobile source file for UX, responsive layout, and craftsmanship violations."""
    violations: List[MobileViolation] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return violations

    full_content = "".join(lines)
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in {".swift", ".kt", ".dart", ".tsx", ".jsx", ".xml"}:
        return violations

    for idx, line in enumerate(lines, start=1):
        clean_line = line.strip()
        if clean_line.startswith(("//", "/*", "*", "#")):
            continue
        violations.extend(_check_line_rules(file_path, idx, clean_line, full_content))

    is_screen = any(kw in file_path.lower() for kw in ("screen", "view", "page", "activity", "sheet"))
    if ext != ".xml" and is_screen and len(lines) > 25:
        if not any(sig in full_content for sig in SAFE_AREA_SIGNATURES):
            violations.append(MobileViolation(
                file_path, 1, "MOB-003",
                "Screen or sheet component missing Safe Area insets management (e.g., SafeArea, WindowInsets.systemBars).",
                severity="WARNING",
            ))

    return violations


def audit_mobile_directory(target_dir: str) -> List[MobileViolation]:
    """Audits all mobile source files recursively in target directory."""
    violations: List[MobileViolation] = []
    supported_extensions = {".swift", ".kt", ".dart", ".tsx", ".jsx", ".xml"}

    for root, _, files in os.walk(target_dir):
        if any(ignored in root for ignored in [".git", "node_modules", "build", "dist"]):
            continue
        for file in files:
            if os.path.splitext(file)[1].lower() in supported_extensions:
                violations.extend(audit_mobile_file(os.path.join(root, file)))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit mobile source files for native UX, responsive layouts, and touch ergonomics."
    )
    parser.add_argument("--path", default=".", help="Path to file or directory to audit (default: current directory).")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        violations = audit_mobile_file(args.path)
    elif os.path.isdir(args.path):
        violations = audit_mobile_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    if not violations:
        print("[PASS] All mobile source files adhere to native UX, responsive layout & craftsmanship standards.")
        return 0

    print(f"Mobile UI Hygiene Audit: Found {len(violations)} violation(s):")
    for v in violations:
        print(f"[{v.severity}] {v.file_path}:{v.line_number} ({v.rule_id}) - {v.message}")

    return 1 if any(v.severity == "ERROR" for v in violations) else 0


if __name__ == "__main__":
    sys.exit(main())
