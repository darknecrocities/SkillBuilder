#!/usr/bin/env python3
"""Unit tests for verify_vlm_hygiene.py."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_vlm_hygiene import audit_vlm_file


class TestVerifyVLMHygiene(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, name: str, content: str) -> str:
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_flags_raw_b64_and_missing_timeout(self) -> None:
        code = (
            "import base64, requests\n"
            "def run_qwen_vl(raw_bytes):\n"
            "    b64 = base64.b64encode(raw_bytes).decode()\n"
            "    return requests.post('http://127.0.0.1:11434/api/chat', json={'images': [b64]})\n"
        )
        violations = audit_vlm_file(self._write("bad_vlm.py", code))
        rules = {v.rule_id for v in violations}
        self.assertIn("VLM-001", rules)
        self.assertIn("VLM-004", rules)

    def test_flags_unthrottled_video_loop_and_missing_schema(self) -> None:
        code = (
            "import cv2\n"
            "def extract_video(cap):\n"
            "    while cap.read()[0]:\n"
            "        call_qwen_vl('extract bbox')\n"
        )
        violations = audit_vlm_file(self._write("bad_vid.py", code))
        rules = {v.rule_id for v in violations}
        self.assertIn("VLM-002", rules)
        self.assertIn("VLM-003", rules)

    def test_compliant_vlm_pipeline_passes(self) -> None:
        code = (
            "import base64, requests\n"
            "from PIL import Image\n"
            "from pydantic import BaseModel\n"
            "class BBoxOut(BaseModel):\n"
            "    label: str\n"
            "def ask_vlm(img: Image.Image):\n"
            "    img.thumbnail((1280, 1280))\n"
            "    b64 = base64.b64encode(b'jpg').decode()\n"
            "    return requests.post(\n"
            "        'http://127.0.0.1:11434/api/chat',\n"
            "        json={'model': 'qwen2.5vl:7b', 'images': [b64], 'format': BBoxOut.model_json_schema()},\n"
            "        timeout=(3.0, 20.0),\n"
            "    )\n"
        )
        violations = audit_vlm_file(self._write("good_vlm.py", code))
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
