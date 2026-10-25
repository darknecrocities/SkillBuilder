#!/usr/bin/env python3
"""
Unit tests for verify_full_scale_orchestration.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_full_scale_orchestration import (
    audit_phased_plan,
    audit_skill_registry,
    audit_subagent_prompt,
    estimate_tokens,
)


class TestVerifyFullScaleOrchestration(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent.parent.parent

    def test_repo_skill_registry_is_complete(self):
        violations = audit_skill_registry(self.repo_root)
        self.assertEqual(len(violations), 0, f"Expected clean registry, got: {violations}")

    def test_detects_missing_skill_in_temp_registry(self):
        # Point to a directory without all skills
        violations = audit_skill_registry(Path(__file__).parent)
        self.assertTrue(any(v["rule"] in ["MISSING-SKILLS-DIRECTORY", "INCOMPLETE-SKILL-REGISTRY"] for v in violations))

    def test_clean_subagent_prompt_passes(self):
        prompt = (
            "Role: UI/UX Specialist. "
            "Implement src/components/TactileButton.tsx using Apple HIG tokens, "
            "Cupertino blur materials, and 44x44pt touch targets. "
            "Return compact SubagentHandoffPayload JSON."
        )
        violations = audit_subagent_prompt(prompt, budget_limit=1500)
        self.assertEqual(len(violations), 0)

    def test_detects_token_budget_exceeded(self):
        # 1600 tokens approx 6000 chars
        long_prompt = "x " * 3500
        violations = audit_subagent_prompt(long_prompt, budget_limit=1500)
        self.assertTrue(any(v["rule"] == "SUBAGENT-TOKEN-BUDGET-EXCEEDED" for v in violations))

    def test_detects_conversational_filler(self):
        prompt = "Hello subagent, could you please help me build the auth service?"
        violations = audit_subagent_prompt(prompt)
        self.assertTrue(any(v["rule"] == "CONVERSATIONAL-TOKEN-BLOAT" for v in violations))

    def test_complete_phased_plan_passes(self):
        plan = """
        # Project Plan
        - Phase 0: Ingestion and Prompt Polish
        - Phase 1: Architectural Technical Plan
        - Phase 2: Autonomous Deep Research
        - Phase 3: Parallel Domain Execution
        - Phase 4: Security and DevOps
        - Phase 5: Two-Tier QA
        - Phase 6: Continuous Learning and Delivery
        """
        violations = audit_phased_plan(plan)
        self.assertEqual(len(violations), 0)

    def test_incomplete_phased_plan_flags_missing_phases(self):
        plan = "# Plan\n- Phase 1: Plan\n- Phase 3: Build"
        violations = audit_phased_plan(plan)
        self.assertTrue(any(v["rule"] == "MISSING-PROJECT-PHASE" for v in violations))

    def test_estimate_tokens_calculation(self):
        self.assertEqual(estimate_tokens(""), 0)
        # 38 chars / 3.8 = 10 tokens
        sample = "a" * 38
        self.assertEqual(estimate_tokens(sample), 10)


if __name__ == "__main__":
    unittest.main()
