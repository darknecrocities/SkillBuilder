#!/usr/bin/env python3
"""
Unit tests for verify_git_delivery_etiquette.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Git Delivery Etiquette Framework
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_git_delivery_etiquette import audit_repository, validate_commit_message


class TestVerifyGitDeliveryEtiquette(unittest.TestCase):
    def test_valid_conventional_commit_with_body_passes(self):
        msg = """feat(qa): implement two-tier QA architecture and verification engine

- Context / Why: Resolves user request to split QA into Full UI and Full App domains.
- Key Changes / What:
  * Created full-ui-frontend-qa-manual.md (213 lines).
  * Implemented verify_app_functionality.py CLI tool.
- Verification / Impact: 28/28 test suites passed cleanly; all source files under 500 lines.
"""
        violations = validate_commit_message(msg)
        self.assertEqual(len(violations), 0, f"Expected 0 violations, got: {violations}")

    def test_detects_single_line_commit_missing_description(self):
        msg = "feat(auth): add login endpoint"
        violations = validate_commit_message(msg)
        self.assertTrue(any(v["rule"] == "MISSING-COMMIT-DESCRIPTION" for v in violations))

    def test_detects_non_conventional_title(self):
        msg = """added login endpoint and updated database models

- Context / Why: Needed for user authentication.
- Key Changes / What: Updated models and routes.
- Verification: Tested locally.
"""
        violations = validate_commit_message(msg)
        self.assertTrue(any(v["rule"] == "NON-CONVENTIONAL-TITLE" for v in violations))

    def test_detects_lazy_title(self):
        msg = """update: fix stuff

- Context / Why: Minor changes to the codebase.
- Key Changes / What: Updated files.
- Verification: Tested.
"""
        violations = validate_commit_message(msg)
        self.assertTrue(any(v["rule"] == "LAZY-COMMIT-TITLE" for v in violations))

    def test_detects_description_too_brief(self):
        msg = """feat(ui): add button component

too short
"""
        violations = validate_commit_message(msg)
        self.assertTrue(any(v["rule"] == "COMMIT-DESCRIPTION-TOO-BRIEF" for v in violations))

    def test_detects_empty_commit_message(self):
        violations = validate_commit_message("   ")
        self.assertTrue(any(v["rule"] == "EMPTY-COMMIT-MESSAGE" for v in violations))

    def test_detects_overlong_title(self):
        long_title = "feat(orchestration): " + "a" * 80 + "\n\n- Detailed description body goes here with enough context."
        violations = validate_commit_message(long_title)
        self.assertTrue(any(v["rule"] == "TITLE-TOO-LONG" for v in violations))

    def test_validates_simulated_git_log_payload(self):
        valid_log = """feat(git): add delivery etiquette verifier

- Context / Why: Enforce mandatory commit titles and description bodies.
- Key Changes / What:
  * Implemented verify_git_delivery_etiquette.py.
  * Added automated test suite.
- Verification / Impact: All tests pass cleanly.
"""
        violations = validate_commit_message(valid_log)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
