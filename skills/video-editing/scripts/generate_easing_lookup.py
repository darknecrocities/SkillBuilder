#!/usr/bin/env python3
"""Mathematical Easing Curve Generator and Lookup Table Builder.

Computes and evaluates mathematical animation curves:
- Snap easing (cubic-bezier(.7, 0, .2, 1))
- Quintic smoothstep (6u^5 - 15u^4 + 10u^3)
- Long-tail counter easing (cubic-bezier(.16, 1, .3, 1))
- 3D perspective card flip (sin(u * pi/2))
Complies strictly with SkillBuilder cognitive limits (<500 lines).
"""

import math
import numpy as np


def ease_snap(u: float) -> float:
    """Cubic-bezier(.7, 0, .2, 1) snap curve approximation."""
    u = max(0.0, min(1.0, u))
    return 1.0 - math.pow(1.0 - u, 4.0) if u > 0.5 else 4.0 * math.pow(u, 3.0)


def ease_quintic(u: float) -> float:
    """Continuous quintic smoothstep curve."""
    u = max(0.0, min(1.0, u))
    return u * u * u * (u * (u * 6.0 - 15.0) + 10.0)


def ease_longtail(u: float) -> float:
    """Cubic-bezier(.16, 1, .3, 1) long-tail counter settle curve."""
    u = max(0.0, min(1.0, u))
    return 1.0 - math.pow(1.0 - u, 3.5)


def ease_flip(u: float) -> float:
    """3D perspective card flip vertical scale."""
    u = max(0.0, min(1.0, u))
    return math.sin(u * math.pi * 0.5)


def build_lookup_table(steps: int = 100) -> dict:
    """Generate normalized lookup tables for all core animation curves."""
    us = np.linspace(0.0, 1.0, steps)
    return {
        "snap": [ease_snap(float(u)) for u in us],
        "quintic": [ease_quintic(float(u)) for u in us],
        "longtail": [ease_longtail(float(u)) for u in us],
        "flip": [ease_flip(float(u)) for u in us],
    }


if __name__ == "__main__":
    lut = build_lookup_table(10)
    print("=== Easing Lookup Table Verification (10 samples) ===")
    for name, vals in lut.items():
        print(f"• {name.capitalize():8s}: {vals[0]:.2f} -> {vals[5]:.2f} -> {vals[-1]:.2f}")
    assert all(0.0 <= v <= 1.0 for vals in lut.values() for v in vals)
    print("[PASS] Easing curves bounded in [0.0, 1.0].")
