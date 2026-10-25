import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from lookup_error import load_error_catalog, search_errors


class TestLookupError(unittest.TestCase):
    def setUp(self):
        self.entries = load_error_catalog()

    def test_catalog_loads_entries(self):
        self.assertGreater(len(self.entries), 0, "Error catalog should load at least one entry.")

    def test_search_by_keyword(self):
        matches = search_errors(self.entries, "deadlock")
        self.assertGreater(len(matches), 0)
        self.assertIn("ERR-DB-001", matches[0]["id"])
        self.assertEqual(matches[0]["category"], "Database")

    def test_search_by_category_filter(self):
        matches = search_errors(self.entries, "hydration", category="Frontend")
        self.assertEqual(len(matches), 1)
        self.assertIn("ERR-FE-001", matches[0]["id"])

    def test_no_match(self):
        matches = search_errors(self.entries, "xyznonexistenterror123456")
        self.assertEqual(len(matches), 0)


if __name__ == "__main__":
    unittest.main()
