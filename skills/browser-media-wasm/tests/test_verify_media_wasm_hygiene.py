#!/usr/bin/env python3
"""Unit tests for browser-media-wasm lifecycle auditor."""

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verify_media_wasm_hygiene  # noqa: E402


class TestVerifyMediaWasmHygiene(unittest.TestCase):
    def test_detects_objecturl_worker_and_audio_leaks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "leakyMedia.ts"
            bad.write_text(
                "const u = URL.createObjectURL(blob);\n"
                "const w = new Worker('./w.js');\n"
                "const ctx = new AudioContext();\n",
                encoding="utf-8",
            )
            issues = verify_media_wasm_hygiene.scan_directory(bad)
            rules = {i["rule"] for i in issues}
            self.assertEqual(rules, {"MEDIA-OBJECTURL-LEAK", "MEDIA-WORKER-NO-TERMINATE", "MEDIA-AUDIOCONTEXT-LEAK"})

    def test_clean_lifecycle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "cleanMedia.ts"
            good.write_text(
                "const u = URL.createObjectURL(blob);\nURL.revokeObjectURL(u);\n"
                "const w = new Worker('./w.js');\nw.terminate();\n"
                "const ctx = new AudioContext();\nawait ctx.close();\n",
                encoding="utf-8",
            )
            self.assertEqual(verify_media_wasm_hygiene.scan_directory(good), [])


if __name__ == "__main__":
    unittest.main()
