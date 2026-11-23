#!/usr/bin/env python3
"""Computer Vision Pipeline Hygiene Auditor.

Detects unreleased VideoCapture handles, unbounded frame queues, missing EXIF
normalization, blocking OpenCV GUI calls in headless code, and implicit ONNX
Runtime providers.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class CVViolation:
    file_path: str
    line_number: int
    rule_id: str
    message: str
    severity: str = "ERROR"


VIDEO_CAPTURE_PAT = re.compile(r"\bcv2\.VideoCapture\s*\(")
UNBOUNDED_QUEUE_PAT = re.compile(r"\b(?:queue\.Queue|asyncio\.Queue)\s*\(\s*\)")
IMAGE_OPEN_PAT = re.compile(r"\bImage\.open\s*\(")
BLOCKING_GUI_PAT = re.compile(r"\bcv2\.(?:imshow|waitKey\s*\(\s*0\s*\))")
ORT_SESSION_PAT = re.compile(r"\b(?:ort|onnxruntime)\.InferenceSession\s*\(")


def _has_frame_context(content: str) -> bool:
    return any(tok in content for tok in ("cv2", "VideoCapture", "frame", "yolo", "onnx"))


def audit_cv_file(file_path: str) -> List[CVViolation]:
    """Audit a single Python source file for computer-vision hygiene issues."""
    violations: List[CVViolation] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return violations

    lines = content.splitlines()

    if VIDEO_CAPTURE_PAT.search(content) and ".release()" not in content:
        for idx, line in enumerate(lines, start=1):
            if VIDEO_CAPTURE_PAT.search(line):
                violations.append(CVViolation(
                    file_path, idx, "CV-001",
                    "cv2.VideoCapture opened without deterministic .release() cleanup.",
                ))

    if _has_frame_context(content):
        for idx, line in enumerate(lines, start=1):
            if UNBOUNDED_QUEUE_PAT.search(line):
                violations.append(CVViolation(
                    file_path, idx, "CV-002",
                    "Unbounded Queue() in CV pipeline; set maxsize=2 (drop-oldest) to prevent OOM.",
                ))

    if IMAGE_OPEN_PAT.search(content) and "exif_transpose" not in content and _has_frame_context(content):
        for idx, line in enumerate(lines, start=1):
            if IMAGE_OPEN_PAT.search(line):
                violations.append(CVViolation(
                    file_path, idx, "CV-003",
                    "Image.open() in CV pipeline lacks ImageOps.exif_transpose() orientation guard.",
                    severity="WARNING",
                ))

    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("#"):
            continue
        if BLOCKING_GUI_PAT.search(line):
            violations.append(CVViolation(
                file_path, idx, "CV-004",
                "Blocking cv2.imshow / cv2.waitKey(0) call detected; prohibited in headless services.",
            ))
        if ORT_SESSION_PAT.search(line) and "providers" not in content:
            violations.append(CVViolation(
                file_path, idx, "CV-005",
                "onnxruntime.InferenceSession missing explicit providers=[...] list (risks silent CPU fallback).",
                severity="WARNING",
            ))

    return violations


def audit_cv_directory(target_dir: str) -> List[CVViolation]:
    """Audit all Python files under target_dir."""
    violations: List[CVViolation] = []
    ignored = {".git", "node_modules", "dist", "build", "__pycache__", "venv"}
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignored]
        for fname in files:
            if fname.endswith(".py") and "verify_cv_hygiene" not in fname and "test_verify_cv_hygiene" not in fname:
                violations.extend(audit_cv_file(os.path.join(root, fname)))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit computer-vision pipelines for memory/runtime hygiene.")
    parser.add_argument("--path", default=".", help="File or directory to audit")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on errors")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        violations = audit_cv_file(args.path)
    elif os.path.isdir(args.path):
        violations = audit_cv_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.", file=sys.stderr)
        return 1

    if not violations:
        print("[PASS] Computer-vision pipeline hygiene verified.")
        return 0

    for v in violations:
        print(f"[{v.severity}] {v.file_path}:{v.line_number} [{v.rule_id}] {v.message}")
    has_errors = any(v.severity == "ERROR" for v in violations)
    return 1 if (args.strict and has_errors) or has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
