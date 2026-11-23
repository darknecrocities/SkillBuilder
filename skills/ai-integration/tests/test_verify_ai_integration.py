#!/usr/bin/env python3
"""Unit tests for verify_ai_integration.py."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_ai_integration import audit_integration_file


class TestVerifyAIIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, name: str, content: str) -> str:
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_flags_silent_cloud_fallback_and_hardcoded_url(self) -> None:
        code = (
            "import requests\n"
            "def run(prompt):\n"
            "    try:\n"
            "        return requests.post('http://127.0.0.1:11434/v1/chat', timeout=(3, 15))\n"
            "    except TimeoutError:\n"
            "        return call_gemini(prompt)\n"
        )
        violations = audit_integration_file(self._write("bad_gw.py", code))
        rules = {v.rule_id for v in violations}
        self.assertIn("AII-001", rules)
        self.assertIn("AII-002", rules)

    def test_flags_missing_abort_controller_in_ts_stream(self) -> None:
        code = "export async function ask() { return fetch('/api/ai/stream', { method: 'POST' }); }\n"
        violations = audit_integration_file(self._write("stream.ts", code))
        self.assertTrue(any(v.rule_id == "AII-003" for v in violations))

    def test_flags_hardcoded_api_key(self) -> None:
        code = "GEMINI_API_KEY = 'AIzaSyDummySecretValue1234567890'\n"
        violations = audit_integration_file(self._write("secrets.py", code))
        self.assertTrue(any(v.rule_id == "AII-004" for v in violations))

    def test_compliant_gateway_passes(self) -> None:
        py_code = (
            "import os, requests\n"
            "BASE = os.getenv('AI_BASE_URL', 'http://127.0.0.1:11434/v1')\n"
            "def run(prompt):\n"
            "    try:\n"
            "        return requests.post(f'{BASE}/chat', timeout=(3, 15))\n"
            "    except TimeoutError:\n"
            "        if os.getenv('AI_PRIVACY_MODE') == 'hybrid_consent':\n"
            "            return call_gemini(prompt)\n"
            "        raise\n"
        )
        ts_code = (
            "export async function ask() {\n"
            "  const c = new AbortController();\n"
            "  return fetch('/api/ai/stream', { method: 'POST', signal: c.signal });\n"
            "}\n"
        )
        self.assertEqual(len(audit_integration_file(self._write("good.py", py_code))), 0)
        self.assertEqual(len(audit_integration_file(self._write("good.ts", ts_code))), 0)


if __name__ == "__main__":
    unittest.main()
