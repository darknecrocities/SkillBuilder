#!/usr/bin/env python3
"""
Unit tests for manage_orchestration_memory.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from manage_orchestration_memory import (
    advance_stage_transition,
    create_initial_state,
    format_status_summary,
    init_memory,
    load_memory,
    record_harness_iteration,
    record_milestone_completion,
    save_memory,
    update_checkpoint,
)


class TestManageOrchestrationMemory(unittest.TestCase):
    def test_create_initial_state_has_standard_fields(self):
        state = create_initial_state("sess-42", goal="Test goal", platform="web")
        self.assertEqual(state["session_id"], "sess-42")
        self.assertEqual(state["current_stage"], "DISCOVER")
        self.assertEqual(state["triad_phase"], "PHASE_1_FRONTEND")
        self.assertEqual(state["platform_target"], "web")
        self.assertEqual(len(state["milestones"]), 5)
        self.assertEqual(state["file_registry"], {"created": [], "modified": []})
        self.assertEqual(state["harness_history"], [])

    def test_checkpoint_updates_stage_and_files(self):
        state = create_initial_state("sess-1")
        updated = update_checkpoint(
            state, stage="PLAN", triad_phase="PHASE_2_BACKEND",
            created_file="src/models/user.ts", modified_file="package.json", token_delta=500
        )
        self.assertEqual(updated["current_stage"], "PLAN")
        self.assertEqual(updated["triad_phase"], "PHASE_2_BACKEND")
        self.assertIn("src/models/user.ts", updated["file_registry"]["created"])
        self.assertIn("package.json", updated["file_registry"]["modified"])
        self.assertEqual(updated["token_usage_estimate"], 500)

    def test_checkpoint_rejects_invalid_stage_and_phase(self):
        state = create_initial_state("sess-1")
        with self.assertRaises(ValueError):
            update_checkpoint(state, stage="INVALID_STAGE")
        with self.assertRaises(ValueError):
            update_checkpoint(state, triad_phase="INVALID_PHASE")

    def test_milestone_completion_tracking(self):
        state = create_initial_state("sess-1")
        record_milestone_completion(state, "M-DISCOVER", status="COMPLETED")
        m_disc = next(m for m in state["milestones"] if m["id"] == "M-DISCOVER")
        self.assertEqual(m_disc["status"], "COMPLETED")
        self.assertIsNotNone(m_disc["completed_at"])

        # Custom milestone addition
        record_milestone_completion(state, "M-CUSTOM-1", status="IN_PROGRESS")
        m_cust = next(m for m in state["milestones"] if m["id"] == "M-CUSTOM-1")
        self.assertEqual(m_cust["status"], "IN_PROGRESS")

    def test_advance_stage_order_and_loop_recovery(self):
        state = create_initial_state("sess-1")
        self.assertEqual(state["current_stage"], "DISCOVER")
        self.assertEqual(advance_stage_transition(state), "PLAN")
        self.assertEqual(advance_stage_transition(state), "BUILD")
        self.assertEqual(advance_stage_transition(state), "VERIFY")
        self.assertEqual(advance_stage_transition(state), "RELEASE")

        # When in LOOP stage, advance transitions back to VERIFY for re-evaluation
        state["current_stage"] = "LOOP"
        self.assertEqual(advance_stage_transition(state), "VERIFY")

    def test_record_harness_history(self):
        state = create_initial_state("sess-1")
        record_harness_iteration(state, iteration=1, passed=False, failing_tiers=["TIER-1-HYGIENE"], failure_count=2)
        self.assertEqual(len(state["harness_history"]), 1)
        self.assertEqual(state["harness_history"][0]["iteration"], 1)
        self.assertFalse(state["harness_history"][0]["passed"])
        self.assertEqual(state["harness_history"][0]["failure_count"], 2)

    def test_disk_persistence_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            mem_path = Path(td) / "state.json"
            init_memory(mem_path, session_id="test-disk", goal="Persist me", platform="universal")
            self.assertTrue(mem_path.exists())

            loaded = load_memory(mem_path)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["session_id"], "test-disk")

            update_checkpoint(loaded, stage="BUILD")
            save_memory(mem_path, loaded)

            reloaded = load_memory(mem_path)
            self.assertEqual(reloaded["current_stage"], "BUILD")

    def test_status_summary_output(self):
        state = create_initial_state("test-summary", goal="Check summary", platform="mobile")
        summary = format_status_summary(state, Path("orchestration_state.json"))
        self.assertIn("=== Orchestration Memory State (orchestration_state.json) ===", summary)
        self.assertIn("Session ID     : test-summary", summary)
        self.assertIn("Platform Target: [MOBILE]", summary)
        self.assertIn("Stage 1: Discover & Memory Recall", summary)


if __name__ == "__main__":
    unittest.main()
