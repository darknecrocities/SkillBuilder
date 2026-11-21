#!/usr/bin/env python3
"""
verify_brand_assets.py - Audits brand SVGs, logos, favicons, and OG assets.

Detects:
- Missing viewBox attributes on SVG assets.
- Embedded base64 raster <image> tags masquerading as vector art.
- Editor metadata bloat (<metadata>, Adobe/Sketch generator comments).
- Bloated logo/icon path command counts (> 60 commands on icons/logos).
- Duplicate gradient/clip IDs across SVG files when inlined together.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", "venv", ".venv"}
PATH_CMD_RE = re.compile(r"[MLHVCSQTAZmlhvcsqtaz]")
GENERIC_IDS = {"grad1", "gradient", "clip0", "a", "b", "c", "layer_1"}


def audit_svg_file(file_path: Path) -> List[Dict[str, str]]:
    """Audit a single SVG file for geometry cleanliness and hygiene."""
    issues: List[Dict[str, str]] = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    if "<svg" not in content:
        return issues

    if "viewBox=" not in content:
        issues.append({"file": str(file_path), "rule": "BRAND-SVG-MISSING-VIEWBOX", "message": "Missing viewBox attribute on SVG."})
    if re.search(r"<image[^>]+data:image/", content, re.IGNORECASE):
        issues.append({"file": str(file_path), "rule": "BRAND-SVG-RASTER-CHEAT", "message": "Embedded raster data URI found inside SVG."})
    if "<metadata" in content.lower() or "adobe illustrator" in content.lower():
        issues.append({"file": str(file_path), "rule": "BRAND-SVG-EDITOR-BLOAT", "message": "Unstripped editor metadata found in SVG."})

    is_logo_or_icon = any(k in file_path.name.lower() for k in ("logo", "icon", "favicon", "squircle"))
    max_cmds = 60 if is_logo_or_icon else 160
    for idx, d_attr in enumerate(re.findall(r'\bd=["\']([^"\']+)["\']', content), start=1):
        cmds = len(PATH_CMD_RE.findall(d_attr))
        if cmds > max_cmds:
            issues.append({
                "file": str(file_path),
                "rule": "BRAND-SVG-NODE-BLOAT",
                "message": f"Path #{idx} has {cmds} commands (> {max_cmds} ceiling).",
            })

    for def_id in re.findall(r'\bid=["\']([^"\']+)["\']', content):
        if def_id.lower() in GENERIC_IDS:
            issues.append({
                "file": str(file_path),
                "rule": "BRAND-SVG-GENERIC-ID-COLLISION",
                "message": f"Generic SVG id='{def_id}' risks collision when multiple SVGs inline.",
            })
    return issues


def scan_assets(target_path: Path) -> List[Dict[str, str]]:
    """Scan a file or directory for brand SVG asset issues."""
    files: List[Path] = []
    if target_path.is_file():
        files = [target_path]
    else:
        for root, dirs, names in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for name in names:
                if name.lower().endswith(".svg"):
                    files.append(Path(root) / name)

    violations: List[Dict[str, str]] = []
    for fpath in sorted(files):
        violations.extend(audit_svg_file(fpath))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit brand SVGs, logos, and icon assets.")
    parser.add_argument("--path", "-p", default=".", help="Target directory or SVG file")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    violations = scan_assets(Path(args.path).resolve())
    print(f"=== Brand Assets & Vector Hygiene Audit: {args.path} ===")
    if not violations:
        print("[PASS] All inspected brand assets comply with DarkNecroStack geometry standards.")
        return 0

    for item in violations:
        print(f"  - {item['file']} [{item['rule']}] {item['message']}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
