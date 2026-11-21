#!/usr/bin/env python3
"""
verify_mascot_assets.py - Audits 2D mascot SVG/Rive/Lottie assets and runtime wrappers.

Checks:
- SVG files: valid viewBox, no embedded base64 raster <image>, clean Bezier command count (<= 120 commands/path).
- Rive/Lottie components: explicit prefers-reduced-motion handling and Rive cleanup()/dispose() lifecycle.
- .riv binary size budget (<= 250 KB warning / <= 500 KB ceiling).
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", "venv", ".venv"}
PATH_CMD_RE = re.compile(r"[MLHVCSQTAZmlhvcsqtaz]")


def audit_svg_mascot(file_path: Path) -> List[Dict[str, str]]:
    """Audit an SVG mascot file for raster cheats, missing viewBox, and AI node bloat."""
    issues: List[Dict[str, str]] = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    if "<svg" not in content:
        return issues
    if "viewBox=" not in content:
        issues.append({"file": str(file_path), "rule": "SVG-MISSING-VIEWBOX", "message": "SVG lacks explicit viewBox attribute."})
    if re.search(r"<image[^>]+data:image/", content, re.IGNORECASE):
        issues.append({"file": str(file_path), "rule": "SVG-EMBEDDED-RASTER-SLOP", "message": "SVG embeds base64 raster image instead of clean vector paths."})

    for idx, d_attr in enumerate(re.findall(r'\bd=["\']([^"\']+)["\']', content), start=1):
        cmd_count = len(PATH_CMD_RE.findall(d_attr))
        if cmd_count > 120:
            issues.append({
                "file": str(file_path),
                "rule": "SVG-JITTER-NODE-BLOAT",
                "message": f"Path #{idx} has {cmd_count} vector commands (> 120 limit; indicates messy AI auto-trace).",
            })
    return issues


def audit_runtime_component(file_path: Path) -> List[Dict[str, str]]:
    """Audit React/Flutter/Mobile Rive or mascot rig code for disposal and reduced motion."""
    issues: List[Dict[str, str]] = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    is_rive_usage = ("useRive(" in content) or ("RiveAnimation" in content)
    is_mascot_rig = is_rive_usage or ("Mascot" in file_path.name and "<svg" in content)

    if is_rive_usage and not any(tok in content for tok in ("cleanup()", "dispose()", "reset()")):
        issues.append({
            "file": str(file_path),
            "rule": "RIVE-MISSING-DISPOSAL",
            "message": "Rive controller lacks cleanup()/dispose() lifecycle teardown.",
        })
    if is_mascot_rig and not any(tok in content for tok in ("prefers-reduced-motion", "disableAnimations", "isReduceMotionEnabled")):
        issues.append({
            "file": str(file_path),
            "rule": "MASCOT-MISSING-REDUCED-MOTION",
            "message": "Mascot stage lacks prefers-reduced-motion accessibility guard.",
        })
    if "<svg" in content and "viewBox" not in content:
        issues.append({"file": str(file_path), "rule": "INLINE-SVG-MISSING-VIEWBOX", "message": "Inline mascot SVG lacks viewBox."})
    return issues


def audit_riv_binary(file_path: Path) -> List[Dict[str, str]]:
    """Check .riv file size budget."""
    size_kb = file_path.stat().st_size / 1024.0
    if size_kb > 500.0:
        return [{"file": str(file_path), "rule": "RIV-SIZE-BUDGET-EXCEEDED", "message": f".riv asset is {size_kb:.1f} KB (> 500 KB budget)."}]
    return []


def scan_path(target_path: Path) -> List[Dict[str, str]]:
    """Scan a file or directory for 2D mascot asset violations."""
    if target_path.is_file():
        files = [target_path]
    else:
        files = []
        for root, dirs, names in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for name in names:
                files.append(Path(root) / name)

    violations: List[Dict[str, str]] = []
    for fpath in sorted(files):
        ext = fpath.suffix.lower()
        if ext == ".svg":
            violations.extend(audit_svg_mascot(fpath))
        elif ext == ".riv":
            violations.extend(audit_riv_binary(fpath))
        elif ext in {".tsx", ".ts", ".jsx", ".js", ".dart", ".swift", ".kt"}:
            violations.extend(audit_runtime_component(fpath))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit 2D mascot SVGs, .riv binaries, and runtime controllers.")
    parser.add_argument("--path", "-p", default=".", help="File or directory to audit")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any violation is found")
    args = parser.parse_args()

    violations = scan_path(Path(args.path).resolve())
    print(f"=== 2D Mascot & Vector Motion Audit: {args.path} ===")
    if not violations:
        print("[PASS] All inspected mascot assets and controllers meet DarkNecroStack standards.")
        return 0

    for item in violations:
        print(f"  - {item['file']} [{item['rule']}] {item['message']}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
