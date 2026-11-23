#!/usr/bin/env python3
"""VLM & Multimodal Pipeline Hygiene Auditor.

Detects raw unresized image encoding, unthrottled video-frame loops into VLM
APIs, unconstrained VLM extraction calls, and missing network timeouts.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class VLMViolation:
    file_path: str
    line_number: int
    rule_id: str
    message: str
    severity: str = "ERROR"


B64_ENCODE_PAT = re.compile(r"\bbase64\.b64encode\s*\(")
VLM_MARKER_PAT = re.compile(r"(?:mmproj|mlx_vlm|qwen.*vl|llava|gemma.*3|images\s*:|Part\.from_bytes|generate_content)", re.IGNORECASE)
VID_LOOP_PAT = re.compile(r"while\s+.*?(?:cap\.read|VideoCapture)")
SCHEMA_GUARD_PAT = re.compile(r"(?:response_schema|format\s*=|grammar\s*=|response_format|Pydantic|BaseModel)")
HTTP_CALL_PAT = re.compile(r"(?:requests|httpx)\.(?:post|get)\s*\(")


def audit_vlm_file(file_path: str) -> List[VLMViolation]:
    """Audit a Python file for VLM visual-token and runtime hygiene."""
    violations: List[VLMViolation] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return violations

    if not VLM_MARKER_PAT.search(content):
        return violations

    lines = content.splitlines()
    has_resize = any(k in content for k in ("thumbnail(", "resize(", "max_pixels", "max_edge", "MEDIA_RESOLUTION"))

    if B64_ENCODE_PAT.search(content) and not has_resize:
        for idx, line in enumerate(lines, start=1):
            if B64_ENCODE_PAT.search(line):
                violations.append(VLMViolation(
                    file_path, idx, "VLM-001",
                    "Raw base64 image encoding into VLM without thumbnail/resize/max_pixels visual token cap.",
                ))

    if VID_LOOP_PAT.search(content) and not any(k in content for k in ("stride", "keyframe", "fps", "scene", "delta", "% ")):
        for idx, line in enumerate(lines, start=1):
            if VID_LOOP_PAT.search(line):
                violations.append(VLMViolation(
                    file_path, idx, "VLM-002",
                    "Video capture loop feeds VLM without keyframe/stride/scene-delta throttling.",
                ))

    if any(k in content for k in ("extract", "bounding", "bbox", "ocr")) and not SCHEMA_GUARD_PAT.search(content):
        violations.append(VLMViolation(
            file_path, 1, "VLM-003",
            "VLM extraction/grounding code lacks structured schema enforcement (response_schema/format/grammar).",
            severity="WARNING",
        ))

    for idx, line in enumerate(lines, start=1):
        if HTTP_CALL_PAT.search(line) and "timeout" not in line:
            window = "\n".join(lines[max(0, idx - 1):min(len(lines), idx + 5)])
            if "timeout" not in window:
                violations.append(VLMViolation(
                    file_path, idx, "VLM-004",
                    "VLM HTTP call missing explicit timeout=(connect, read) budget.",
                ))

    return violations


def audit_vlm_directory(target_dir: str) -> List[VLMViolation]:
    """Audit all Python files under target_dir."""
    violations: List[VLMViolation] = []
    ignored = {".git", "node_modules", "dist", "build", "__pycache__", "venv"}
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignored]
        for fname in files:
            if fname.endswith(".py") and "verify_vlm_hygiene" not in fname and "test_verify_vlm_hygiene" not in fname:
                violations.extend(audit_vlm_file(os.path.join(root, fname)))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit VLM pipelines for visual token and runtime hygiene.")
    parser.add_argument("--path", default=".", help="File or directory to audit")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on errors")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        violations = audit_vlm_file(args.path)
    elif os.path.isdir(args.path):
        violations = audit_vlm_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.", file=sys.stderr)
        return 1

    if not violations:
        print("[PASS] VLM & multimodal pipeline hygiene verified.")
        return 0

    for v in violations:
        print(f"[{v.severity}] {v.file_path}:{v.line_number} [{v.rule_id}] {v.message}")
    has_errors = any(v.severity == "ERROR" for v in violations)
    return 1 if (args.strict and has_errors) or has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
