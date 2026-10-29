#!/usr/bin/env python3
"""
post_tool_use_line_guard.py - Antigravity PostToolUse line guard.
Audits modified source files against the 500-line physical limit and 350-line warning threshold.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Antigravity Automation Engine
"""

import json
import os
import sys
from pathlib import Path


def audit_file_lines(file_path: Path) -> tuple[int, str]:
    """Audits physical line count of target file."""
    if not file_path.exists() or not file_path.is_file():
        return 0, "File not found"

    # Skip minified, lock, or non-source files
    ignored_exts = {".json", ".lock", ".svg", ".png", ".jpg", ".map", ".min.js", ".min.css"}
    if any(file_path.name.endswith(ext) for ext in ignored_exts):
        return 0, "Ignored file type"

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        line_count = len(content.splitlines())
    except Exception as exc:
        return 0, f"Error reading file: {exc}"

    if line_count > 500:
        return line_count, f"[VIOLATION] {file_path} has {line_count} lines (exceeds 500-line ceiling)."
    elif line_count > 350:
        return line_count, f"[WARN] {file_path} has {line_count} lines (in 350–500 warning zone; decompose via /refactor)."
    return line_count, "Passed line guard"


def main() -> None:
    raw_input = ""
    if not sys.stdin.isatty():
        try:
            raw_input = sys.stdin.read()
        except Exception:
            pass

    path_str = ""
    if raw_input:
        try:
            payload = json.loads(raw_input)
            path_str = payload.get("Path", "") or payload.get("path", "")
        except json.JSONDecodeError:
            path_str = raw_input.strip()
    elif len(sys.argv) > 1:
        path_str = sys.argv[1]

    if not path_str:
        sys.exit(0)

    target_path = Path(path_str).resolve()
    lines, msg = audit_file_lines(target_path)
    if lines > 350:
        print(f"[SkillBuilder Line Guard] {msg}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
