#!/usr/bin/env python3
"""Local LLM Hygiene & Quantized Inference Auditor.

Audits local model configurations, Python client code, and deployment scripts
for quantization profile validity, GPU layer offloading, GBNF grammar constraints,
and timeout/fallback resilience.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class LocalLLMViolation:
    file_path: str
    line_number: int
    rule_id: str
    message: str
    severity: str = "ERROR"


# Detection Patterns
LOW_QUANT_PATTERN = re.compile(
    r"""\b(?:q2_k|q3_k_s|q3_k_m|q3_k_l)\b""", re.IGNORECASE
)

LOCAL_HTTP_NO_TIMEOUT_PATTERN = re.compile(
    r"""(?:requests|httpx|aiohttp)\.(?:post|get)\s*\(\s*['"][^'"]*(?:11434|8080|localhost|127\.0\.0\.1)[^'"]*['"](?![^)]*timeout\s*=)"""
)

LLAMA_SERVER_ZERO_GPU_PATTERN = re.compile(
    r"""llama-server\b[^;\n]*?(?:-ngl\s+0\b|--n-gpu-layers\s+0\b)"""
)

JSON_PROMPT_WITHOUT_GRAMMAR_PATTERN = re.compile(
    r"""(?i)(?:respond in json|output json|json object)\b[^;]*?(?:call_local|generate|completion)\s*\((?![^)]*(?:grammar|format\s*=\s*['"]json['"]|schema))"""
)


def audit_local_llm_file(file_path: str) -> List[LocalLLMViolation]:
    """Audits a single file for local LLM inference and deployment hygiene."""
    violations: List[LocalLLMViolation] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return violations

    full_content = "".join(lines)
    ext = os.path.splitext(file_path)[1].lower()
    base_name = os.path.basename(file_path).lower()

    # Rule LLM-001: Degraded low-bit quantization (Q2/Q3)
    for idx, line in enumerate(lines, start=1):
        clean_line = line.strip()
        if clean_line.startswith(("#", "//", "/*")):
            continue

        if LOW_QUANT_PATTERN.search(clean_line):
            violations.append(
                LocalLLMViolation(
                    file_path=file_path,
                    line_number=idx,
                    rule_id="LLM-001",
                    message="Degraded quantization tier detected (Q2/Q3). Use Q4_K_M or Q5_K_M for production stability.",
                )
            )

        if LOCAL_HTTP_NO_TIMEOUT_PATTERN.search(clean_line):
            violations.append(
                LocalLLMViolation(
                    file_path=file_path,
                    line_number=idx,
                    rule_id="LLM-002",
                    message="Local inference HTTP call missing explicit timeout guardrails (3s connect / 15s body).",
                )
            )

        if LLAMA_SERVER_ZERO_GPU_PATTERN.search(clean_line):
            violations.append(
                LocalLLMViolation(
                    file_path=file_path,
                    line_number=idx,
                    rule_id="LLM-003",
                    message="llama-server launched with 0 GPU layers offloaded. Use -ngl 999 or metal acceleration.",
                    severity="WARNING",
                )
            )

    # Rule LLM-004: Unconstrained JSON prompt without GBNF grammar or schema
    if ext in [".py", ".ts", ".js"]:
        for idx, line in enumerate(lines, start=1):
            if JSON_PROMPT_WITHOUT_GRAMMAR_PATTERN.search(line):
                violations.append(
                    LocalLLMViolation(
                        file_path=file_path,
                        line_number=idx,
                        rule_id="LLM-004",
                        message="Local LLM JSON prompt lacks deterministic GBNF grammar or strict schema constraint.",
                        severity="WARNING",
                    )
                )

    return violations


def audit_local_llm_directory(target_dir: str) -> List[LocalLLMViolation]:
    """Audits all relevant files in target directory for local LLM hygiene."""
    violations: List[LocalLLMViolation] = []
    supported_extensions = {".py", ".ts", ".js", ".sh", ".yaml", ".yml", ".dockerfile"}

    for root, _, files in os.walk(target_dir):
        if any(ignored in root for ignored in [".git", "node_modules", "dist", "build"]):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions or "modelfile" in file.lower():
                full_path = os.path.join(root, file)
                violations.extend(audit_local_llm_file(full_path))

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit local LLM inference configurations, quantization, and grammar constraints."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to file or directory to audit (default: current directory).",
    )
    args = parser.parse_args()

    if os.path.isfile(args.path):
        violations = audit_local_llm_file(args.path)
    elif os.path.isdir(args.path):
        violations = audit_local_llm_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    if not violations:
        print("[PASS] All configurations adhere to Local LLM engineering and quantization standards.")
        return 0

    print(f"Local LLM Hygiene Audit: Found {len(violations)} violation(s):")
    for v in violations:
        print(f"[{v.severity}] {v.file_path}:{v.line_number} ({v.rule_id}) - {v.message}")

    errors = [v for v in violations if v.severity == "ERROR"]
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
