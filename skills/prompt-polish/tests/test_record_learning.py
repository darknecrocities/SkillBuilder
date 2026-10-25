import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from record_learning import record_convention, load_conventions


class TestRecordLearning(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.conventions_file = os.path.join(self.test_dir, "learned_conventions.md")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_record_single_convention(self):
        entry = record_convention(
            "Use named exports for all React components.",
            category="ARCH",
            filepath=self.conventions_file,
        )
        self.assertEqual(entry["id"], "ARCH-001")
        self.assertEqual(entry["category"], "ARCH")

        conventions = load_conventions(self.conventions_file)
        self.assertEqual(len(conventions), 1)
        self.assertEqual(conventions[0]["rule"], "Use named exports for all React components.")

    def test_record_multiple_categories(self):
        record_convention("Rule 1", category="UI", filepath=self.conventions_file)
        record_convention("Rule 2", category="UI", filepath=self.conventions_file)
        entry3 = record_convention("Rule 3", category="STYLE", filepath=self.conventions_file)

        self.assertEqual(entry3["id"], "STYLE-001")
        conventions = load_conventions(self.conventions_file)
        self.assertEqual(len(conventions), 3)


if __name__ == "__main__":
    unittest.main()
