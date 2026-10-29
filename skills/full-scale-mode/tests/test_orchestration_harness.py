#!/usr/bin/env python3
"""
Unit tests for orchestration_harness.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from orchestration_harness import (
    check_tier1_hygiene,
    check_tier2_contracts,
    check_tier4_security,
    check_tier5_git,
    execute_self_healing_loop,
    run_harness_suite,
)


class TestOrchestrationHarness(unittest.TestCase):
    def test_tier1_hygiene_clean_directory(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "clean.py").write_text("def hello():\n    return 'clean'\n", encoding="utf-8")
            violations = check_tier1_hygiene(p)
            self.assertEqual(len(violations), 0)

    def test_tier1_hygiene_flags_line_limit_exceeded(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            lines = ["# line\n"] * 520
            (p / "bloated.py").write_text("".join(lines), encoding="utf-8")
            violations = check_tier1_hygiene(p)
            self.assertTrue(any(v["rule"] == "SOURCE-LINE-LIMIT-EXCEEDED" for v in violations))

    def test_tier1_hygiene_flags_ai_slop(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "slop.ts").write_text("const url = 'https://img.shields.io/badge/test';\n", encoding="utf-8")
            violations = check_tier1_hygiene(p)
            self.assertTrue(any(v["rule"] == "AI-SLOP-DETECTED" for v in violations))

    def test_tier2_contracts_flags_syntax_error(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            skills_dir = p / "skills" / "my-skill"
            skills_dir.mkdir(parents=True)
            (skills_dir / "broken.py").write_text("def syntax_error(\n", encoding="utf-8")
            violations = check_tier2_contracts(p)
            self.assertTrue(any(v["rule"] == "SYNTAX-ERROR" for v in violations))

    def test_tier4_security_flags_hardcoded_secret(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "config.py").write_text("api_key = 'abcdef1234567890abcdef123456'\n", encoding="utf-8")
            violations = check_tier4_security(p)
            self.assertTrue(any(v["rule"] == "SECRET-LEAK-RISK" for v in violations))

    def test_run_harness_suite_aggregates_tier_results(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "main.py").write_text("print('test')\n", encoding="utf-8")
            res = run_harness_suite(p, active_tiers=[1, 2, 4])
            self.assertTrue(res["passed"])
            self.assertIn("tier_1", res["tier_results"])
            self.assertIn("tier_2", res["tier_results"])
            self.assertIn("tier_4", res["tier_results"])

    def test_execute_self_healing_loop_converges_with_remediation(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            test_file = p / "slop_file.py"
            test_file.write_text("const b = 'img.shields.io';\n", encoding="utf-8")

            def remedy(violations, iteration):
                if iteration == 1:
                    test_file.write_text("const clean = true;\n", encoding="utf-8")
                    return True
                return False

            loop_res = execute_self_healing_loop(
                p, max_iterations=3, active_tiers=[1], remediation_callback=remedy
            )
            self.assertTrue(loop_res["converged"])
            self.assertEqual(loop_res["iterations_used"], 2)

    def test_execute_self_healing_loop_halts_at_max_iterations(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "bad.py").write_text("const b = 'img.shields.io';\n", encoding="utf-8")

            loop_res = execute_self_healing_loop(p, max_iterations=2, active_tiers=[1])
            self.assertFalse(loop_res["converged"])
            self.assertEqual(loop_res["iterations_used"], 1)


if __name__ == "__main__":
    unittest.main()
