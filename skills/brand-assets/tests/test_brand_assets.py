#!/usr/bin/env python3
"""Unit tests for brand-assets squircle generator and SVG auditor."""

import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import generate_svg_squircle_kit  # noqa: E402
import verify_brand_assets  # noqa: E402


class TestBrandAssets(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_dir = Path(__file__).resolve().parent.parent

    def test_templates_pass_brand_audit(self) -> None:
        violations = verify_brand_assets.scan_assets(self.skill_dir / "templates")
        self.assertEqual(violations, [])

    def test_generated_squircle_kit_passes_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            created = generate_svg_squircle_kit.generate_kit(Path(tmp), title="DarkNecro")
            self.assertEqual(len(created), 4)
            violations = verify_brand_assets.scan_assets(Path(tmp))
            self.assertEqual(violations, [])

    def test_flags_editor_bloat_and_generic_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "logo-bad.svg"
            bad.write_text(
                '<svg><metadata>Adobe Illustrator</metadata><defs><linearGradient id="grad1"/></defs>'
                '<image href="data:image/png;base64,AAA" /></svg>',
                encoding="utf-8",
            )
            issues = verify_brand_assets.scan_assets(bad)
            rules = {i["rule"] for i in issues}
            self.assertIn("BRAND-SVG-MISSING-VIEWBOX", rules)
            self.assertIn("BRAND-SVG-RASTER-CHEAT", rules)
            self.assertIn("BRAND-SVG-EDITOR-BLOAT", rules)
            self.assertIn("BRAND-SVG-GENERIC-ID-COLLISION", rules)


if __name__ == "__main__":
    unittest.main()
