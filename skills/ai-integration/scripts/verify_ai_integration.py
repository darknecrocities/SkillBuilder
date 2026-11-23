#!/usr/bin/env python3
"""Universal AI Integration Hygiene Auditor.

Detects hardcoded AI service URLs, silent cloud fallbacks lacking privacy mode
gates, streaming clients missing AbortController signal cleanup, and hardcoded
API secrets.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class IntegrationViolation:
    file_path: str
    line_number: int
    rule_id: str
    message: str
    severity: str = "ERROR"


HARDCODED_URL_PAT = re.compile(
    r"""['"]https?://(?:127\.0\.0\.1|localhost):(?:11434|8080|8000)/[^'"]*['"]"""
)
HARDCODED_KEY_PAT = re.compile(r"""(?:GEMINI_API_KEY|OPENAI_API_KEY)\s*=\s*['"][A-Za-z0-9_\-]{16,}['"]""")
CLOUD_FALLBACK_PAT = re.compile(r"""except\b[^:]*:\s*(?:\n\s+.*)*(?:gemini|openai|anthropic|cloud_gw)""", re.IGNORECASE)
STREAM_FETCH_PAT = re.compile(r"""fetch\s*\([^)]*(?:/chat|/generate|/completion|/stream)""")


def audit_integration_file(file_path: str) -> List[IntegrationViolation]:
    """Audit a single Python or TypeScript file for AI integration hygiene."""
    violations: List[IntegrationViolation] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return violations

    lines = content.splitlines()
    ext = os.path.splitext(file_path)[1].lower()

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(("#", "//", "/*")):
            continue
        if HARDCODED_URL_PAT.search(line) and "getenv" not in line and "process.env" not in line:
            violations.append(IntegrationViolation(
                file_path, idx, "AII-001",
                "Hardcoded local AI URL detected; inject AI_BASE_URL via environment config.",
                severity="WARNING",
            ))
        if HARDCODED_KEY_PAT.search(line):
            violations.append(IntegrationViolation(
                file_path, idx, "AII-004",
                "Hardcoded AI API key literal detected; load from Secret Manager / .env.",
            ))

    if ext == ".py" and CLOUD_FALLBACK_PAT.search(content):
        if not any(k in content for k in ("AI_PRIVACY_MODE", "PrivacyMode", "hybrid_consent", "allow_cloud")):
            violations.append(IntegrationViolation(
                file_path, 1, "AII-002",
                "Silent cloud fallback in exception handler without AI_PRIVACY_MODE / consent gate.",
            ))

    if ext in {".ts", ".tsx", ".js"} and STREAM_FETCH_PAT.search(content) and "AbortController" not in content and "signal" not in content:
        for idx, line in enumerate(lines, start=1):
            if STREAM_FETCH_PAT.search(line):
                violations.append(IntegrationViolation(
                    file_path, idx, "AII-003",
                    "Streaming AI fetch() lacks AbortController / signal cancellation cleanup.",
                ))

    return violations


def audit_integration_directory(target_dir: str) -> List[IntegrationViolation]:
    """Audit Python and TypeScript files under target_dir."""
    violations: List[IntegrationViolation] = []
    ignored = {".git", "node_modules", "dist", "build", "__pycache__", "venv"}
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignored]
        for fname in files:
            if fname.endswith((".py", ".ts", ".tsx", ".js")) and "verify_ai_integration" not in fname and "test_verify_ai_integration" not in fname:
                violations.extend(audit_integration_file(os.path.join(root, fname)))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit cross-project AI/CV/VLM integration hygiene.")
    parser.add_argument("--path", default=".", help="File or directory to audit")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on errors")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        violations = audit_integration_file(args.path)
    elif os.path.isdir(args.path):
        violations = audit_integration_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.", file=sys.stderr)
        return 1

    if not violations:
        print("[PASS] AI integration gateway hygiene verified.")
        return 0

    for v in violations:
        print(f"[{v.severity}] {v.file_path}:{v.line_number} [{v.rule_id}] {v.message}")
    has_errors = any(v.severity == "ERROR" for v in violations)
    return 1 if (args.strict and has_errors) or has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
