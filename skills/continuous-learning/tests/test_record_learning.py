#!/usr/bin/env python3
"""
Unit tests for record_learning.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from record_learning import load_conventions, save_convention


class TestRecordLearning(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.conv_file = os.path.join(self.temp_dir.name, "learned_conventions.md")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_convention(self):
        msg = save_convention("UI", "Use Lucide icons instead of emojis", self.conv_file)
        self.assertIn("UI-001", msg)

        conventions = load_conventions(self.conv_file)
        self.assertEqual(len(conventions), 1)
        self.assertEqual(conventions[0]["id"], "UI-001")
        self.assertEqual(conventions[0]["text"], "Use Lucide icons instead of emojis")

    def test_deduplicates_identical_text(self):
        save_convention("ARCH", "Prefer SQLite for embedded apps", self.conv_file)
        msg2 = save_convention("ARCH", "Prefer SQLite for embedded apps", self.conv_file)
        self.assertIn("Duplicate", msg2)

        conventions = load_conventions(self.conv_file)
        self.assertEqual(len(conventions), 1)


if __name__ == "__main__":
    unittest.main()
