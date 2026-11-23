#!/usr/bin/env python3
"""Unit tests for verify_cv_hygiene.py."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_cv_hygiene import audit_cv_file


class TestVerifyCVHygiene(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, name: str, content: str) -> str:
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_flags_unreleased_capture_and_unbounded_queue(self) -> None:
        code = (
            "import cv2, queue\n"
            "q = queue.Queue()\n"
            "cap = cv2.VideoCapture(0)\n"
            "ok, frame = cap.read()\n"
        )
        violations = audit_cv_file(self._write("bad_cam.py", code))
        rules = {v.rule_id for v in violations}
        self.assertIn("CV-001", rules)
        self.assertIn("CV-002", rules)

    def test_flags_blocking_gui_and_missing_ort_providers(self) -> None:
        code = (
            "import cv2, onnxruntime as ort\n"
            "sess = ort.InferenceSession('det.onnx')\n"
            "cv2.imshow('dbg', frame)\n"
            "cv2.waitKey(0)\n"
        )
        violations = audit_cv_file(self._write("bad_ort.py", code))
        rules = {v.rule_id for v in violations}
        self.assertIn("CV-004", rules)
        self.assertIn("CV-005", rules)

    def test_flags_missing_exif_transpose(self) -> None:
        code = (
            "from PIL import Image\n"
            "def prep(path):\n"
            "    frame = Image.open(path)\n"
            "    return frame\n"
        )
        violations = audit_cv_file(self._write("exif.py", code))
        self.assertTrue(any(v.rule_id == "CV-003" for v in violations))

    def test_compliant_cv_pipeline_passes(self) -> None:
        code = (
            "import cv2, queue, onnxruntime as ort\n"
            "from PIL import Image, ImageOps\n"
            "q = queue.Queue(maxsize=2)\n"
            "sess = ort.InferenceSession('yolo.onnx', providers=['CPUExecutionProvider'])\n"
            "def read_once():\n"
            "    cap = cv2.VideoCapture(0)\n"
            "    try:\n"
            "        return cap.read()\n"
            "    finally:\n"
            "        cap.release()\n"
            "def load_img(p):\n"
            "    return ImageOps.exif_transpose(Image.open(p))\n"
        )
        violations = audit_cv_file(self._write("good_cv.py", code))
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
