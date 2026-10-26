#!/usr/bin/env python3
"""
Unit tests for verify_state_hygiene.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_state_hygiene import audit_state_file, scan_state_workspace


class TestVerifyStateHygiene(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_file(self, rel_path: str, content: str) -> str:
        fp = os.path.join(self.temp_dir.name, rel_path)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return fp

    def test_clean_state_passes(self):
        content = """
        const count = useCounterStore(state => state.count);
        const { data } = useQuery({ queryKey: ['todos', id], queryFn: fetchTodo });
        """
        fp = self._write_file("component.tsx", content)
        violations = audit_state_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_unmemoized_store_subscription(self):
        content = 'const store = useWorkspaceStore();'
        fp = self._write_file("sidebar.tsx", content)
        violations = audit_state_file(fp)
        self.assertTrue(any(v["rule"] == "STATE-UNMEMOIZED-STORE-SUBSCRIPTION" for v in violations))

    def test_detects_raw_string_query_key(self):
        content = 'const { data } = useQuery("todos", fetchTodos);'
        fp = self._write_file("todos.tsx", content)
        violations = audit_state_file(fp)
        self.assertTrue(any(v["rule"] == "STATE-RAW-STRING-QUERY-KEY" for v in violations))

    def test_detects_boolean_explosion(self):
        content = """
        const [isLoading, setIsLoading] = useState(false);
        const [isError, setIsError] = useState(false);
        const [isSuccess, setIsSuccess] = useState(false);
        """
        fp = self._write_file("profile.tsx", content)
        violations = audit_state_file(fp)
        self.assertTrue(any(v["rule"] == "STATE-BOOLEAN-EXPLOSION" for v in violations))


if __name__ == "__main__":
    unittest.main()
