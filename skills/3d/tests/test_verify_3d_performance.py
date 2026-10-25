#!/usr/bin/env python3
"""
Unit tests for verify_3d_performance.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_3d_performance import audit_3d_file


class TestVerify3DPerformance(unittest.TestCase):
    def test_clean_threejs_scene_passes(self):
        code = """
        import * as THREE from 'three';
        import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader';
        import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

        const loader = new GLTFLoader();
        const draco = new DRACOLoader();
        loader.setDRACOLoader(draco);

        const renderer = new THREE.WebGLRenderer();
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2.0));

        // Cleanup
        renderer.dispose();
        """
        violations = audit_3d_file("Scene.tsx", code)
        self.assertEqual(len(violations), 0)

    def test_detects_unclamped_dpr(self):
        code = """
        import * as THREE from 'three';
        const renderer = new THREE.WebGLRenderer();
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.dispose();
        """
        violations = audit_3d_file("Canvas.tsx", code)
        self.assertTrue(any(v["rule"] == "UNCLAMPED-DEVICE-PIXEL-RATIO" for v in violations))

    def test_detects_gltf_without_draco(self):
        code = """
        import * as THREE from 'three';
        import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
        const loader = new GLTFLoader();
        const renderer = new THREE.WebGLRenderer();
        renderer.dispose();
        """
        violations = audit_3d_file("CarModel.tsx", code)
        self.assertTrue(any(v["rule"] == "MISSING-DRACO-COMPRESSION" for v in violations))

    def test_detects_missing_webgl_disposal(self):
        code = """
        import * as THREE from 'three';
        const renderer = new THREE.WebGLRenderer();
        """
        violations = audit_3d_file("LeakyCanvas.tsx", code)
        self.assertTrue(any(v["rule"] == "MISSING-WEBGL-DISPOSAL" for v in violations))


if __name__ == "__main__":
    unittest.main()
