#!/usr/bin/env python3
"""
Unit tests for Antigravity Automation scripts:
- generate_sidecar_automation.py
- verify_antigravity_hooks.py
- schedule_in_turn_helper.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Antigravity Automation Engine
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from generate_sidecar_automation import (
    build_sidecar_payload,
    deploy_sidecar,
    list_existing_sidecars,
    validate_cron_expression,
    validate_timezone,
)
from schedule_in_turn_helper import (
    build_in_turn_cron,
    build_in_turn_timer,
)
from verify_antigravity_hooks import (
    audit_hooks_file,
)


class TestAntigravityAutomation(unittest.TestCase):
    def test_validate_cron_expression(self):
        valid, msg = validate_cron_expression("0 9 * * 1-5")
        self.assertTrue(valid)
        invalid, msg = validate_cron_expression("0 9 * *")
        self.assertFalse(invalid)

    def test_validate_timezone(self):
        valid, _ = validate_timezone("America/New_York")
        self.assertTrue(valid)
        valid_utc, _ = validate_timezone("UTC")
        self.assertTrue(valid_utc)
        invalid, _ = validate_timezone("PST")
        self.assertFalse(invalid)

    def test_build_and_deploy_sidecar(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            path, payload = deploy_sidecar(
                slug="daily-audit",
                cron_expr="0 8 * * *",
                timezone="Europe/London",
                prompt="Audit git commit logs and report anomalies.",
                output_dir=out_dir
            )
            self.assertTrue(path.exists())
            self.assertEqual(payload["builtin"], "schedule")
            self.assertEqual(payload["args"]["schedule"], "CRON_TZ=Europe/London 0 8 * * *")

            # Check listing
            found = list_existing_sidecars(out_dir)
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0]["slug"], "daily-audit")

    def test_schedule_in_turn_timer_and_cron(self):
        timer = build_in_turn_timer("Check build status", 30, "any")
        self.assertEqual(timer["DurationSeconds"], 30)
        self.assertEqual(timer["TimerCondition"], "any")

        cron = build_in_turn_cron("Poll queue", "*/10 * * * *", max_iterations=5, is_daemon=True)
        self.assertEqual(cron["CronExpression"], "*/10 * * * *")
        self.assertEqual(cron["MaxIterations"], 5)
        self.assertTrue(cron["IsDaemon"])

    def test_audit_hooks_file_valid_and_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            hooks_file = Path(td) / "hooks.json"
            script_file = Path(td) / "test_script.py"
            script_file.write_text("print('ok')\n", encoding="utf-8")

            valid_hooks = {
                "my-hook": {
                    "PreToolUse": [
                        {
                            "matcher": "run_command",
                            "hooks": [
                                {
                                    "command": "python3 test_script.py",
                                    "timeout": 5
                                }
                            ]
                        }
                    ]
                }
            }
            hooks_file.write_text(json.dumps(valid_hooks), encoding="utf-8")
            violations = audit_hooks_file(hooks_file, repo_root=Path(td))
            self.assertEqual(len(violations), 0, f"Expected 0 violations, got {violations}")

            # Test unknown event
            invalid_hooks = {
                "bad-hook": {
                    "NonExistentEvent": []
                }
            }
            hooks_file.write_text(json.dumps(invalid_hooks), encoding="utf-8")
            bad_violations = audit_hooks_file(hooks_file, repo_root=Path(td))
            self.assertTrue(any(v["rule"] == "UNKNOWN-EVENT-TYPE" for v in bad_violations))


if __name__ == "__main__":
    unittest.main()
