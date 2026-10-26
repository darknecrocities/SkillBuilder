#!/usr/bin/env python3
"""Unit tests for verify_local_llm_hygiene script."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_local_llm_hygiene import (
    audit_local_llm_file,
    LocalLLMViolation,
)


class TestVerifyLocalLLMHygiene(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    def _create_file(self, filename: str, content: str) -> str:
        path = os.path.join(self.test_dir.name, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_detects_low_quantization_tier(self):
        modelfile = """
        FROM llama-3.2-3b-instruct-q2_k.gguf
        PARAMETER temperature 0.2
        """
        path = self._create_file("Modelfile", modelfile)
        violations = audit_local_llm_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("LLM-001", rule_ids)

    def test_detects_local_http_no_timeout(self):
        code = """
        import requests

        def query_ollama(prompt):
            res = requests.post("http://localhost:11434/api/generate", json={"prompt": prompt})
            return res.json()
        """
        path = self._create_file("client.py", code)
        violations = audit_local_llm_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("LLM-002", rule_ids)

    def test_warns_on_zero_gpu_layers(self):
        script = """
        #!/usr/bin/env bash
        ./llama-server -m models/llama-3.2-3b.gguf -ngl 0 --port 8080
        """
        path = self._create_file("launch.sh", script)
        violations = audit_local_llm_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("LLM-003", rule_ids)

    def test_passes_compliant_local_llm_setup(self):
        code = """
        import requests

        def query_local_model(prompt: str, grammar: str) -> dict:
            res = requests.post(
                "http://localhost:8080/completion",
                json={"prompt": prompt, "grammar": grammar},
                timeout=(3.0, 15.0)
            )
            return res.json()
        """
        path = self._create_file("compliant_client.py", code)
        violations = audit_local_llm_file(path)
        errors = [v for v in violations if v.severity == "ERROR"]
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
