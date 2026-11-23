#!/usr/bin/env python3
"""A/B Testing Hygiene Auditor & Statistical Significance Verifier.

Audits code for non-deterministic random() experiment bucketing, missing
experiment attribution on exposure tracking, and missing guardrails; also
computes exact Sample Ratio Mismatch (SRM) chi-squared and two-proportion
z-test significance directly from CLI counts.
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ABViolation:
    file_path: str
    line_number: int
    rule_id: str
    message: str
    severity: str = "ERROR"


EXP_CONTEXT_PAT = re.compile(r"(?:experiment|ab_test|abtest|variant|feature_flag|bucket)", re.IGNORECASE)
RANDOM_BUCKET_PAT = re.compile(r"\b(?:Math\.random|random\.random|random\.choice|np\.random\.rand)\s*\(")
EXPOSURE_PAT = re.compile(r"\b(?:track_exposure|logExposure|trackExperiment)\s*\(([^)]*)\)")


def check_srm(control_n: int, treatment_n: int, expected_treatment_ratio: float = 0.5) -> Dict[str, object]:
    """Compute exact 1-df Pearson chi-squared Sample Ratio Mismatch (SRM) test."""
    total = control_n + treatment_n
    if total <= 0 or not (0.0 < expected_treatment_ratio < 1.0):
        raise ValueError("Counts must be positive and ratio in (0, 1).")
    exp_treat = total * expected_treatment_ratio
    exp_ctrl = total * (1.0 - expected_treatment_ratio)
    chi2 = ((control_n - exp_ctrl) ** 2) / exp_ctrl + ((treatment_n - exp_treat) ** 2) / exp_treat
    # For df=1, chi2 = Z^2, so p = erfc(sqrt(chi2 / 2))
    p_value = math.erfc(math.sqrt(chi2 / 2.0))
    return {
        "total_n": total,
        "chi2": round(chi2, 4),
        "p_value": round(p_value, 6),
        "srm_detected": p_value < 0.001,
        "status": "SRM_HALT" if p_value < 0.001 else "PASS",
    }


def check_two_proportion_ztest(
    control_n: int,
    control_conv: int,
    treatment_n: int,
    treatment_conv: int,
    alpha: float = 0.05,
) -> Dict[str, object]:
    """Compute two-proportion z-test, relative lift, and two-sided p-value."""
    if control_n <= 0 or treatment_n <= 0:
        raise ValueError("Sample sizes must be > 0.")
    if not (0 <= control_conv <= control_n and 0 <= treatment_conv <= treatment_n):
        raise ValueError("Conversions cannot exceed sample sizes.")

    p1 = control_conv / control_n
    p2 = treatment_conv / treatment_n
    pooled = (control_conv + treatment_conv) / (control_n + treatment_n)
    se = math.sqrt(pooled * (1.0 - pooled) * (1.0 / control_n + 1.0 / treatment_n))
    z_score = (p2 - p1) / se if se > 0 else 0.0
    p_value = math.erfc(abs(z_score) / math.sqrt(2.0))
    rel_lift = ((p2 - p1) / p1 * 100.0) if p1 > 0 else 0.0
    return {
        "control_rate": round(p1, 5),
        "treatment_rate": round(p2, 5),
        "abs_diff": round(p2 - p1, 5),
        "rel_lift_pct": round(rel_lift, 2),
        "z_score": round(z_score, 4),
        "p_value": round(p_value, 6),
        "significant": p_value < alpha,
    }


def audit_ab_file(file_path: str) -> List[ABViolation]:
    """Audit Python or TypeScript experiment/flag code for A/B hygiene defects."""
    violations: List[ABViolation] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return violations

    if not EXP_CONTEXT_PAT.search(content):
        return violations

    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith(("#", "//")):
            continue
        if RANDOM_BUCKET_PAT.search(line):
            violations.append(ABViolation(
                file_path, idx, "AB-001",
                "Non-deterministic random() used in experiment/variant code; use SHA-256/MurmurHash3 bucketing.",
            ))
        exp_match = EXPOSURE_PAT.search(line)
        if exp_match and "experiment" not in exp_match.group(1).lower():
            violations.append(ABViolation(
                file_path, idx, "AB-002",
                "Exposure logger call missing explicit experiment_id attribution.",
                severity="WARNING",
            ))

    if any(k in content for k in ("experiment_id", "EXPERIMENT_ID")) and "guardrail" not in content.lower():
        violations.append(ABViolation(
            file_path, 1, "AB-003",
            "Experiment definition lacks explicit guardrail metrics (latency/error-rate ceilings).",
            severity="WARNING",
        ))

    return violations


def audit_ab_directory(target_dir: str) -> List[ABViolation]:
    """Audit experiment files under target_dir."""
    violations: List[ABViolation] = []
    ignored = {".git", "node_modules", "dist", "build", "__pycache__", "venv"}
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignored]
        for fname in files:
            if fname.endswith((".py", ".ts", ".tsx", ".js")) and "verify_ab_experiment" not in fname and "test_verify_ab_experiment" not in fname:
                violations.extend(audit_ab_file(os.path.join(root, fname)))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit A/B experiment code and compute SRM / z-test significance.")
    parser.add_argument("--path", help="File or directory to audit for A/B bucketing hygiene")
    parser.add_argument("--srm", nargs=2, type=int, metavar=("CTRL_N", "TREAT_N"), help="Check 50/50 Sample Ratio Mismatch")
    parser.add_argument("--ratio", type=float, default=0.5, help="Expected treatment ratio for --srm (default: 0.5)")
    parser.add_argument("--ztest", nargs=4, type=int, metavar=("CTRL_N", "CTRL_CONV", "TREAT_N", "TREAT_CONV"), help="Run two-proportion z-test")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on errors or SRM failure")
    args = parser.parse_args()

    exit_code = 0
    if args.srm:
        res = check_srm(args.srm[0], args.srm[1], args.ratio)
        print(f"[SRM] total={res['total_n']} chi2={res['chi2']} p={res['p_value']} -> {res['status']}")
        if res["srm_detected"] and args.strict:
            exit_code = 1

    if args.ztest:
        res = check_two_proportion_ztest(args.ztest[0], args.ztest[1], args.ztest[2], args.ztest[3])
        verdict = "SIGNIFICANT" if res["significant"] else "INCONCLUSIVE"
        print(f"[Z-TEST] ctrl={res['control_rate']} treat={res['treatment_rate']} lift={res['rel_lift_pct']}% z={res['z_score']} p={res['p_value']} -> {verdict}")

    if args.path or (not args.srm and not args.ztest):
        target = args.path or "."
        violations = audit_ab_file(target) if os.path.isfile(target) else audit_ab_directory(target)
        if not violations:
            print("[PASS] A/B testing & experimentation hygiene verified.")
        else:
            for v in violations:
                print(f"[{v.severity}] {v.file_path}:{v.line_number} [{v.rule_id}] {v.message}")
            if any(v.severity == "ERROR" for v in violations):
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
