#!/usr/bin/env python3
"""Unit tests for 2d-mascot-motion verifier and templates."""

import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import verify_mascot_assets  # noqa: E402


class TestVerifyMascotAssets(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_dir = Path(__file__).resolve().parent.parent

    def test_templates_pass_audit(self) -> None:
        violations = verify_mascot_assets.scan_path(self.skill_dir / "templates")
        self.assertEqual(violations, [])

    def test_detects_embedded_raster_and_node_bloat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_svg = Path(tmp) / "slop_mascot.svg"
            bloat_cmds = " ".join(["L 1 1"] * 130)
            bad_svg.write_text(
                f'<svg><image href="data:image/png;base64,AAAA" /><path d="M 0 0 {bloat_cmds}" /></svg>',
                encoding="utf-8",
            )
            issues = verify_mascot_assets.scan_path(bad_svg)
            rules = {item["rule"] for item in issues}
            self.assertIn("SVG-MISSING-VIEWBOX", rules)
            self.assertIn("SVG-EMBEDDED-RASTER-SLOP", rules)
            self.assertIn("SVG-JITTER-NODE-BLOAT", rules)

    def test_detects_missing_rive_cleanup_and_reduced_motion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_tsx = Path(tmp) / "BadMascot.tsx"
            bad_tsx.write_text(
                'import { useRive } from "@rive-app/react-canvas";\n'
                'export function BadMascot() { const { RiveComponent } = useRive({ src: "/m.riv" }); return <RiveComponent />; }',
                encoding="utf-8",
            )
            issues = verify_mascot_assets.scan_path(bad_tsx)
            rules = {item["rule"] for item in issues}
            self.assertIn("RIVE-MISSING-DISPOSAL", rules)
            self.assertIn("MASCOT-MISSING-REDUCED-MOTION", rules)


if __name__ == "__main__":
    unittest.main()
