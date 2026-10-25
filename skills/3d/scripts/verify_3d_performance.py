#!/usr/bin/env python3
"""
verify_3d_performance.py - Audits Three.js and WebGL codebases for performance anti-patterns:
unclamped devicePixelRatio, memory leaks in render loops, missing resource disposal,
and uncompressed 3D asset loaders.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".agents", "__pycache__", "venv"}
CHECKED_EXTENSIONS = {".tsx", ".ts", ".jsx", ".js"}

UNCLAMPED_DPR_PATTERN = re.compile(
    r"\.setPixelRatio\s*\(\s*window\.devicePixelRatio\s*\)", re.IGNORECASE
)
DRACO_ABSENCE_PATTERN = re.compile(
    r"\bnew\s+GLTFLoader\s*\(", re.IGNORECASE
)
ALLOCATION_IN_RENDER_LOOP = re.compile(
    r"(?:requestAnimationFrame|useFrame)\s*\([^)]*\)\s*=>\s*\{[^}]*?\bnew\s+THREE\.(?:Vector3|Matrix4|Color|TextureLoader)\b",
    re.DOTALL
)


def audit_3d_file(file_path: str, content: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []

    # Check if file uses Three.js
    if "three" not in content.lower() and "webgl" not in content.lower():
        return violations

    # 1. Unclamped devicePixelRatio
    for match in UNCLAMPED_DPR_PATTERN.finditer(content):
        line_no = content[:match.start()].count("\n") + 1
        violations.append({
            "file": file_path,
            "line": line_no,
            "rule": "UNCLAMPED-DEVICE-PIXEL-RATIO",
            "message": "Unclamped devicePixelRatio causes GPU throttling on Retina screens. Use Math.min(window.devicePixelRatio, 2.0).",
            "snippet": match.group(0)
        })

    # 2. GLTFLoader without Draco compression
    if DRACO_ABSENCE_PATTERN.search(content):
        if "DRACOLoader" not in content and "setDRACOLoader" not in content:
            violations.append({
                "file": file_path,
                "line": 1,
                "rule": "MISSING-DRACO-COMPRESSION",
                "message": "GLTFLoader used without DRACOLoader. Compress 3D assets with Draco to minimize load time."
            })

    # 3. Allocations inside render loops
    for match in ALLOCATION_IN_RENDER_LOOP.finditer(content):
        line_no = content[:match.start()].count("\n") + 1
        violations.append({
            "file": file_path,
            "line": line_no,
            "rule": "ALLOCATION-IN-RENDER-LOOP",
            "message": "Object instantiated inside animation/render loop. Pre-allocate mutable vectors to avoid GC stutter.",
            "snippet": match.group(0)[:80].replace("\n", " ")
        })

    # 4. Renderer initialized without disposal in component
    if "new THREE.WebGLRenderer" in content and "renderer.dispose()" not in content and ".dispose" not in content:
        violations.append({
            "file": file_path,
            "line": 1,
            "rule": "MISSING-WEBGL-DISPOSAL",
            "message": "WebGLRenderer initialized without explicit .dispose() cleanup on unmount."
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
                        all_violations.extend(audit_3d_file(fp, content))
                except Exception as err:
                    all_violations.append({"file": fp, "line": 0, "rule": "READ-ERROR", "message": str(err)})
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Three.js and WebGL files for 3D performance anti-patterns.")
    parser.add_argument("--path", "-p", default=".", help="Root directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            violations = audit_3d_file(target, f.read())
    else:
        violations = scan_directory(target)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== 3D WebGL & Three.js Performance Audit: {target} ===")
        if not violations:
            print("[PASS] 3D scenes adhere to DPR clamping, Draco compression, and memory disposal guardrails.")
        else:
            print(f"[FAIL] Found {len(violations)} 3D performance violation(s):")
            for v in violations:
                print(f"  - {v['file']}:{v['line']} [{v['rule']}] {v['message']}")
                if "snippet" in v:
                    print(f"    Snippet: {v['snippet']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
