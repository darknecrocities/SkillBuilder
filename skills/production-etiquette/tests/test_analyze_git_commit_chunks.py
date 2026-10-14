#!/usr/bin/env python3
"""
Unit tests for analyze_git_commit_chunks.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_git_commit_chunks import (
    categorize_file,
    cluster_chunks,
    generate_pr_payload,
    get_diff_stats,
    MAX_PUSH_LINE_BUDGET,
)


class TestGitCommitChunkAnalyzer(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.script_path = SCRIPT_DIR / "analyze_git_commit_chunks.py"

    def tearDown(self) -> None:
        self.temp_dir_obj.cleanup()

    def test_categorize_file(self) -> None:
        self.assertEqual(categorize_file("db/migrations/001_init.sql"), "db")
        self.assertEqual(categorize_file("src/models/user_entity.ts"), "db")
        self.assertEqual(categorize_file("src/services/billing_service.ts"), "service")
        self.assertEqual(categorize_file("src/repositories/user_repo.py"), "service")
        self.assertEqual(categorize_file("src/routes/api_controller.ts"), "api")
        self.assertEqual(categorize_file("src/components/Button.tsx"), "ui")
        self.assertEqual(categorize_file("tests/unit/auth.test.ts"), "test")
        self.assertEqual(categorize_file("Dockerfile"), "infra")
        self.assertEqual(categorize_file("misc_notes.txt"), "misc")

    def test_cluster_chunks(self) -> None:
        files = [
            {"file": "src/models/user.ts", "added": 50, "deleted": 0, "total_diff": 50},
            {"file": "src/services/user_service.ts", "added": 120, "deleted": 10, "total_diff": 130},
            {"file": "tests/unit/user.test.ts", "added": 80, "deleted": 0, "total_diff": 80},
        ]
        clusters = cluster_chunks(files)
        self.assertIn("db", clusters)
        self.assertIn("service", clusters)
        self.assertIn("test", clusters)
        self.assertEqual(len(clusters["db"]), 1)
        self.assertEqual(len(clusters["service"]), 1)
        self.assertEqual(len(clusters["test"]), 1)

    def test_generate_pr_payload(self) -> None:
        files = [
            {"file": "src/services/auth.ts", "added": 40, "deleted": 5, "total_diff": 45}
        ]
        payload = generate_pr_payload("feat/auth-jwt-refresh", files, 45)
        self.assertIn("feat(auth):", payload["title"])
        self.assertIn("## 1. Summary & Objective", payload["body"])
        self.assertIn("## 4. Verification Evidence", payload["body"])
        self.assertIn("src/services/auth.ts", payload["body"])

    def test_git_diff_in_real_repo(self) -> None:
        # Initialize a temporary git repository
        subprocess.run(["git", "init"], cwd=self.temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.temp_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.temp_dir, check=True)

        # Create initial commit
        initial_file = self.temp_dir / "README.md"
        initial_file.write_text("# Initial", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.temp_dir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.temp_dir, check=True, capture_output=True)

        # Make modifications
        new_source = self.temp_dir / "service.py"
        new_source.write_text("\n".join(f"print({i})" for i in range(25)), encoding="utf-8")

        stats = get_diff_stats(self.temp_dir)
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]["file"], "service.py")
        self.assertEqual(stats[0]["total_diff"], 25)

    def test_cli_execution_clean(self) -> None:
        subprocess.run(["git", "init"], cwd=self.temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.temp_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.temp_dir, check=True)

        file1 = self.temp_dir / "main.py"
        file1.write_text("print('hello')\n", encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertFalse(data["exceeds_budget"])
        self.assertEqual(data["file_count"], 1)


if __name__ == "__main__":
    unittest.main()
