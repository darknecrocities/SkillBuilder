#!/usr/bin/env python3
"""Unit tests for the DarkNecroStack dynamic router, decision trail, and core files."""

import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import log_decision_trail  # noqa: E402
import route_task  # noqa: E402


class TestDarkNecroStack(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parent.parent.parent.parent

    def test_worker_and_skill_exist(self) -> None:
        skill_dir = self.repo_root / "skills" / "darknecrostack"
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertTrue((skill_dir / "worker.md").exists())
        self.assertGreaterEqual(len(list((skill_dir / "principles").glob("*.md"))), 6)
        self.assertGreaterEqual(len(list((skill_dir / "playbooks").glob("*.md"))), 18)

    def test_route_web_mascot_prunes_mobile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "package.json").write_text('{"name":"demo"}', encoding="utf-8")
            decision = route_task.route_prompt("Build a Rive .riv mascot and logo in Next.js", tmp_path)
            self.assertEqual(decision["playbook"], "skills/darknecrostack/playbooks/visual-parity.md")
            self.assertIn("2d-mascot-motion", decision["active_skills"])
            self.assertIn("brand-assets", decision["active_skills"])
            self.assertIn("web-ui", decision["active_skills"])
            self.assertIn("mobile-ui", decision["pruned_skills"])
            self.assertGreaterEqual(decision["estimated_tokens_saved"], 1850)

    def test_route_bug_fix_mounts_archaeology(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            decision = route_task.route_prompt("Fix regression crash on login endpoint", Path(tmp))
            self.assertEqual(decision["playbook"], "skills/darknecrostack/playbooks/bug-fix.md")
            self.assertIn("code-archaeology", decision["active_skills"])
            self.assertIn("prove-it-works", decision["active_skills"])

    def test_decision_trail_tsv_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            trail = Path(tmp) / "decision_trail.tsv"
            log_decision_trail.append_trail_entry(
                trail,
                step="iter-1",
                hypothesis="Tab\tbreak",
                action="Run\npytest",
                result="PASS",
                evidence="10/10 passed",
            )
            rows = log_decision_trail.read_trail(trail)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0], log_decision_trail.HEADER)
            self.assertEqual(rows[1][1], "iter-1")
            self.assertEqual(rows[1][2], "Tab break")
            self.assertEqual(rows[1][3], "Run pytest")
            self.assertEqual(rows[1][4], "PASS")


if __name__ == "__main__":
    unittest.main()
