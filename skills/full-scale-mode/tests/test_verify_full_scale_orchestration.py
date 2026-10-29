#!/usr/bin/env python3
"""
Unit tests for verify_full_scale_orchestration.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_full_scale_orchestration import (
    REQUIRED_SKILLS,
    analyze_skill_resonance,
    audit_cross_skill_sync,
    audit_orchestration_memory,
    audit_phased_plan,
    audit_skill_registry,
    audit_subagent_prompt,
    estimate_tokens,
)


class TestVerifyFullScaleOrchestration(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent.parent.parent

    def test_repo_skill_registry_has_36_skills(self):
        self.assertEqual(len(REQUIRED_SKILLS), 36)
        violations = audit_skill_registry(self.repo_root)
        self.assertEqual(len(violations), 0, f"Expected clean registry, got: {violations}")

    def test_cross_skill_sync_is_clean(self):
        violations = audit_cross_skill_sync(self.repo_root)
        self.assertEqual(len(violations), 0, f"Expected 0 cross-skill sync drift, got: {violations}")

    def test_detects_missing_skill_in_temp_registry(self):
        violations = audit_skill_registry(Path(__file__).parent)
        self.assertTrue(any(v["rule"] in ["MISSING-SKILLS-DIRECTORY", "INCOMPLETE-SKILL-REGISTRY"] for v in violations))

    def test_autonomous_skill_resonance_detection(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "firebase.json").write_text("{}", encoding="utf-8")
            (p / "app").mkdir()
            (p / "app.json").write_text("{}", encoding="utf-8")
            (p / "tailwind.config.js").write_text("// tailwind", encoding="utf-8")
            (p / "Modelfile").write_text("FROM llama-3.2", encoding="utf-8")
            res = analyze_skill_resonance(p)
            self.assertIn("firebase", res["resonant_skills"])
            self.assertIn("routing", res["resonant_skills"])
            self.assertIn("frontend", res["resonant_skills"])
            self.assertIn("security", res["resonant_skills"])
            self.assertIn("mobile-ui", res["resonant_skills"])
            self.assertIn("web-ui", res["resonant_skills"])
            self.assertIn("local-llm", res["resonant_skills"])

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
        - Phase 1: Frontend & Interface Architecture
        - Phase 2: Backend, Cloud & Data Infrastructure
        - Phase 3: Testing, Quality Assurance & Verifiable Release
        """
        violations = audit_phased_plan(plan)
        self.assertEqual(len(violations), 0)

    def test_5stage_plan_passes(self):
        plan = """
        # 5-Stage Orchestration Lifecycle
        - Stage 1: Discover & Memory Recall
        - Stage 2: Plan & Blueprint
        - Stage 3: Build & Execution
        - Stage 4: Harness Evaluation
        - Stage 5: Release & Consolidate
        """
        violations = audit_phased_plan(plan)
        self.assertEqual(len(violations), 0)

    def test_incomplete_phased_plan_flags_missing_phases(self):
        plan = "# Plan\n- Phase 1: Plan\n- Phase 3: Build"
        violations = audit_phased_plan(plan)
        self.assertTrue(any(v["rule"] == "MISSING-PROJECT-PHASE" for v in violations))

    def test_audit_orchestration_memory_valid_and_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            mem_dir = p / ".agents" / "memory"
            mem_dir.mkdir(parents=True)
            mem_file = mem_dir / "orchestration_state.json"

            # Valid memory state
            valid_state = {
                "version": "1.0.0",
                "session_id": "test-sess",
                "current_stage": "BUILD",
                "triad_phase": "PHASE_2_BACKEND",
                "milestones": [],
                "file_registry": {"created": [], "modified": []}
            }
            mem_file.write_text(json.dumps(valid_state), encoding="utf-8")
            self.assertEqual(len(audit_orchestration_memory(p)), 0)

            # Invalid stage
            valid_state["current_stage"] = "UNKNOWN_STAGE"
            mem_file.write_text(json.dumps(valid_state), encoding="utf-8")
            violations = audit_orchestration_memory(p)
            self.assertTrue(any(v["rule"] == "INVALID-ORCHESTRATION-STAGE" for v in violations))

            # Corrupt JSON
            mem_file.write_text("{ corrupt json", encoding="utf-8")
            violations = audit_orchestration_memory(p)
            self.assertTrue(any(v["rule"] == "CORRUPT-ORCHESTRATION-MEMORY" for v in violations))

    def test_estimate_tokens_calculation(self):
        self.assertEqual(estimate_tokens(""), 0)
        sample = "a" * 38
        self.assertEqual(estimate_tokens(sample), 10)

    def test_platform_domain_specialization_mobile_only(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "pubspec.yaml").write_text("name: mobile_app", encoding="utf-8")
            res = analyze_skill_resonance(p)
            self.assertEqual(res["platform_target"], "mobile")
            self.assertIn("mobile-ui", res["resonant_skills"])
            self.assertIn("web-ui", res["pruned_skills"])
            self.assertGreaterEqual(res["token_quota_saved"], 1850)

    def test_platform_domain_specialization_web_only(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "next.config.js").write_text("// next config", encoding="utf-8")
            (p / "tailwind.config.js").write_text("// tailwind", encoding="utf-8")
            res = analyze_skill_resonance(p)
            self.assertEqual(res["platform_target"], "web")
            self.assertIn("web-ui", res["resonant_skills"])
            self.assertIn("mobile-ui", res["pruned_skills"])
            self.assertGreaterEqual(res["token_quota_saved"], 1850)

    def test_platform_override_pruning(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "app.json").write_text("{}", encoding="utf-8")
            (p / "tailwind.config.js").write_text("{}", encoding="utf-8")
            res_mobile = analyze_skill_resonance(p, target_platform="mobile")
            self.assertIn("mobile-ui", res_mobile["resonant_skills"])
            self.assertIn("web-ui", res_mobile["pruned_skills"])
            res_web = analyze_skill_resonance(p, target_platform="web")
            self.assertIn("web-ui", res_web["resonant_skills"])
            self.assertIn("mobile-ui", res_web["pruned_skills"])


if __name__ == "__main__":
    unittest.main()
