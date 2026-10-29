#!/usr/bin/env python3
"""Master Director & Video Compositor for the SkillBuilder Product Marketing Film.

Executes Swiss Grid & Kinetic Type motion graphics inspired by Awesome Claude:
- Pure text-only, high-contrast monochrome (#000000 and #FFFFFF)
- 11 distinct kinetic typography techniques across 11 timed marketing shots
- Zero AI cliché tropes (no '//' comment markers, no fake badges, no particle dust)
- Non-overlapping, emotional male voiceover with -5dB sidechain music ducking
- Streams 1080p RGB24 frames into FFmpeg with synchronized 48kHz stereo AAC audio.
Complies strictly with SkillBuilder cognitive limits (<500 lines).
"""

import os
import subprocess
import sys
import time
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from showcase_audio_synth import generate_soundtrack
from showcase_camera_engine import get_camera_state, apply_camera_transform
from showcase_repo_assets import render_telemetry_hud
from showcase_swiss_engine import render_swiss_frame
from showcase_transitions import apply_transition

W, H = 1920, 1080
FPS = 30
DURATION = 46.0
TOTAL_FRAMES = int(FPS * DURATION)

SHOT_TIMESTAMPS = [
    (0.00, 3.75, "01 WHAT IF PROMPTING"),
    (3.75, 7.60, "02 ZERO MOCK SLOP"),
    (7.60, 11.40, "03 SENIOR DISCIPLINE"),
    (11.40, 15.30, "04 ENTER SKILLBUILDER"),
    (15.30, 19.40, "05 FULL-SCALE ARCHITECTURE"),
    (19.40, 23.80, "06 REAL PERSISTENCE"),
    (23.80, 27.60, "07 SOURCE LINE CEILING"),
    (27.60, 31.80, "08 5-TIER VERIFICATION"),
    (31.80, 35.80, "09 AGENTIC AUTOMATION"),
    (35.80, 40.00, "10 CONVENTIONAL COMMITS"),
    (40.00, 46.00, "11 SKILLBUILDER APEX"),
]


def render_shot_composite(shot_idx: int, t: float, cx: float = 960.0, cy: float = 540.0, zoom: float = 1.0) -> np.ndarray:
    """Render a pure high-contrast Swiss kinetic typography frame with tight zoom & word tracking."""
    t_start, t_end, _ = SHOT_TIMESTAMPS[shot_idx]
    dur = max(0.001, t_end - t_start)
    rel_t = max(0.0, min(dur, t - t_start))

    # Render Swiss typography frame natively shifted and scaled by camera
    frame_pil = render_swiss_frame(shot_idx, rel_t, dur, cx, cy, zoom)
    return np.array(frame_pil.convert("L"))


def main():
    """Execute full rendering loop streaming to FFmpeg with synchronized audio."""
    os.makedirs("assets", exist_ok=True)
    audio_wav = "assets/showcase_soundtrack.wav"
    output_mp4 = "assets/skillbuilder_showcase_cinematic.mp4"

    # Verify soundtrack exists
    if not os.path.exists(audio_wav):
        generate_soundtrack(audio_wav)

    print(f"[DIRECTOR] Starting Swiss Kinetic Marketing Video render: {TOTAL_FRAMES} frames @ {FPS} FPS...")
    t_start_render = time.time()

    # Launch FFmpeg streaming process
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",  # Video pipe from stdin
        "-i", audio_wav,  # Audio master
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "16",  # High quality, razor-sharp vector type
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        output_mp4
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    transition_dur = 0.45  # 450ms smooth continuous transition

    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / float(FPS)

        # Locate active shot
        active_idx = 0
        for i, (t0, t1, _) in enumerate(SHOT_TIMESTAMPS):
            if t0 <= t < t1:
                active_idx = i
                break
            if t >= SHOT_TIMESTAMPS[-1][1]:
                active_idx = len(SHOT_TIMESTAMPS) - 1

        t0, t1, tag = SHOT_TIMESTAMPS[active_idx]
        t_to_end = t1 - t

        # Compute smooth quintic camera focus coordinates
        cam_zoom, cam_cx, cam_cy, cam_roll = get_camera_state(t, active_idx, t0, t1)

        # Render active shot plate with smooth focal position and deep zoom
        frame_a = render_shot_composite(active_idx, t, cam_cx, cam_cy, cam_zoom)

        # Apply dedicated smooth transition in transition window
        if t_to_end < transition_dur and active_idx < len(SHOT_TIMESTAMPS) - 1:
            next_idx = active_idx + 1
            next_t0, next_t1, _ = SHOT_TIMESTAMPS[next_idx]
            next_zoom, next_cx, next_cy, _ = get_camera_state(t, next_idx, next_t0, next_t1)
            p_trans = (transition_dur - t_to_end) / transition_dur
            frame_b = render_shot_composite(next_idx, t, next_cx, next_cy, next_zoom)
            final_gray = apply_transition(active_idx, frame_a, frame_b, p_trans)
        else:
            final_gray = frame_a

        # Convert to 3-channel RGB24
        final_rgb = np.repeat(final_gray[:, :, None], 3, axis=2)

        # Composite clean HUD telemetry overlay
        hud_img = render_telemetry_hud(t, frame_idx, tag)
        hud_np = np.array(hud_img)
        hud_alpha = hud_np[:, :, 3] / 255.0
        for c in range(3):
            final_rgb[:, :, c] = np.clip(
                final_rgb[:, :, c] * (1.0 - hud_alpha) + hud_np[:, :, c] * hud_alpha,
                0, 255
            ).astype(np.uint8)

        # Stream raw RGB24 frame into FFmpeg stdin
        proc.stdin.write(final_rgb.tobytes())

        if frame_idx % 90 == 0 or frame_idx == TOTAL_FRAMES - 1:
            elapsed = time.time() - t_start_render
            fps_render = (frame_idx + 1) / max(0.001, elapsed)
            print(f"  -> Rendered {frame_idx + 1}/{TOTAL_FRAMES} frames ({fps_render:.1f} fps) | t={t:.1f}s")

    proc.stdin.close()
    stderr_out = proc.stderr.read().decode("utf-8")
    proc.wait()

    if proc.returncode != 0:
        print(f"[ERROR] FFmpeg failed with exit code {proc.returncode}:\n{stderr_out}", file=sys.stderr)
        sys.exit(proc.returncode)

    total_time = time.time() - t_start_render
    file_size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"\n[SUCCESS] Rendered Swiss Kinetic Marketing Video to {output_mp4} ({file_size_mb:.2f} MB in {total_time:.1f}s)")


if __name__ == "__main__":
    main()
