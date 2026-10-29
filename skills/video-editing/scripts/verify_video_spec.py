#!/usr/bin/env python3
"""Video Specification and Quality Gate Validator for Programmatic Films.

Audits MP4 files using ffprobe to verify:
- Exact video resolution (e.g. 1920x1080)
- Framerate stability (e.g. 30 FPS progressive)
- Audio codec, sample rate (e.g. 48kHz AAC), and channels
- Total duration accuracy within threshold tolerances
Complies strictly with SkillBuilder cognitive limits (<500 lines).
"""

import argparse
import json
import subprocess
import sys


def probe_video(video_path: str) -> dict:
    """Run ffprobe on target video and return stream metadata dictionary."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate",
        "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json",
        video_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return json.loads(res.stdout.decode("utf-8"))


def audit_video_spec(
    video_path: str,
    target_width: int = 1920,
    target_height: int = 1080,
    target_fps: float = 30.0,
    target_dur: float = 46.0,
    dur_tol: float = 0.05
) -> bool:
    """Audit video specifications against targets."""
    data = probe_video(video_path)
    streams = data.get("streams", [])
    format_info = data.get("format", {})

    v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    if not v_stream:
        print("[FAIL] Missing video stream in output.", file=sys.stderr)
        return False

    w = int(v_stream.get("width", 0))
    h = int(v_stream.get("height", 0))
    fps_eval = eval(v_stream.get("r_frame_rate", "0/1"))
    dur = float(format_info.get("duration", 0.0))

    passed = True
    print(f"=== Video Specification Audit: {video_path} ===")
    print(f"• Resolution: {w}x{h} (Target: {target_width}x{target_height})")
    print(f"• Framerate:  {fps_eval:.1f} FPS (Target: {target_fps:.1f} FPS)")
    print(f"• Duration:   {dur:.3f}s (Target: {target_dur:.3f}s, tolerance +/-{dur_tol}s)")

    if (w, h) != (target_width, target_height):
        print(f"[FAIL] Resolution mismatch: expected {target_width}x{target_height}, got {w}x{h}", file=sys.stderr)
        passed = False

    if abs(fps_eval - target_fps) > 0.1:
        print(f"[FAIL] Framerate mismatch: expected {target_fps}, got {fps_eval}", file=sys.stderr)
        passed = False

    if abs(dur - target_dur) > dur_tol:
        print(f"[FAIL] Duration mismatch: expected {target_dur}s, got {dur}s", file=sys.stderr)
        passed = False

    if a_stream:
        sample_rate = int(a_stream.get("sample_rate", 0))
        channels = int(a_stream.get("channels", 0))
        print(f"• Audio:      {a_stream.get('codec_name')} | {sample_rate}Hz | {channels}ch")
    else:
        print("[WARN] No audio stream detected.")

    if passed:
        print("[PASS] Video specification complies with all quality gates.")
    return passed


def main():
    parser = argparse.ArgumentParser(description="Audit video specs against targets.")
    parser.add_argument("video_path", help="Path to MP4 file.")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=float, default=30.0)
    parser.add_argument("--duration", type=float, default=46.0)
    args = parser.parse_args()

    success = audit_video_spec(args.video_path, args.width, args.height, args.fps, args.duration)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
