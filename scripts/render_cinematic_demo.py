#!/usr/bin/env python3
"""Cinematic Demo Video Renderer with Dynamic Camera Shifts and Telemetry HUD.

Renders dramatic 2.0x-2.2x camera punch-ins, continuous pan-and-glide vectors,
glowing highlight bounding boxes, and glassmorphic telemetry HUD badges.
Complies strictly with SkillBuilder 500-line limits and production standards.
"""

import math
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 1250
FPS = 60.0
DEFAULT_CX = WIDTH / 2.0
DEFAULT_CY = HEIGHT / 2.0

# 8 Pixel-Calibrated Highlights:
# (t_start, t_peak_in, t_peak_out, t_end, (p1_x, p1_y), (p2_x, p2_y), zoom_max, badge_text, box1, box2)
HIGHLIGHTS = [
    # 1. GitHub repo view: Click on skills directory
    (10.5, 11.2, 14.5, 15.2, (450.0, 720.0), (600.0, 580.0), 2.00,
     "REPO EXPLORATION // GitHub skills/ Directory",
     [185, 698, 480, 742], [185, 410, 600, 800]),

    # 2. backend/SKILL.md: Click on file, then scroll down to Clean Architecture
    (18.0, 19.0, 26.0, 26.8, (500.0, 720.0), (680.0, 420.0), 2.00,
     "CLEAN ARCHITECTURE // Core Domain & Persistence",
     [380, 695, 540, 740], [350, 240, 950, 420]),

    # 3. Live Runtime: Gemini 3.8 Flash High agent editing files in middle column
    (29.5, 30.5, 37.5, 38.5, (705.0, 350.0), (705.0, 550.0), 2.00,
     "LIVE RUNTIME // Gemini 3.8 Flash High Agent Execution",
     [370, 200, 1040, 600], [370, 200, 1040, 600]),

    # 4. QA Remediation Plan: Click card on left, camera shifts to plan on right
    (41.5, 42.5, 52.0, 53.0, (705.0, 575.0), (1480.0, 350.0), 2.00,
     "QA REMEDIATION PLAN // Two-Tier Visual Bug Fixes",
     [370, 520, 1040, 630], [1080, 140, 1880, 520]),

    # 5. Hit Command /fu: Autocomplete menu popup + prompt input
    (64.0, 65.0, 73.0, 74.0, (705.0, 1120.0), (705.0, 940.0), 2.00,
     "HIT COMMAND // /full Autocomplete & Orchestration",
     [370, 852, 1040, 1225], [370, 852, 1040, 1225]),

    # 6. Hit Command /Ai: Tooltip cards for anti-slop and google-antigravity-sdk
    (75.0, 76.0, 84.0, 85.0, (705.0, 1120.0), (705.0, 940.0), 2.00,
     "HIT COMMAND // /Ai & /anti-slop Tooltip Cards",
     [370, 852, 1040, 1225], [370, 852, 1040, 1225]),

    # 7. Portfolio localhost:3001: Verified Swiss headline and Capabilities
    (88.0, 89.0, 97.5, 98.5, (500.0, 475.0), (960.0, 520.0), 2.00,
     "VERIFIED OUTPUT // Zero Clipping & 99.99% Alignment",
     [80, 330, 910, 620], [165, 265, 1755, 745]),

    # 8. Gate Passed: Vitest, TypeScript, build, and 500-line limit audit
    (100.5, 101.5, 105.5, 106.3, (705.0, 630.0), (1480.0, 390.0), 2.00,
     "GATE PASSED // 30 Test Suites & 500-Line Limit",
     [370, 570, 1040, 690], [1080, 140, 1880, 640]),
]


def create_hud_badge(text: str) -> Image.Image:
    """Pre-render a high-contrast Apple-style glassmorphic HUD badge."""
    w, h = 540, 44
    badge = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    # Background chassis with rounded corners
    draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=8, fill=(12, 13, 14, 235), outline=(56, 189, 248, 255), width=1)
    # Emerald status dot
    draw.ellipse([16, 15, 28, 27], fill=(16, 185, 129, 255))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 15)
    except OSError:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
        except OSError:
            font = ImageFont.load_default()
    draw.text((38, 13), text, fill=(241, 245, 249, 255), font=font)
    return badge


def get_camera_state(t: float):
    """Compute smoothed camera zoom, center coordinates, active badge, and highlight box."""
    for (t_start, t_peak_in, t_peak_out, t_end, (x1, y1), (x2, y2), z_max, badge_text, box1, box2) in HIGHLIGHTS:
        if t_start <= t <= t_end:
            v_prog = (t - t_start) / max(0.001, t_end - t_start)
            target_cx = x1 + (x2 - x1) * v_prog
            target_cy = y1 + (y2 - y1) * v_prog

            if box1 == box2 or v_prog < 0.45:
                active_box = box1
                box_fade = 1.0
            elif v_prog > 0.55:
                active_box = box2
                box_fade = 1.0
            else:
                # Mid-flight crossfade
                box_fade = 0.5
                active_box = box2 if v_prog >= 0.5 else box1

            if t < t_peak_in:
                u = (t - t_start) / max(0.001, t_peak_in - t_start)
                factor = 0.5 * (1.0 - math.cos(math.pi * u))
                zoom = 1.0 + (z_max - 1.0) * factor
                cx = DEFAULT_CX + (target_cx - DEFAULT_CX) * factor
                cy = DEFAULT_CY + (target_cy - DEFAULT_CY) * factor
                alpha = factor
            elif t <= t_peak_out:
                zoom = z_max
                cx = target_cx
                cy = target_cy
                alpha = 1.0
            else:
                u = (t - t_peak_out) / max(0.001, t_end - t_peak_out)
                factor = 0.5 * (1.0 + math.cos(math.pi * u))
                zoom = 1.0 + (z_max - 1.0) * factor
                cx = DEFAULT_CX + (target_cx - DEFAULT_CX) * factor
                cy = DEFAULT_CY + (target_cy - DEFAULT_CY) * factor
                alpha = factor
            return zoom, cx, cy, badge_text, active_box, alpha * box_fade
    return 1.0, DEFAULT_CX, DEFAULT_CY, None, None, 0.0


def draw_highlight_box(image: Image.Image, box: list, alpha: float) -> Image.Image:
    """Draw a glowing cyan highlight rectangle around the target UI element."""
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # Outer glow
    for r in range(4, 0, -1):
        a = int(alpha * (90 / r))
        draw.rounded_rectangle([box[0]-r, box[1]-r, box[2]+r, box[3]+r], radius=10, outline=(56, 189, 248, a), width=2)
    # Sharp inner border
    sharp_a = int(alpha * 255)
    draw.rounded_rectangle(box, radius=8, outline=(56, 189, 248, sharp_a), width=2)
    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def main():
    """Main rendering pipeline streaming frames through FFmpeg rawvideo pipe."""
    in_video = "assets/skillbuilderdemo_web.mp4"
    out_video = "assets/skillbuilderdemo_cinematic_web.mp4"

    badges = {text: create_hud_badge(text) for _, _, _, _, _, _, _, text, _, _ in HIGHLIGHTS}

    dec_cmd = [
        "ffmpeg", "-i", in_video,
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
    ]
    p_dec = subprocess.Popen(dec_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    enc_cmd = [
        "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}", "-r", f"{FPS}",
        "-i", "-", "-i", in_video,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-crf", "21", "-preset", "fast",
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart", out_video
    ]
    p_enc = subprocess.Popen(enc_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    frame_bytes = WIDTH * HEIGHT * 3
    frame_idx = 0

    print("Rendering Pixel-Accurate 2.0x Cinematic Zoom, Shifts & Highlight Boxes...", file=sys.stderr)
    try:
        while True:
            raw = p_dec.stdout.read(frame_bytes)
            if len(raw) < frame_bytes:
                break

            t = frame_idx / FPS
            zoom, cx, cy, badge_text, box, alpha = get_camera_state(t)

            frame = Image.frombytes("RGB", (WIDTH, HEIGHT), raw)

            if zoom > 1.002:
                # 1. Draw glowing highlight box on uncropped frame
                if box and alpha > 0.05:
                    frame = draw_highlight_box(frame, box, alpha)

                # 2. Dynamic crop centered on camera position
                w_crop = WIDTH / zoom
                h_crop = HEIGHT / zoom
                x1 = max(0.0, min(WIDTH - w_crop, cx - w_crop / 2.0))
                y1 = max(0.0, min(HEIGHT - h_crop, cy - h_crop / 2.0))
                x2 = x1 + w_crop
                y2 = y1 + h_crop
                frame = frame.crop((int(x1), int(y1), int(x2), int(y2))).resize(
                    (WIDTH, HEIGHT), Image.Resampling.BILINEAR
                )

                # 3. Composite HUD Badge at top center
                if badge_text and alpha > 0.05 and badge_text in badges:
                    badge = badges[badge_text]
                    if alpha < 0.98:
                        badge_layer = badge.copy()
                        r, g, b, a = badge_layer.split()
                        a = a.point(lambda p: int(p * alpha))
                        badge_layer.putalpha(a)
                    else:
                        badge_layer = badge
                    bx = (WIDTH - badge.width) // 2
                    by = 40
                    frame_rgba = frame.convert("RGBA")
                    frame_rgba.paste(badge_layer, (bx, by), badge_layer)
                    frame = frame_rgba.convert("RGB")

            p_enc.stdin.write(frame.tobytes())
            frame_idx += 1

            if frame_idx % 600 == 0:
                print(f"Rendered {frame_idx} frames ({t:.1f}s / 107.4s)...", file=sys.stderr)

    finally:
        p_dec.stdout.close()
        p_dec.wait()
        p_enc.stdin.close()
        p_enc.wait()

    print(f"Finished rendering {frame_idx} frames to {out_video}!", file=sys.stderr)


if __name__ == "__main__":
    main()
