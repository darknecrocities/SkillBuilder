#!/usr/bin/env python3
"""
generate_svg_squircle_kit.py - Pure-stdlib App Icon Kit Generator.

Generates an Apple continuous-curvature squircle master SVG (512x512),
a theme-adaptive favicon.svg, and an Android adaptive foreground/background
SVG pair (108dp canvas with 66dp safe area) from a clean geometric mark.
"""

import argparse
import html
from pathlib import Path
import sys
from typing import List

DEFAULT_MARK_PATH = "M 256 132 L 348 256 L 256 380 L 164 256 Z"

SQUIRCLE_PATH = (
    "M 140 32 C 48 32, 32 48, 32 140 "
    "L 32 372 C 32 464, 48 480, 140 480 "
    "L 372 480 C 464 480, 480 464, 480 372 "
    "L 480 140 C 480 48, 464 32, 372 32 Z"
)


def build_apple_squircle_svg(title: str, mark_path: str, bg_hex: str, fg_hex: str, accent_hex: str) -> str:
    """Build 512x512 Apple continuous-curvature squircle app icon SVG."""
    safe_title = html.escape(title)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="{safe_title} App Icon">
  <defs>
    <clipPath id="squircle-clip">
      <path d="{SQUIRCLE_PATH}" />
    </clipPath>
    <linearGradient id="squircle-zenith" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.02" />
    </linearGradient>
  </defs>
  <g clip-path="url(#squircle-clip)">
    <rect width="512" height="512" fill="{bg_hex}" />
    <path d="{mark_path}" fill="{fg_hex}" />
    <circle cx="256" cy="256" r="24" fill="{bg_hex}" />
    <circle cx="256" cy="256" r="11" fill="{accent_hex}" />
  </g>
  <path d="{SQUIRCLE_PATH}" fill="none" stroke="url(#squircle-zenith)" stroke-width="3" />
</svg>
"""


def build_adaptive_favicon_svg(title: str, accent_hex: str) -> str:
    """Build theme-adaptive favicon.svg supporting dark and light browser tabs."""
    safe_title = html.escape(title)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="{safe_title} Favicon">
  <style>
    .bg {{ fill: #09090b; }}
    .fg {{ fill: #f4f4f5; }}
    .accent {{ fill: {accent_hex}; }}
    @media (prefers-color-scheme: light) {{
      .bg {{ fill: #f4f4f5; }}
      .fg {{ fill: #09090b; }}
    }}
  </style>
  <rect class="bg" x="4" y="4" width="56" height="56" rx="14" />
  <path class="fg" d="M 32 14 L 46 32 L 32 50 L 18 32 Z" />
  <circle class="bg" cx="32" cy="32" r="7" />
  <circle class="accent" cx="32" cy="32" r="3.5" />
</svg>
"""


def build_android_adaptive_pair(mark_path: str, bg_hex: str, fg_hex: str, accent_hex: str) -> List[str]:
    """Build Android 108dp adaptive background and 66dp-safe foreground SVGs."""
    background_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108" width="108" height="108">
  <rect width="108" height="108" fill="{bg_hex}" />
</svg>
"""
    scale = 66.0 / 512.0
    offset = (108.0 - 512.0 * scale) / 2.0
    foreground_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108" width="108" height="108">
  <g transform="translate({offset:.2f}, {offset:.2f}) scale({scale:.4f})">
    <path d="{mark_path}" fill="{fg_hex}" />
    <circle cx="256" cy="256" r="24" fill="{bg_hex}" />
    <circle cx="256" cy="256" r="11" fill="{accent_hex}" />
  </g>
</svg>
"""
    return [background_svg, foreground_svg]


def generate_kit(
    out_dir: Path,
    title: str,
    mark_path: str = DEFAULT_MARK_PATH,
    bg_hex: str = "#09090b",
    fg_hex: str = "#f4f4f5",
    accent_hex: str = "#38bdf8",
) -> List[Path]:
    """Write all generated SVG icon artifacts into out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    bg_svg, fg_svg = build_android_adaptive_pair(mark_path, bg_hex, fg_hex, accent_hex)
    outputs = {
        out_dir / "app-icon-squircle.svg": build_apple_squircle_svg(title, mark_path, bg_hex, fg_hex, accent_hex),
        out_dir / "favicon.svg": build_adaptive_favicon_svg(title, accent_hex),
        out_dir / "android-adaptive-bg.svg": bg_svg,
        out_dir / "android-adaptive-fg.svg": fg_svg,
    }
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    return list(outputs.keys())


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate cross-platform app icon SVG kit.")
    parser.add_argument("--out-dir", required=True, help="Output directory for generated SVGs")
    parser.add_argument("--title", default="App", help="Application name for ARIA labels")
    parser.add_argument("--bg", default="#09090b", help="Background canvas hex color")
    parser.add_argument("--fg", default="#f4f4f5", help="Foreground silhouette hex color")
    parser.add_argument("--accent", default="#38bdf8", help="Intentional accent hex color")
    args = parser.parse_args()

    created = generate_kit(Path(args.out_dir), args.title, bg_hex=args.bg, fg_hex=args.fg, accent_hex=args.accent)
    for item in created:
        print(f"+ {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
