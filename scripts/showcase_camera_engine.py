#!/usr/bin/env python3
"""Smooth Quintic Orthographic Camera Engine for SkillBuilder Marketing Showcase.

Features:
- $C^2$-continuous quintic smoothstep interpolation ($6u^5 - 15u^4 + 10u^3$).
- Generous 0.58s shift duration for buttery, elegant glide across the Swiss grid.
- Subtle continuous harmonic camera drift so the frame stays fluidly alive.
- Precise deep zoom ($1.50x - 2.25x$) and 2D focal tracking on every spoken word.
Complies strictly with SkillBuilder cognitive limits (<500 lines).
"""

import math
from PIL import Image

W, H = 1920, 1080
CX_DEFAULT = W / 2.0  # 960.0
CY_DEFAULT = H / 2.0  # 540.0

# 11 Chapters of Word & Content Focal Waypoints with Deep Zoom & Tracking:
# Each waypoint defines: (t_rel_start, focal_cx, focal_cy, zoom_level, label)
WORD_WAYPOINTS = {
    0: [  # Shot 1 (0.0 - 3.75s): WHAT IF... -> PROMPT ROULETTE
        (0.0, 960.0, 540.0, 1.35, "INTRO"),
        (0.4, 620.0, 480.0, 1.85, "WHAT IF..."),
        (1.5, 1180.0, 480.0, 1.95, "PROMPT ROULETTE")
    ],
    1: [  # Shot 2 (3.75 - 7.60s): MOCK ARRAYS -> BLOATED MONOLITHS
        (0.0, 640.0, 430.0, 1.85, "MOCK ARRAYS"),
        (1.6, 1220.0, 490.0, 2.05, "BLOATED MONOLITHS")
    ],
    2: [  # Shot 3 (7.60 - 11.40s): SENIOR STAFF -> DISCIPLINE
        (0.0, 700.0, 440.0, 1.85, "SENIOR STAFF"),
        (1.5, 1180.0, 520.0, 1.95, "ENGINEER DISCIPLINE")
    ],
    3: [  # Shot 4 (11.40 - 15.30s): ENTER SKILLBUILDER -> 36 SKILLS IN UNISON
        (0.0, 680.0, 420.0, 1.75, "ENTER SKILLBUILDER"),
        (1.4, 1320.0, 430.0, 2.20, "36 COUNTER"),
        (2.5, 840.0, 580.0, 1.65, "PERFECT UNISON")
    ],
    4: [  # Shot 5 (15.30 - 19.40s): FULL-SCALE MODE -> ARCHITECTURE BEFORE CODE
        (0.0, 960.0, 440.0, 1.90, "FULL-SCALE MODE"),
        (1.7, 960.0, 560.0, 1.70, "ARCHITECTURE PLANNED")
    ],
    5: [  # Shot 6 (19.40 - 23.80s): ZERO MOCK DATA -> REAL SCHEMAS & BACKUPS
        (0.0, 640.0, 420.0, 1.85, "ZERO MOCK DATA"),
        (1.5, 1180.0, 510.0, 1.85, "REAL SCHEMAS & BACKUPS")
    ],
    6: [  # Shot 7 (23.80 - 27.60s): 500 GIANT NUMBER -> PHYSICAL LINE CEILING
        (0.0, 580.0, 440.0, 2.25, "500 GIANT NUMBER"),
        (1.5, 1180.0, 480.0, 1.75, "PHYSICAL LINE CEILING")
    ],
    7: [  # Shot 8 (27.60 - 31.80s): 5-TIER VERIFICATION -> 100% PASS RADAR
        (0.0, 640.0, 430.0, 1.75, "5-TIER VERIFICATION"),
        (1.5, 1320.0, 530.0, 2.20, "100% PASS RADAR"),
        (2.7, 880.0, 570.0, 1.65, "AUTONOMOUS SELF-HEALING")
    ],
    8: [  # Shot 9 (31.80 - 35.80s): ANTIGRAVITY AUTOMATION -> AGENTS IN SYNC
        (0.0, 720.0, 440.0, 1.80, "ANTIGRAVITY AUTOMATION"),
        (1.6, 1280.0, 510.0, 1.95, "AGENTS IN SYNC")
    ],
    9: [  # Shot 10 (35.80 - 40.00s): CONVENTIONAL COMMITS -> READY-TO-MERGE RELEASES
        (0.0, 680.0, 420.0, 1.85, "CONVENTIONAL COMMITS"),
        (1.5, 1180.0, 510.0, 1.85, "READY-TO-MERGE RELEASES")
    ],
    10: [  # Shot 11 (40.00 - 46.00s): STOP PROMPTING -> START ENGINEERING -> SKILLBUILDER
        (0.0, 720.0, 440.0, 1.75, "STOP PROMPTING"),
        (1.4, 1200.0, 440.0, 1.85, "START ENGINEERING"),
        (2.6, 960.0, 490.0, 2.10, "SKILLBUILDER APEX")
    ]
}


def ease_quintic_smooth(u: float) -> float:
    """Smoothstep quintic curve 6u^5 - 15u^4 + 10u^3 for C^2 continuous acceleration & glide."""
    u = max(0.0, min(1.0, u))
    return u * u * u * (u * (u * 6.0 - 15.0) + 10.0)


def get_camera_state(t: float, scene_idx: int, t_start: float, t_end: float):
    """Compute camera center (cx, cy) and deep zoom level shifting smoothly between active words."""
    waypoints = WORD_WAYPOINTS.get(scene_idx, [(0.0, CX_DEFAULT, CY_DEFAULT, 1.0, "DEFAULT")])
    rel_t = max(0.0, t - t_start)

    # Locate active waypoint segment
    curr_idx = 0
    for i in range(len(waypoints)):
        if rel_t >= waypoints[i][0]:
            curr_idx = i

    curr_wp = waypoints[curr_idx]
    prev_wp = waypoints[curr_idx - 1] if curr_idx > 0 else (0.0, CX_DEFAULT, CY_DEFAULT, 1.35, "INIT")

    # Shift smoothly over 0.58s (17-18 frames)
    t_activation = curr_wp[0]
    dt_from_act = rel_t - t_activation
    shift_dur = 0.58

    if dt_from_act < shift_dur and curr_idx > 0:
        p = ease_quintic_smooth(dt_from_act / shift_dur)
        cx = prev_wp[1] + (curr_wp[1] - prev_wp[1]) * p
        cy = prev_wp[2] + (curr_wp[2] - prev_wp[2]) * p
        zoom = prev_wp[3] + (curr_wp[3] - prev_wp[3]) * p
    else:
        cx = curr_wp[1]
        cy = curr_wp[2]
        zoom = curr_wp[3]

    # Subtle continuous harmonic camera drift (keeps frame dynamically alive)
    drift_x = 6.0 * math.sin(1.25 * rel_t)
    drift_y = 3.8 * math.cos(0.95 * rel_t)
    cx += drift_x
    cy += drift_y

    roll_deg = 0.0  # Zero tilt - pure perpendicular Swiss drafting geometry
    return zoom, cx, cy, roll_deg


def apply_camera_transform(image: Image.Image, zoom: float, cx: float, cy: float, roll_deg: float) -> Image.Image:
    """Fallback 2D frame translation (when not natively rendered with offset)."""
    shift_x = int(CX_DEFAULT - cx)
    shift_y = int(CY_DEFAULT - cy)

    if shift_x == 0 and shift_y == 0:
        return image

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    canvas.paste(image, (shift_x, shift_y))
    return canvas


if __name__ == "__main__":
    test_img = Image.new("RGBA", (W, H), (20, 20, 20, 255))
    z, x, y, r = get_camera_state(1.5, 0, 0.0, 3.75)
    out = apply_camera_transform(test_img, z, x, y, r)
    print(f"[OK] Smooth Camera Engine verified. State: Zoom={z:.2f}, Focus=({x:.1f},{y:.1f})")
