#!/usr/bin/env python3
"""
verify_media_wasm_hygiene.py - Audits browser media/WASM code for ObjectURL and Worker leaks.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", "venv", ".venv"}
CHECKED_EXTS = {".ts", ".tsx", ".js", ".jsx"}


def audit_media_file(file_path: Path) -> List[Dict[str, str]]:
    """Inspect a browser media/WASM file for ObjectURL, Worker, and AudioContext leaks."""
    issues: List[Dict[str, str]] = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    if "createObjectURL(" in content and "revokeObjectURL(" not in content:
        issues.append({
            "file": str(file_path),
            "rule": "MEDIA-OBJECTURL-LEAK",
            "message": "URL.createObjectURL() called without matching URL.revokeObjectURL().",
        })
    if "new Worker(" in content and ".terminate(" not in content:
        issues.append({
            "file": str(file_path),
            "rule": "MEDIA-WORKER-NO-TERMINATE",
            "message": "Web Worker instantiated without .terminate() teardown.",
        })
    if "new AudioContext(" in content and ".close(" not in content:
        issues.append({
            "file": str(file_path),
            "rule": "MEDIA-AUDIOCONTEXT-LEAK",
            "message": "AudioContext created without .close() cleanup.",
        })
    return issues


def scan_directory(target_path: Path) -> List[Dict[str, str]]:
    """Scan file or directory for browser media lifecycle violations."""
    if target_path.is_file():
        return audit_media_file(target_path)

    violations: List[Dict[str, str]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for fname in sorted(files):
            if Path(fname).suffix.lower() in CHECKED_EXTS:
                violations.extend(audit_media_file(Path(root) / fname))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit browser media, Canvas, and WASM lifecycles.")
    parser.add_argument("--path", "-p", default=".", help="Path to inspect")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations")
    args = parser.parse_args()

    findings = scan_directory(Path(args.path).resolve())
    print(f"=== Browser Media & WASM Lifecycle Audit: {args.path} ===")
    if not findings:
        print("[PASS] Zero ObjectURL, Worker, or AudioContext leaks detected.")
        return 0
    for f in findings:
        print(f"  - {f['file']} [{f['rule']}] {f['message']}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
