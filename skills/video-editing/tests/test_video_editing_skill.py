"""Unit tests for skills/video-editing components, references, and validation scripts."""

import json
import os
import sys
import unittest
from pathlib import Path

# Add scripts directory to path
SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from generate_easing_lookup import (
    ease_snap,
    ease_quintic,
    ease_longtail,
    ease_flip,
    build_lookup_table,
)
from audio_silence_validator import validate_cushions


class TestVideoEditingSkillReferences(unittest.TestCase):
    """Verifies reference manuals and catalogs are present and comprehensive."""

    def test_catalog_contains_all_17_styles(self):
        catalog_path = SKILL_ROOT / "references" / "awesome-claude-styles-catalog.md"
        self.assertTrue(catalog_path.exists(), "awesome-claude-styles-catalog.md must exist")
        content = catalog_path.read_text(encoding="utf-8")
        
        expected_styles = [
            "Swiss Grid & Kinetic Type",
            "Flat Vector Explainer",
            "Shape Morph & Liquid",
            "Single Line & Live Drawing",
            "Data Story",
            "Isometric Miniature World",
            "Dark Tech Keynote",
            "Living UI Screencast",
            "HUD & Terminal",
            "Watercolour & Ink",
            "Editorial Print Layout & Collage",
            "Retro 8-Bit Pixel Art",
            "3D Geometric Clay & Orthographic Solids",
            "3D Split-Flap Perspective Flip",
            "Minimalist Monochrome Brand Film",
            "Concentric Sonar & Verification Radar",
            "Broadcast Director Harness",
        ]
        for style in expected_styles:
            self.assertIn(style, content, f"Catalog missing style: {style}")

    def test_all_reference_files_exist(self):
        expected_refs = [
            "awesome-claude-styles-catalog.md",
            "easing-curves-and-motion.md",
            "ffmpeg-streaming-pipeline.md",
            "audio-sync-and-ducking.md",
        ]
        for ref in expected_refs:
            ref_path = SKILL_ROOT / "references" / ref
            self.assertTrue(ref_path.exists(), f"Reference file missing: {ref}")
            self.assertGreater(ref_path.stat().st_size, 500, f"Reference file too small: {ref}")


class TestVideoEditingEasingCurves(unittest.TestCase):
    """Verifies math and boundary conditions of motion graphic easing functions."""

    def test_boundary_conditions(self):
        curves = [ease_snap, ease_quintic, ease_longtail, ease_flip]
        for curve in curves:
            self.assertAlmostEqual(curve(0.0), 0.0, places=5)
            self.assertAlmostEqual(curve(1.0), 1.0, places=5)

    def test_ease_longtail_speed(self):
        # Long-tail settle curve front-loads > 80% of movement in first 40%
        val_at_40 = ease_longtail(0.4)
        self.assertGreater(val_at_40, 0.80, f"ease_longtail not steep enough: {val_at_40}")

    def test_ease_snap_steep_finish(self):
        # Snap curve achieves > 90% by u=0.75
        val_at_75 = ease_snap(0.75)
        self.assertGreater(val_at_75, 0.95, f"ease_snap not steep enough at finish: {val_at_75}")

    def test_ease_flip_perspective(self):
        # ease_flip at 0.5 should be sin(pi/4) approx 0.7071
        self.assertAlmostEqual(ease_flip(0.5), 0.707106, places=4)

    def test_build_lookup_table(self):
        table = build_lookup_table(steps=50)
        self.assertIn("snap", table)
        self.assertIn("quintic", table)
        self.assertIn("longtail", table)
        self.assertIn("flip", table)
        self.assertEqual(len(table["snap"]), 50)
        self.assertAlmostEqual(table["snap"][0], 0.0)
        self.assertAlmostEqual(table["snap"][-1], 1.0)


class TestAudioSilenceValidator(unittest.TestCase):
    """Verifies voiceover timeline cushion detection."""

    def test_valid_timeline_with_sufficient_cushions(self):
        timeline = [
            (0.0, 3.0, "Segment 1"),
            (4.0, 7.0, "Segment 2"),
            (8.0, 11.0, "Segment 3"),
        ]
        is_valid = validate_cushions(timeline, min_cushion=0.85)
        self.assertTrue(is_valid)

    def test_detects_collision(self):
        timeline = [
            (0.0, 3.5, "Segment 1"),
            (3.8, 6.5, "Segment 2"),  # Gap = 0.3s < 0.85s
        ]
        is_valid = validate_cushions(timeline, min_cushion=0.85)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
