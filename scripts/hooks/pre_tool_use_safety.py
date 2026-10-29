#!/usr/bin/env python3
"""
pre_tool_use_safety.py - Antigravity PreToolUse safety gate.
Intercepts destructive filesystem or database commands to prevent accidental data loss.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Antigravity Automation Engine
"""

import json
import os
import re
import sys

DANGEROUS_PATTERNS = [
    (re.compile(r"\brm\s+-[rRfF]+\s+(?:/|~|\$HOME|\.\.)(?:\s|$)", re.IGNORECASE), "Destructive root/home directory deletion detected"),
    (re.compile(r"\b(?:DROP\s+TABLE|DROP\s+DATABASE|TRUNCATE)\b", re.IGNORECASE), "Destructive database drop/truncate detected"),
    (re.compile(r"\bgit\s+push\s+(?:--force|-f)\s+(?:origin\s+)?(?:main|master)\b", re.IGNORECASE), "Force push to protected primary git branch detected"),
]


def audit_command_safety(command_str: str) -> tuple[bool, str]:
    """Audits shell command for dangerous operations."""
    for pattern, warning in DANGEROUS_PATTERNS:
        if pattern.search(command_str):
            return False, warning
    return True, "Command passed safety gate"


def main() -> None:
    # Read tool execution payload from stdin if available
    raw_input = ""
    if not sys.stdin.isatty():
        try:
            raw_input = sys.stdin.read()
        except Exception:
            pass

    cmd_to_check = ""
    if raw_input:
        try:
            payload = json.loads(raw_input)
            cmd_to_check = payload.get("CommandLine", "") or payload.get("command", "") or ""
        except json.JSONDecodeError:
            cmd_to_check = raw_input
    elif len(sys.argv) > 1:
        cmd_to_check = " ".join(sys.argv[1:])

    if not cmd_to_check:
        sys.exit(0)

    is_safe, message = audit_command_safety(cmd_to_check)
    if not is_safe:
        print(f"[SECURITY INTERCEPT] {message}", file=sys.stderr)
        print(f"Command blocked by SkillBuilder PreToolUse Safety Gate: '{cmd_to_check}'", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
