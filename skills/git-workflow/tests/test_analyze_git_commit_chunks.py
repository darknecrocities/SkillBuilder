#!/usr/bin/env python3
"""
Unit tests for analyze_git_commit_chunks.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from analyze_git_commit_chunks import classify_file, partition_commit_chunks


class TestAnalyzeGitCommitChunks(unittest.TestCase):
    def test_classify_files(self):
        self.assertEqual(classify_file("src/db/migrations/001_init.sql"), "db")
        self.assertEqual(classify_file("src/services/billing.py"), "service")
        self.assertEqual(classify_file("src/controllers/auth.ts"), "api")
        self.assertEqual(classify_file("src/components/Header.tsx"), "ui")
        self.assertEqual(classify_file("tests/unit/test_auth.py"), "test")
        self.assertEqual(classify_file("Dockerfile"), "infra")
        self.assertEqual(classify_file("README.md"), "core")

    def test_partition_commit_chunks_within_budget(self):
        files = [
            {"path": "src/services/a.py", "total": 200},
            {"path": "src/services/b.py", "total": 300},
        ]
        chunks = partition_commit_chunks(files, budget=1000)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["total_lines"], 500)

    def test_partition_commit_chunks_exceeds_budget(self):
        files = [
            {"path": "src/services/a.py", "total": 700},
            {"path": "src/services/b.py", "total": 600},
        ]
        chunks = partition_commit_chunks(files, budget=1000)
        self.assertEqual(len(chunks), 2)


if __name__ == "__main__":
    unittest.main()
