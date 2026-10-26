#!/usr/bin/env python3
"""
Unit tests for verify_pipeline_integrity.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_pipeline_integrity import audit_pipeline_file, scan_pipeline_workspace


class TestVerifyPipelineIntegrity(unittest.TestCase):
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

    def test_clean_chunked_pipeline_passes(self):
        content = """
        import pandas as pd
        for chunk in pd.read_csv("events.csv", chunksize=5000):
            process_chunk(chunk)
        """
        fp = self._write_file("pipeline.py", content)
        violations = audit_pipeline_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_unbounded_read_csv(self):
        content = """
        import pandas as pd
        df = pd.read_csv("huge_dataset.csv")
        """
        fp = self._write_file("bad_pipeline.py", content)
        violations = audit_pipeline_file(fp)
        self.assertTrue(any(v["rule"] == "PIPELINE-UNBOUNDED-READ" for v in violations))

    def test_detects_silent_discard_in_batch(self):
        content = """
        def run_batch():
            for item in batch:
                try:
                    save_item(item)
                except Exception:
                    continue
        """
        fp = self._write_file("batch_worker.py", content)
        violations = audit_pipeline_file(fp)
        self.assertTrue(any(v["rule"] == "PIPELINE-MISSING-DEAD-LETTER-QUEUE" for v in violations))


if __name__ == "__main__":
    unittest.main()
