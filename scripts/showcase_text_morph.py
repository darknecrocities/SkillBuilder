#!/usr/bin/env python3
"""Kinetic Text Morphing and Particle Vector Interpolation Engine.

Provides frame-by-frame point-cloud extraction, sorted trajectory matching,
per-particle fluid turbulence, dynamic velocity streaks, and cryptographic
monospace character scrambling in stark monochromatic black and white.
Complies with SkillBuilder cognitive limits (<500 lines).
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
N_PARTICLES = 4500
GLYPH_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/_+-*#~<>"


class TextMorphEngine:
    """Caches point clouds for phrases and renders smooth per-frame morphs."""

    def __init__(self):
        try:
            self.title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 108)
            self.title_font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 124)
            self.sub_font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 24)
        except OSError:
            try:
                self.title_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 100)
                self.title_font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 112)
                self.sub_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
            except OSError:
                self.title_font = ImageFont.load_default()
                self.title_font_large = ImageFont.load_default()
                self.sub_font = ImageFont.load_default()

        self.point_cache = {}

    def get_phrase_points(self, text: str, font_size: int = 108, center_y: int = 540) -> np.ndarray:
        """Rasterize text and extract N_PARTICLES coordinates sorted spatially."""
        cache_key = (text, font_size, center_y)
        if cache_key in self.point_cache:
            return self.point_cache[cache_key]

        font = self.title_font_large if font_size > 110 else self.title_font
        img = Image.new("L", (W, H), 0)
        draw = ImageDraw.Draw(img)

        # Draw centered text
        draw.text((W // 2, center_y), text, font=font, fill=255, anchor="mm")
        arr = np.array(img)
        ys, xs = np.where(arr > 120)

        if len(xs) == 0:
            # Fallback if empty text
            pts = np.zeros((N_PARTICLES, 2), dtype=np.float32)
            pts[:, 0] = W // 2
            pts[:, 1] = center_y
            self.point_cache[cache_key] = pts
            return pts

        # Resample to exactly N_PARTICLES
        if len(xs) >= N_PARTICLES:
            indices = np.linspace(0, len(xs) - 1, N_PARTICLES, dtype=int)
            sel_x = xs[indices].astype(np.float32)
            sel_y = ys[indices].astype(np.float32)
        else:
            repeats = int(math.ceil(N_PARTICLES / len(xs)))
            sel_x = np.tile(xs, repeats)[:N_PARTICLES].astype(np.float32)
            sel_y = np.tile(ys, repeats)[:N_PARTICLES].astype(np.float32)
            # Add minor subpixel jitter to duplicated points
            sel_x += np.random.uniform(-0.8, 0.8, N_PARTICLES)
            sel_y += np.random.uniform(-0.8, 0.8, N_PARTICLES)

        # Sort points spatially by X + 0.3*Y for natural left-to-right laminar flow
        sort_order = np.argsort(sel_x + 0.35 * sel_y)
        pts = np.column_stack((sel_x[sort_order], sel_y[sort_order]))

        self.point_cache[cache_key] = pts
        return pts

    def get_shape_points(self, shape: str, cx: float = 960.0, cy: float = 540.0, size: float = 280.0) -> np.ndarray:
        """Generate N_PARTICLES coordinates for geometric shapes (box, circle, diamond)."""
        cache_key = (shape, cx, cy, size)
        if cache_key in self.point_cache:
            return self.point_cache[cache_key]

        pts = np.zeros((N_PARTICLES, 2), dtype=np.float32)
        if shape == "circle":
            theta = np.linspace(0, 2 * math.pi, N_PARTICLES, endpoint=False)
            r = size + np.random.uniform(-3, 3, N_PARTICLES)
            pts[:, 0] = cx + r * np.cos(theta)
            pts[:, 1] = cy + r * np.sin(theta)
        elif shape == "diamond":
            p_edge = np.linspace(0, 4, N_PARTICLES, endpoint=False)
            for i in range(N_PARTICLES):
                e = p_edge[i]
                frac = e % 1.0
                if e < 1.0:
                    pts[i] = [cx + frac * size, cy - (1.0 - frac) * size]
                elif e < 2.0:
                    pts[i] = [cx + (1.0 - frac) * size, cy + frac * size]
                elif e < 3.0:
                    pts[i] = [cx - frac * size, cy + (1.0 - frac) * size]
                else:
                    pts[i] = [cx - (1.0 - frac) * size, cy - frac * size]
        else:  # "box" default
            p_edge = np.linspace(0, 4, N_PARTICLES, endpoint=False)
            hw, hh = size, size * 0.55
            for i in range(N_PARTICLES):
                e = p_edge[i]
                frac = e % 1.0
                if e < 1.0:
                    pts[i] = [cx - hw + frac * 2 * hw, cy - hh]
                elif e < 2.0:
                    pts[i] = [cx + hw, cy - hh + frac * 2 * hh]
                elif e < 3.0:
                    pts[i] = [cx + hw - frac * 2 * hw, cy + hh]
                else:
                    pts[i] = [cx - hw, cy + hh - frac * 2 * hh]

        pts[:, 0] += np.random.uniform(-0.8, 0.8, N_PARTICLES)
        pts[:, 1] += np.random.uniform(-0.8, 0.8, N_PARTICLES)
        sort_order = np.argsort(pts[:, 0] + 0.35 * pts[:, 1])
        sorted_pts = pts[sort_order]
        self.point_cache[cache_key] = sorted_pts
        return sorted_pts

    def _interpolate_points(
        self,
        pts_a: np.ndarray,
        pts_b: np.ndarray,
        progress: float,
        turbulence_amp: float = 32.0
    ) -> tuple:
        """Interpolate point clouds with fluid turbulence."""
        p = max(0.0, min(1.0, progress))
        e = p * p * (3.0 - 2.0 * p)
        curr_pts = (1.0 - e) * pts_a + e * pts_b

        mid_factor = math.sin(math.pi * p)
        vel_x = np.zeros(N_PARTICLES, dtype=np.float32)
        vel_y = np.zeros(N_PARTICLES, dtype=np.float32)

        if mid_factor > 0.001:
            turb_x = np.sin(pts_a[:, 1] * 0.025 + p * 14.0) * turbulence_amp * mid_factor
            turb_y = np.cos(pts_a[:, 0] * 0.025 + p * 14.0) * turbulence_amp * mid_factor
            curr_pts[:, 0] += turb_x
            curr_pts[:, 1] += turb_y
            vel_x = (pts_b[:, 0] - pts_a[:, 0]) * (e - p) + turb_x * 0.4
            vel_y = (pts_b[:, 1] - pts_a[:, 1]) * (e - p) + turb_y * 0.4

        return curr_pts, vel_x, vel_y

    def morph_frame(
        self,
        text_from: str,
        text_to: str,
        progress: float,
        center_y: int = 540,
        turbulence_amp: float = 32.0,
    ) -> tuple:
        """Compute particle coordinates and velocity vectors for text-to-text morphing."""
        pts_a = self.get_phrase_points(text_from, center_y=center_y)
        pts_b = self.get_phrase_points(text_to, center_y=center_y)
        return self._interpolate_points(pts_a, pts_b, progress, turbulence_amp)

    def morph_shape_to_text(
        self,
        shape: str,
        text_to: str,
        progress: float,
        cx: float = 960.0,
        cy: float = 540.0,
        size: float = 280.0,
        turbulence_amp: float = 28.0
    ) -> tuple:
        """Morph from geometric drafting shape into vector typography."""
        pts_a = self.get_shape_points(shape, cx=cx, cy=cy, size=size)
        pts_b = self.get_phrase_points(text_to, center_y=int(cy))
        return self._interpolate_points(pts_a, pts_b, progress, turbulence_amp)

    def scramble_text(self, target_str: str, progress: float, seed: int = 0) -> str:
        """Cryptographically scramble characters until progress locks each glyph."""
        n = len(target_str)
        if n == 0:
            return ""
        chars = list(target_str)
        rng = random.Random(seed + int(progress * 100))
        for i in range(n):
            lock_threshold = (i + 1) / float(n + 1)
            if progress < lock_threshold:
                if target_str[i] not in (" ", "/", "-", ":", "[", "]"):
                    chars[i] = rng.choice(GLYPH_CHARS)
        return "".join(chars)

    def draw_particles_to_frame(
        self,
        frame_arr: np.ndarray,
        pts: np.ndarray,
        vel_x: np.ndarray = None,
        vel_y: np.ndarray = None,
        intensity: int = 255
    ):
        """Render vectorized 3x3 particles with directional motion blur velocity streaks."""
        xs = np.clip(np.round(pts[:, 0]).astype(int), 3, W - 4)
        ys = np.clip(np.round(pts[:, 1]).astype(int), 3, H - 4)

        # Center core (brightest)
        frame_arr[ys, xs] = np.maximum(frame_arr[ys, xs], intensity)
        # 4-connected cross
        cross_intensity = int(intensity * 0.75)
        frame_arr[ys - 1, xs] = np.maximum(frame_arr[ys - 1, xs], cross_intensity)
        frame_arr[ys + 1, xs] = np.maximum(frame_arr[ys + 1, xs], cross_intensity)
        frame_arr[ys, xs - 1] = np.maximum(frame_arr[ys, xs - 1], cross_intensity)
        frame_arr[ys, xs + 1] = np.maximum(frame_arr[ys, xs + 1], cross_intensity)

        # Draw motion blur streaks along velocity vector
        if vel_x is not None and vel_y is not None:
            streak_len = np.clip(np.hypot(vel_x, vel_y) * 0.25, 0.0, 8.0)
            has_motion = streak_len > 1.2
            if np.any(has_motion):
                sx = xs[has_motion]
                sy = ys[has_motion]
                vx = vel_x[has_motion]
                vy = vel_y[has_motion]
                # Tail 1
                t1x = np.clip(np.round(sx - vx * 0.35).astype(int), 2, W - 3)
                t1y = np.clip(np.round(sy - vy * 0.35).astype(int), 2, H - 3)
                frame_arr[t1y, t1x] = np.maximum(frame_arr[t1y, t1x], int(intensity * 0.55))
                # Tail 2
                t2x = np.clip(np.round(sx - vx * 0.70).astype(int), 2, W - 3)
                t2y = np.clip(np.round(sy - vy * 0.70).astype(int), 2, H - 3)
                frame_arr[t2y, t2x] = np.maximum(frame_arr[t2y, t2x], int(intensity * 0.30))

    def draw_solid_text_overlay(
        self,
        base_img: Image.Image,
        text: str,
        alpha: float,
        center_y: int = 540,
        tracking_offset: float = 0.0
    ):
        """Crossfade solid high-res raster typography when morph is settled."""
        if alpha <= 0.01:
            return
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        font = self.title_font
        fill_val = int(255 * alpha)
        draw.text((W // 2 + tracking_offset, center_y), text, font=font, fill=(255, 255, 255, fill_val), anchor="mm")
        base_img.alpha_composite(overlay)


if __name__ == "__main__":
    engine = TextMorphEngine()
    pts = engine.get_phrase_points("SKILLBUILDER")
    print(f"[OK] TextMorphEngine initialized. Points shape: {pts.shape}")
