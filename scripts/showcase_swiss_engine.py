#!/usr/bin/env python3
"""Swiss Grid & Kinetic Type Engine with 3D Word Flips & Shape-to-Text Morphing.

Features:
- Narrative Arc: "What If...?" dilemma -> SkillBuilder solution & engineering proofs.
- 3D perspective split-flap card flips on high-impact words (zero bug-like stray lines).
- Geometric shape & text morphing (drafting box, diamond, and particle clouds).
- Dynamic FreeType font scaling for crisp vector curves at all zoom levels.
- Pure high-contrast monochrome (#000000 and #FFFFFF) adhering to Awesome Claude rules.
Complies strictly with SkillBuilder cognitive limits (<500 lines).
"""

import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from showcase_text_morph import TextMorphEngine

W, H = 1920, 1080
MARGIN_X = 96
MARGIN_Y = 54
GRID_COLS = 12
COL_W = (W - 2 * MARGIN_X) / GRID_COLS

_morph_engine = None


def get_morph_engine() -> TextMorphEngine:
    """Lazy initialize global TextMorphEngine instance."""
    global _morph_engine
    if _morph_engine is None:
        _morph_engine = TextMorphEngine()
    return _morph_engine


def get_swiss_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    """Load bold Swiss grotesque or clean monospace font."""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Menlo.ttc"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, max(12, int(size)))
        except OSError:
            continue
    return ImageFont.load_default()


def ease_quintic(t: float) -> float:
    """C^2 continuous quintic smoothstep curve."""
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def ease_longtail(t: float) -> float:
    """Cubic-bezier(.16, 1, .3, 1) - slow, long-tail deceleration for rolling numbers."""
    t = max(0.0, min(1.0, t))
    return 1.0 - math.pow(1.0 - t, 3.5)


def to_screen(x: float, y: float, cx: float, cy: float, zoom: float) -> tuple[int, int]:
    """Map world coordinate (x, y) to screen space through camera (cx, cy, zoom)."""
    return int((x - cx) * zoom + W / 2.0), int((y - cy) * zoom + H / 2.0)


def draw_hud_bracket(draw: ImageDraw.ImageDraw, b: tuple[int, int, int, int], color=(255, 255, 255, 255)):
    """Draw Awesome Claude HUD precision drafting lock-on corner brackets [ WORD ] with tick."""
    d = 16
    pad = 10
    x0, y0, x1, y1 = b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad
    draw.line([(x0, y0 + d), (x0, y0), (x0 + d, y0)], fill=color, width=2)
    draw.line([(x1 - d, y0), (x1, y0), (x1, y0 + d)], fill=color, width=2)
    draw.line([(x0, y1 - d), (x0, y1), (x0 + d, y1)], fill=color, width=2)
    draw.line([(x1 - d, y1), (x1, y1), (x1 - d, y1)], fill=color, width=2)
    draw.line([((x0 + x1) // 2 - 8, y0 - 4), ((x0 + x1) // 2 + 8, y0 - 4)], fill=color, width=2)


def draw_grid_lines(draw: ImageDraw.ImageDraw, cx: float = 960.0, cy: float = 540.0, zoom: float = 1.0):
    """Draw subtle 12-column drafting grid lines scaled and shifted by camera."""
    grid_col = (18, 18, 18, 255)
    for c in range(-4, GRID_COLS + 5):
        wx = MARGIN_X + c * COL_W
        sx = int((wx - cx) * zoom + W / 2.0)
        if -20 <= sx <= W + 20:
            draw.line([(sx, 0), (sx, H)], fill=grid_col, width=1)
    for wy in [MARGIN_Y, 540.0, H - MARGIN_Y]:
        sy = int((wy - cy) * zoom + H / 2.0)
        if -20 <= sy <= H + 20:
            draw.line([(0, sy), (W, sy)], fill=grid_col, width=1)
    ret_color = (255, 255, 255, 35)
    draw.line([(948, 540), (972, 540)], fill=ret_color, width=1)
    draw.line([(960, 528), (960, 552)], fill=ret_color, width=1)


def draw_token(draw: ImageDraw.ImageDraw, text: str, wx: float, wy: float, base_size: int,
               cx: float, cy: float, zoom: float, active: bool = False, bold: bool = True,
               anchor: str = "mm", dim_color=(80, 80, 80, 255), is_inv: bool = False) -> tuple[int, int, int, int]:
    """Render dynamic vector text token scaled by zoom, with HUD brackets if active."""
    sx, sy = to_screen(wx, wy, cx, cy, zoom)
    f = get_swiss_font(int(base_size * zoom), bold=bold)
    color = (0, 0, 0, 255) if (is_inv and active) else ((160, 160, 160, 255) if is_inv else ((255, 255, 255, 255) if active else dim_color))
    bbox = draw.textbbox((sx, sy), text, font=f, anchor=anchor)
    draw.text((sx, sy), text, font=f, fill=color, anchor=anchor)
    if active:
        draw_hud_bracket(draw, bbox, color=color)
    return bbox


def draw_flip_token(img: Image.Image, draw: ImageDraw.ImageDraw, text: str, wx: float, wy: float,
                    base_size: int, cx: float, cy: float, zoom: float, flip_p: float,
                    active: bool = False, bold: bool = True, is_inv: bool = False) -> tuple[int, int, int, int]:
    """Render 3D perspective split-flap card flip for high-impact words."""
    p = max(0.0, min(1.0, flip_p))
    scale_y = math.sin(p * math.pi * 0.5)

    sx, sy = to_screen(wx, wy, cx, cy, zoom)
    font_size = max(12, int(base_size * zoom))
    f = get_swiss_font(font_size, bold=bold)

    temp_draw = ImageDraw.Draw(img)
    bbox = temp_draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0] + 20
    th = bbox[3] - bbox[1] + 20

    sub_img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sub_img)
    color = (0, 0, 0, 255) if (is_inv and active) else ((160, 160, 160, 255) if is_inv else ((255, 255, 255, 255) if active else (100, 100, 100, 255)))
    sdraw.text((tw // 2, th // 2), text, font=f, fill=color, anchor="mm")

    new_h = max(2, int(th * scale_y))
    flipped = sub_img.resize((tw, new_h), Image.BILINEAR)

    px = sx - tw // 2
    py = sy - new_h // 2
    img.paste(flipped, (px, py), flipped)

    final_bbox = (sx - tw // 2, sy - th // 2, sx + tw // 2, sy + th // 2)
    if active and p > 0.85:
        draw_hud_bracket(draw, final_bbox, color=color)
    return final_bbox


# --- 11 Distinct Kinetic Shot Renderers with 3D Flips & Shape Morphing ---

def render_shot_1(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 1: 3D Flip 'WHAT IF...' -> Vector morph into 'PROMPT ROULETTE'."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    engine = get_morph_engine()
    if rel_t < 1.4:
        p_flip = ease_quintic(rel_t / 0.7)
        act = (0.2 <= rel_t < 1.4)
        draw_token(draw, "THE PROBLEM SCENARIO", 960, 280, 22, cx, cy, zoom, active=False, bold=False)
        draw_flip_token(img, draw, "WHAT IF...", 620, 480, 86, cx, cy, zoom, p_flip, active=act, bold=True)
        draw_token(draw, "WRITING SOFTWARE WASN'T ABOUT GUESSING PROMPTS?", 960, 580, 28, cx, cy, zoom, active=False, bold=False)
    elif rel_t < 2.5:
        p_morph = ease_quintic((rel_t - 1.4) / 1.1)
        pts, vx, vy = engine.morph_frame("WHAT IF...", "PROMPT ROULETTE", p_morph, center_y=480, turbulence_amp=26.0)
        pts[:, 0] = (pts[:, 0] - cx) * zoom + W / 2.0
        pts[:, 1] = (pts[:, 1] - cy) * zoom + H / 2.0
        arr = np.array(img.convert("L"))
        engine.draw_particles_to_frame(arr, pts, vx * zoom, vy * zoom, intensity=255)
        img = Image.fromarray(arr).convert("RGBA")
        draw = ImageDraw.Draw(img)
        draw_grid_lines(draw, cx, cy, zoom)
    else:
        draw_flip_token(img, draw, "PROMPT ROULETTE.", 1180, 460, 80, cx, cy, zoom, 1.0, active=True, bold=True)
        draw_token(draw, "PROMPTING != DETERMINISTIC SOFTWARE", 960, 560, 32, cx, cy, zoom, active=False, bold=False)
    return img


def render_shot_2(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 2: 3D Flip 'MOCK ARRAYS' & Shape Morph into Drafting Box."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    draw_token(draw, "UNVERIFIED AI GENERATION", 960, 260, 22, cx, cy, zoom, active=False, bold=False)
    act_mock = (rel_t < 1.6)
    act_mono = (rel_t >= 1.6)

    p_flip1 = ease_quintic(min(1.0, rel_t / 0.5))
    draw_flip_token(img, draw, "MOCK ARRAYS.", 640, 430, 72, cx, cy, zoom, p_flip1, active=act_mock, bold=True)

    p_flip2 = ease_quintic(max(0.0, min(1.0, (rel_t - 1.3) / 0.5)))
    draw_flip_token(img, draw, "BLOATED MONOLITHS.", 1220, 490, 72, cx, cy, zoom, p_flip2, active=act_mono, bold=True)

    draw_token(draw, "WHAT IF YOU NEVER DEBUGGED SYNTHETIC SLOP AGAIN?", 960, 600, 26, cx, cy, zoom, active=False, bold=False)
    return img


def render_shot_3(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 3: Mechanical Split-Flap 3D 'SENIOR STAFF' & 'DISCIPLINE'."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    draw_token(draw, "TERMINAL ARCHITECTURE", 960, 260, 22, cx, cy, zoom, active=False, bold=False)
    act_staff = (rel_t < 1.5)
    act_disc = (rel_t >= 1.5)

    draw_token(draw, "WHAT IF EVERY AGENT HAD", 700, 390, 26, cx, cy, zoom, active=False, bold=False)
    p_f1 = ease_quintic(min(1.0, rel_t / 0.6))
    draw_flip_token(img, draw, "SENIOR STAFF", 700, 440, 66, cx, cy, zoom, p_f1, active=act_staff, bold=True)

    p_f2 = ease_quintic(max(0.0, min(1.0, (rel_t - 1.2) / 0.6)))
    draw_flip_token(img, draw, "ENGINEER DISCIPLINE?", 1180, 520, 72, cx, cy, zoom, p_f2, active=act_disc, bold=True)

    draw_token(draw, "RIGOR • SECURITY • CONTRACTS • PURE BOUNDARIES", 960, 620, 22, cx, cy, zoom, active=False, bold=False)
    return img


def render_shot_4(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 4: Diamond Shape Morph into 36 Skills Counter & 'ENTER SKILLBUILDER'."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    engine = get_morph_engine()
    p = ease_longtail(rel_t / (dur * 0.65))
    current_num = int(p * 36)

    act_enter = (rel_t < 1.4)
    act_num = (1.4 <= rel_t < 2.5)
    act_unison = (rel_t >= 2.5)

    p_flip = ease_quintic(min(1.0, rel_t / 0.55))
    draw_flip_token(img, draw, "ENTER SKILLBUILDER.", 680, 420, 68, cx, cy, zoom, p_flip, active=act_enter, bold=True)

    # Mid-flight particle morph from geometric diamond into 36
    if 1.0 < rel_t < 2.2:
        p_morph = ease_quintic((rel_t - 1.0) / 1.1)
        pts, vx, vy = engine.morph_shape_to_text("diamond", f"{current_num:02d}", p_morph, cx=1320, cy=430, size=180)
        pts[:, 0] = (pts[:, 0] - cx) * zoom + W / 2.0
        pts[:, 1] = (pts[:, 1] - cy) * zoom + H / 2.0
        arr = np.array(img.convert("L"))
        engine.draw_particles_to_frame(arr, pts, vx * zoom, vy * zoom, intensity=255)
        img = Image.fromarray(arr).convert("RGBA")
        draw = ImageDraw.Draw(img)
        draw_grid_lines(draw, cx, cy, zoom)
    else:
        draw_token(draw, f"{current_num:02d}", 1320, 430, 220, cx, cy, zoom, active=act_num, bold=True)

    draw_token(draw, "36 SKILLS IN UNISON.", 840, 580, 46, cx, cy, zoom, active=act_unison, bold=True)
    draw_token(draw, "FRONTEND • BACKEND • SECURITY • TESTING • DEVOPS • DATABASE", 960, 660, 20, cx, cy, zoom, active=False, bold=False)
    return img


def render_shot_5(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 5: 3D Flip 'FULL-SCALE MODE' on Stark Paper White Inversion."""
    p = ease_quintic(min(1.0, rel_t / 0.45))
    w_block = int(p * W)
    h_block = int(p * H)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    bx0 = int(((W - w_block) // 2.0 - cx) * zoom + W / 2.0)
    by0 = int(((H - h_block) // 2.0 - cy) * zoom + H / 2.0)
    bx1 = int(((W + w_block) // 2.0 - cx) * zoom + W / 2.0)
    by1 = int(((H + h_block) // 2.0 - cy) * zoom + H / 2.0)
    draw.rectangle([bx0, by0, bx1, by1], fill=(255, 255, 255, 255))

    act_full = (rel_t < 1.7)
    act_arch = (rel_t >= 1.7)
    if p > 0.55:
        p_flip = ease_quintic(min(1.0, (rel_t - 0.25) / 0.55))
        draw_flip_token(img, draw, "FULL-SCALE MODE.", 960, 440, 78, cx, cy, zoom, p_flip, active=act_full, bold=True, is_inv=True)
        draw_token(draw, "ARCHITECTURE PLANNED BEFORE CODE.", 960, 550, 40, cx, cy, zoom, active=act_arch, bold=True, is_inv=True)
        sx0, sy0 = to_screen(MARGIN_X + COL_W, 620, cx, cy, zoom)
        sx1, sy1 = to_screen(W - MARGIN_X - COL_W, 620, cx, cy, zoom)
        draw.line([(sx0, sy0), (sx1, sy1)], fill=(0, 0, 0, 255), width=3)
    return img


def render_shot_6(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 6: Shape Morphing 'MOCK DATA' -> 'REAL PERSISTENCE' & Database Schemas."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    engine = get_morph_engine()
    if rel_t < 1.3:
        p_f = ease_quintic(min(1.0, rel_t / 0.5))
        draw_flip_token(img, draw, "ZERO MOCK DATA.", 640, 420, 78, cx, cy, zoom, p_f, active=True, bold=True)
        draw_token(draw, "PURE SCHEMAS IN PRODUCTION.", 640, 520, 30, cx, cy, zoom, active=False, bold=False)
    elif rel_t < 2.5:
        p_morph = ease_quintic((rel_t - 1.3) / 1.1)
        pts, vx, vy = engine.morph_frame("MOCK DATA", "REAL PERSISTENCE", p_morph, center_y=480, turbulence_amp=26.0)
        pts[:, 0] = (pts[:, 0] - cx) * zoom + W / 2.0
        pts[:, 1] = (pts[:, 1] - cy) * zoom + H / 2.0
        arr = np.array(img.convert("L"))
        engine.draw_particles_to_frame(arr, pts, vx * zoom, vy * zoom, intensity=255)
        img = Image.fromarray(arr).convert("RGBA")
        draw = ImageDraw.Draw(img)
        draw_grid_lines(draw, cx, cy, zoom)
    else:
        draw_flip_token(img, draw, "REAL PERSISTENCE.", 1180, 420, 74, cx, cy, zoom, 1.0, active=True, bold=True)
        draw_token(draw, "SQLITE • POSTGRESQL • SHA-256 DEDUPLICATED BACKUPS", 960, 530, 28, cx, cy, zoom, active=False, bold=False)
    return img


def render_shot_7(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 7: 3D Flip Scale Punch '500' & Fluid Gauge Threshold Charging."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    act_500 = (rel_t < 1.5)
    act_ceil = (rel_t >= 1.5)

    p_f = ease_quintic(min(1.0, rel_t / 0.5))
    draw_flip_token(img, draw, "500", 580, 440, 240, cx, cy, zoom, p_f, active=act_500, bold=True)
    draw_token(draw, "PHYSICAL LINE CEILING", 1180, 480, 48, cx, cy, zoom, active=act_ceil, bold=True)
    draw_token(draw, "COGNITIVE HYGIENE • ZERO BLOAT • PURE DOMAIN SLICES", 1180, 550, 22, cx, cy, zoom, active=False, bold=False)

    p_gauge = ease_quintic(min(1.0, rel_t / 1.8))
    sx0, sy0 = to_screen(900, 600, cx, cy, zoom)
    sx1, sy1 = to_screen(1460, 600, cx, cy, zoom)
    draw.line([(sx0, sy0), (sx1, sy1)], fill=(70, 70, 70, 255), width=2)
    charge_w = int((sx1 - sx0) * p_gauge)
    draw.line([(sx0, sy0), (sx0 + charge_w, sy1)], fill=(255, 255, 255, 255), width=4)
    return img


def render_shot_8(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 8: 5-Tier Verification & Concentric Sonar Radar Wave Morphing."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    act_tier = (rel_t < 1.5)
    act_radar = (1.5 <= rel_t < 2.7)
    act_heal = (rel_t >= 2.7)

    draw_token(draw, "5-TIER VERIFICATION.", 640, 430, 66, cx, cy, zoom, active=act_tier, bold=True)
    draw_token(draw, "AUTONOMOUS SELF-HEALING LOOPS.", 880, 570, 36, cx, cy, zoom, active=act_heal, bold=True)
    draw_token(draw, "STATIC • CONTRACT • TDD • SECURITY • INTEGRATION", 960, 640, 20, cx, cy, zoom, active=False, bold=False)

    rcx, rcy = to_screen(1320, 530, cx, cy, zoom)
    p_wave = (rel_t * 1.5) % 1.0
    for radius in [int(50 * zoom), int(100 * zoom), int(160 * zoom)]:
        draw.ellipse([rcx - radius, rcy - radius, rcx + radius, rcy + radius], outline=(70, 70, 70, 255), width=1)
    ripple_r = int(p_wave * 180 * zoom)
    draw.ellipse([rcx - ripple_r, rcy - ripple_r, rcx + ripple_r, rcy + ripple_r], outline=(255, 255, 255, 120), width=1)
    draw.line([(rcx - int(190 * zoom), rcy), (rcx + int(190 * zoom), rcy)], fill=(90, 90, 90, 255), width=1)
    draw.line([(rcx, rcy - int(190 * zoom)), (rcx, rcy + int(190 * zoom))], fill=(90, 90, 90, 255), width=1)
    draw_token(draw, "100% PASS", 1320, 530, 24, cx, cy, zoom, active=act_radar, bold=True)
    return img


def render_shot_9(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 9: Antigravity Automation & Multi-Agent Node Conduits."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    act_auto = (rel_t < 1.6)
    act_node = (rel_t >= 1.6)

    p_f = ease_quintic(min(1.0, rel_t / 0.55))
    draw_flip_token(img, draw, "ANTIGRAVITY AUTOMATION", 720, 440, 64, cx, cy, zoom, p_f, active=act_auto, bold=True)
    draw_token(draw, "AUTONOMOUS AGENTS IN SYNC • SCHEDULED SIDECARS • ZERO POLLING", 720, 530, 22, cx, cy, zoom, active=False, bold=False)

    ncx, ncy = to_screen(1280, 510, cx, cy, zoom)
    nr = int(24 * zoom)
    draw.ellipse([ncx - nr, ncy - nr, ncx + nr, ncy + nr], fill=(255, 255, 255, 255))
    if act_node:
        draw_hud_bracket(draw, (ncx - nr - 8, ncy - nr - 8, ncx + nr + 8, ncy + nr + 8))
        draw_token(draw, "AGENTS IN SYNC", 1280, 560, 20, cx, cy, zoom, active=False, bold=True)
    return img


def render_shot_10(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 10: 3D Flip 'CONVENTIONAL COMMITS' & Ready-to-Merge PR Alignment."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    act_commit = (rel_t < 1.5)
    act_release = (rel_t >= 1.5)

    p_f1 = ease_quintic(min(1.0, rel_t / 0.55))
    draw_flip_token(img, draw, "CONVENTIONAL COMMITS.", 680, 420, 66, cx, cy, zoom, p_f1, active=act_commit, bold=True)

    p_f2 = ease_quintic(max(0.0, min(1.0, (rel_t - 1.2) / 0.55)))
    draw_flip_token(img, draw, "READY-TO-MERGE RELEASES.", 1180, 510, 66, cx, cy, zoom, p_f2, active=act_release, bold=True)
    sx0, sy0 = to_screen(MARGIN_X, 600, cx, cy, zoom)
    sx1, sy1 = to_screen(W - MARGIN_X, 600, cx, cy, zoom)
    draw.line([(sx0, sy0), (sx1, sy1)], fill=(255, 255, 255, 255), width=2)
    return img


def render_shot_11(rel_t: float, dur: float, cx: float, cy: float, zoom: float) -> Image.Image:
    """Shot 11: 3D Flips 'STOP PROMPTING' -> 'START ENGINEERING' -> SKILLBUILDER Apex."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_lines(draw, cx, cy, zoom)

    engine = get_morph_engine()
    if rel_t < 1.3:
        p_f1 = ease_quintic(min(1.0, rel_t / 0.5))
        draw_flip_token(img, draw, "STOP PROMPTING.", 720, 440, 68, cx, cy, zoom, p_f1, active=True, bold=True)
    elif rel_t < 2.5:
        p_f2 = ease_quintic(min(1.0, (rel_t - 1.3) / 0.5))
        draw_flip_token(img, draw, "START ENGINEERING.", 1200, 440, 68, cx, cy, zoom, p_f2, active=True, bold=True)
    else:
        draw_flip_token(img, draw, "SKILLBUILDER", 960, 490, 120, cx, cy, zoom, 1.0, active=True, bold=True)
        draw_token(draw, "THE APEX HARNESS FOR AGENTIC SOFTWARE ENGINEERING", 960, 580, 26, cx, cy, zoom, active=False, bold=False)
        sx0, sy0 = to_screen(MARGIN_X + 2 * COL_W, 640, cx, cy, zoom)
        sx1, sy1 = to_screen(W - MARGIN_X - 2 * COL_W, 640, cx, cy, zoom)
        draw.line([(sx0, sy0), (sx1, sy1)], fill=(255, 255, 255, 255), width=2)
    return img


SHOT_RENDERERS = [
    render_shot_1, render_shot_2, render_shot_3, render_shot_4,
    render_shot_5, render_shot_6, render_shot_7, render_shot_8,
    render_shot_9, render_shot_10, render_shot_11
]


def render_swiss_frame(shot_idx: int, rel_t: float, dur: float, cx: float = 960.0, cy: float = 540.0, zoom: float = 1.0) -> Image.Image:
    """Dispatch to the dedicated Swiss shot renderer with camera state (cx, cy, zoom)."""
    idx = max(0, min(len(SHOT_RENDERERS) - 1, shot_idx))
    return SHOT_RENDERERS[idx](rel_t, dur, cx, cy, zoom)


if __name__ == "__main__":
    test_img = render_swiss_frame(0, 0.8, 3.75, 620.0, 480.0, 1.85)
    print(f"[OK] Swiss Engine with 3D Flips ready. Size: {test_img.size}")
