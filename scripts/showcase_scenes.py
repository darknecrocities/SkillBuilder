#!/usr/bin/env python3
"""Scene Renderers for the 12 Chapters of the SkillBuilder Showcase Video.

Renders brutalist/Swiss monochrome backgrounds, technical HUD panels,
architectural wireframes, code snippets, and telemetry meters.
Complies with SkillBuilder cognitive limits (<500 lines).
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from showcase_repo_assets import get_font

W, H = 1920, 1080


def draw_grid_background(draw: ImageDraw.ImageDraw, spacing: int = 60, alpha: int = 25):
    """Draw a subtle precision drafting grid."""
    color = (alpha, alpha, alpha, 255)
    for x in range(0, W, spacing):
        draw.line([(x, 0), (x, H)], fill=color, width=1)
    for y in range(0, H, spacing):
        draw.line([(0, y), (W, y)], fill=color, width=1)


def render_scene_0(t: float) -> Image.Image:
    """Scene 0: Cold Open / System Initialization / Radar Sweep."""
    img = Image.new("RGBA", (W, H), (4, 4, 4, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 80, 20)

    # Rotating radar circle at center
    cx, cy = W // 2, H // 2
    for r in (180, 320, 460):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 40, 40, 255), width=1)

    angle = (t * 2.8) % (2.0 * math.pi)
    rx = cx + math.cos(angle) * 460
    ry = cy + math.sin(angle) * 460
    draw.line([(cx, cy), (rx, ry)], fill=(120, 120, 120, 255), width=1)

    f_hud = get_font(13, mono=True)
    draw.text((cx - 150, cy + 220), "STATUS: INITIALIZING HIGH-PERFORMANCE HARNESS...", font=f_hud, fill=(160, 160, 160, 255))
    draw.text((cx - 110, cy + 245), "CORE MODEL: GEMINI 3.8 FLASH (HIGH)", font=f_hud, fill=(220, 220, 220, 255))
    return img


def render_scene_1(t: float) -> Image.Image:
    """Scene 1: Full-Scale Mode / 5-Stage Lifecycle Flowchart."""
    img = Image.new("RGBA", (W, H), (6, 6, 6, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 60, 22)

    stages = ["1. DISCOVER", "2. PLAN", "3. BUILD", "4. HARNESS", "5. RELEASE"]
    box_w, box_h = 240, 64
    y = H // 2 + 180
    total_w = len(stages) * box_w + (len(stages) - 1) * 60
    start_x = (W - total_w) // 2
    f_box = get_font(14, mono=True)

    for i, name in enumerate(stages):
        x = start_x + i * (box_w + 60)
        # Active pulse
        is_active = (int(t * 2.5) % len(stages)) == i
        fill_col = (40, 40, 40, 255) if is_active else (16, 16, 16, 255)
        border_col = (255, 255, 255, 255) if is_active else (70, 70, 70, 255)
        draw.rectangle([x, y, x + box_w, y + box_h], fill=fill_col, outline=border_col, width=1)
        draw.text((x + 35, y + 24), name, font=f_box, fill=(240, 240, 240, 255))
        # Arrow
        if i < len(stages) - 1:
            arr_x = x + box_w + 15
            draw.line([(arr_x, y + 32), (arr_x + 30, y + 32)], fill=(120, 120, 120, 255), width=2)

    return img


def render_scene_2(t: float) -> Image.Image:
    """Scene 2: 36 Modular Skills Ecosystem Matrix."""
    img = Image.new("RGBA", (W, H), (5, 5, 5, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 50, 18)

    sample_skills = [
        "prompt-polish", "anti-slop", "ui", "mobile-ui", "web-ui", "3d",
        "frontend", "routing", "state-management", "i18n", "backend", "fullstack",
        "api-design", "database", "gcp", "aws", "firebase", "supabase",
        "data-pipelines", "devops", "security", "ai", "local-llm", "research",
        "antigravity-automation", "testing", "qa", "performance", "observability", "refactor"
    ]
    cols = 6
    cw, ch = 240, 38
    sx = (W - (cols * cw + (cols - 1) * 20)) // 2
    sy = H // 2 + 100
    f_sk = get_font(12, mono=True)

    for idx, skill in enumerate(sample_skills):
        r = idx // cols
        c = idx % cols
        x = sx + c * (cw + 20)
        y = sy + r * (ch + 14)
        if y + ch > H - 60:
            break
        pulse = (int(t * 8 + idx) % 11) == 0
        border = (200, 200, 200, 255) if pulse else (45, 45, 45, 255)
        draw.rectangle([x, y, x + cw, y + ch], fill=(14, 14, 14, 255), outline=border, width=1)
        draw.text((x + 16, y + 12), f"/{skill}", font=f_sk, fill=(210, 210, 210, 255))

    return img


def render_scene_3(t: float) -> Image.Image:
    """Scene 3: Prompt Polishing & Token Optimization Spec."""
    img = Image.new("RGBA", (W, H), (6, 6, 6, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 60, 20)

    # Two comparison cards
    cw, ch = 680, 240
    y = H // 2 + 130
    draw.rectangle([200, y, 200 + cw, y + ch], fill=(12, 12, 12, 255), outline=(60, 60, 60, 255), width=1)
    draw.rectangle([W - 200 - cw, y, W - 200, y + ch], fill=(18, 18, 18, 255), outline=(220, 220, 220, 255), width=1)

    f_h = get_font(14, mono=True)
    f_b = get_font(12, mono=True)
    draw.text((220, y + 20), "BEFORE: AMBIGUOUS PROMPT [UNSTRUCTURED]", font=f_h, fill=(140, 140, 140, 255))
    draw.text((220, y + 60), "> 'make a fast backend with auth and database...'", font=f_b, fill=(100, 100, 100, 255))

    draw.text((W - 180 - cw, y + 20), "AFTER: PPE RFC SPECIFICATION [TOKEN OPTIMIZED]", font=f_h, fill=(255, 255, 255, 255))
    draw.text((W - 180 - cw, y + 60), "✓ RFC 7807 Problem Details  ✓ Constant-time HMAC", font=f_b, fill=(220, 220, 220, 255))
    draw.text((W - 180 - cw, y + 90), "✓ Token Family Rotation     ✓ SSRF Post-DNS Guard", font=f_b, fill=(220, 220, 220, 255))
    draw.text((W - 180 - cw, y + 140), "TOKEN SAVINGS: ~1,850 TOKENS PER TURN", font=f_h, fill=(240, 240, 240, 255))
    return img


def render_scene_4(t: float) -> Image.Image:
    """Scene 4: Anti-AI-Slop Discipline / Zero Mocks."""
    img = Image.new("RGBA", (W, H), (5, 5, 5, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 70, 20)

    # 4 discipline blocks
    blocks = [
        ("[X] PROHIBITED", "Decorative Shields & Neon Gradients", False),
        ("[X] PROHIBITED", "Static Toy Mock Arrays Pretending to be DBs", False),
        ("[✓] ENFORCED", "Real SQLite & PostgreSQL ACID Persistence", True),
        ("[✓] ENFORCED", "Content-Hashed SHA-256 Single-Slot Backups", True),
    ]
    y = H // 2 + 110
    f_t = get_font(13, mono=True)
    f_d = get_font(15, mono=True)

    for i, (tag, desc, ok) in enumerate(blocks):
        bx = 220 + (i % 2) * 760
        by = y + (i // 2) * 110
        border = (220, 220, 220, 255) if ok else (80, 80, 80, 255)
        draw.rectangle([bx, by, bx + 700, by + 85], fill=(14, 14, 14, 255), outline=border, width=1)
        tag_col = (255, 255, 255, 255) if ok else (140, 140, 140, 255)
        draw.text((bx + 25, by + 18), tag, font=f_t, fill=tag_col)
        draw.text((bx + 25, by + 45), desc, font=f_d, fill=(230, 230, 230, 255))

    return img


def render_scene_5(t: float) -> Image.Image:
    """Scene 5: Precision Swiss UI / Apple HIG / Sub-Pixel Lighting."""
    img = Image.new("RGBA", (W, H), (6, 6, 6, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 60, 22)

    # Glassmorphic card wireframe
    cx, cy = W // 2, H // 2 + 200
    cw, ch = 900, 180
    draw.rectangle([cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2], fill=(15, 15, 15, 255), outline=(100, 100, 100, 255), width=1)
    # Sub-pixel highlight line at top of card
    draw.line([(cx - cw // 2 + 1, cy - ch // 2 + 1), (cx + cw // 2 - 1, cy - ch // 2 + 1)], fill=(255, 255, 255, 255), width=1)

    f_sub = get_font(13, mono=True)
    draw.text((cx - cw // 2 + 40, cy - 40), "SPEC: APPLE HIG 18/19  |  SINGLE-ZENITH 90° SPECULAR REFLECTION", font=f_sub, fill=(240, 240, 240, 255))
    draw.text((cx - cw // 2 + 40, cy - 10), "RESPONSIVENESS: 4-TIER MATRIX (375px, 768px, 1280px, 1920px+)", font=f_sub, fill=(180, 180, 180, 255))
    draw.text((cx - cw // 2 + 40, cy + 20), "COMPOSITOR: 120Hz PROMOTION BUDGET (<= 8.33ms FRAME BUDGET)", font=f_sub, fill=(180, 180, 180, 255))
    return img


def render_scene_6(t: float) -> Image.Image:
    """Scene 6: Resilient Backend Architecture & OWASP Defense."""
    img = Image.new("RGBA", (W, H), (5, 5, 5, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 50, 18)

    f_m = get_font(13, mono=True)
    y = H // 2 + 120
    draw.rectangle([280, y, W - 280, y + 200], fill=(12, 12, 12, 255), outline=(80, 80, 80, 255), width=1)
    draw.text((320, y + 25), "HEXAGONAL ARCHITECTURE // DOMAIN CORE & ADAPTERS", font=f_m, fill=(255, 255, 255, 255))
    draw.text((320, y + 65), "• Containerization: Multi-stage Dockerfile with non-root USER 10001", font=f_m, fill=(200, 200, 200, 255))
    draw.text((320, y + 95), "• Network Resilience: Explicit 3s connection / 15s read timeouts & jitter", font=f_m, fill=(200, 200, 200, 255))
    draw.text((320, y + 125), "• Security: Tenant-scoped queries, token bucket rate limits, SSRF validation", font=f_m, fill=(200, 200, 200, 255))
    draw.text((320, y + 155), "• Deduplicated Storage: SHA-256 digest lock via backup_manifest.json", font=f_m, fill=(200, 200, 200, 255))
    return img


def render_scene_7(t: float) -> Image.Image:
    """Scene 7: 5-Tier Evaluation Harness Status Dashboard."""
    img = Image.new("RGBA", (W, H), (5, 5, 5, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 60, 20)

    tiers = [
        ("TIER 1", "Static Hygiene & Cognitive Limits", "PASS"),
        ("TIER 2", "API Contracts & RFC 7807 Errors", "PASS"),
        ("TIER 3", "TDD Automated Test Suites", "PASS"),
        ("TIER 4", "OWASP Security Hardening", "PASS"),
        ("TIER 5", "Git Workflow & 1000-Line Budget", "PASS"),
    ]
    y = H // 2 + 80
    f_t = get_font(13, mono=True)
    f_res = get_font(14, mono=True)

    for i, (t_num, desc, res) in enumerate(tiers):
        by = y + i * 46
        draw.rectangle([340, by, W - 340, by + 36], fill=(14, 14, 14, 255), outline=(55, 55, 55, 255), width=1)
        draw.text((360, by + 10), t_num, font=f_t, fill=(160, 160, 160, 255))
        draw.text((460, by + 10), desc, font=f_t, fill=(230, 230, 230, 255))
        draw.text((W - 440, by + 9), f"[ {res} ]", font=f_res, fill=(255, 255, 255, 255))

    return img


def render_scene_8(t: float) -> Image.Image:
    """Scene 8: Multi-Tier Code Quality / 500-Line Physical Limit."""
    img = Image.new("RGBA", (W, H), (6, 6, 6, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 50, 20)

    y = H // 2 + 110
    draw.rectangle([300, y, W - 300, y + 210], fill=(10, 10, 10, 255), outline=(90, 90, 90, 255), width=1)
    f_c = get_font(13, mono=True)
    draw.text((330, y + 20), "$ python3 check_source_line_limits.py --show-tiers", font=f_c, fill=(180, 180, 180, 255))
    draw.text((330, y + 55), "Scanned 126 source file(s) across SkillBuilder repository", font=f_c, fill=(220, 220, 220, 255))
    draw.text((330, y + 85), "• Sweet Spot  (<= 250 lines) : 113 file(s)", font=f_c, fill=(255, 255, 255, 255))
    draw.text((330, y + 115), "• Nominal     (251-350 lines): 9 file(s)", font=f_c, fill=(200, 200, 200, 255))
    draw.text((330, y + 145), "• Violations  (> 500 lines)  : 0 file(s)  [100% COMPLIANT]", font=f_c, fill=(255, 255, 255, 255))
    draw.text((330, y + 175), "MAX FUNCTION LINES: <= 40  |  CYCLOMATIC COMPLEXITY: <= 10", font=f_c, fill=(160, 160, 160, 255))
    return img


def render_scene_9(t: float) -> Image.Image:
    """Scene 9: Antigravity Automation & Multi-Agent Sidecars."""
    img = Image.new("RGBA", (W, H), (5, 5, 5, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 60, 20)

    y = H // 2 + 120
    draw.rectangle([260, y, W - 260, y + 190], fill=(12, 12, 12, 255), outline=(70, 70, 70, 255), width=1)
    f_a = get_font(13, mono=True)
    draw.text((300, y + 25), "GOOGLE ANTIGRAVITY AUTOMATION ENGINE // ZERO-POLLING EVENT BUS", font=f_a, fill=(255, 255, 255, 255))
    draw.text((300, y + 65), "• Scheduled Sidecars: ~/.gemini/jetski/sidecars/<slug>/sidecar.json", font=f_a, fill=(200, 200, 200, 255))
    draw.text((300, y + 95), "• Reactive Wakeup: Native schedule tool timers, zero sleep polling", font=f_a, fill=(200, 200, 200, 255))
    draw.text((300, y + 125), "• Multi-Agent Synchronized Coordination via Shared Lease Locks", font=f_a, fill=(200, 200, 200, 255))
    draw.text((300, y + 155), "• Plugin Lifecycle Hooks: PreToolUse, PostToolUse, SessionStart", font=f_a, fill=(180, 180, 180, 255))
    return img


def render_scene_10(t: float) -> Image.Image:
    """Scene 10: Verified Production Release & PR Ready."""
    img = Image.new("RGBA", (W, H), (6, 6, 6, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 50, 22)

    y = H // 2 + 110
    draw.rectangle([280, y, W - 280, y + 200], fill=(14, 14, 14, 255), outline=(200, 200, 200, 255), width=1)
    f_p = get_font(13, mono=True)
    draw.text((320, y + 25), "GIT COMMIT & PULL REQUEST // READY TO MERGE", font=f_p, fill=(255, 255, 255, 255))
    draw.text((320, y + 65), "commit 7f3a9e2  feat(orchestration): unify 36 skills in full-scale mode", font=f_p, fill=(220, 220, 220, 255))
    draw.text((320, y + 95), "Why: Deliver apex autonomous engineering pipeline with zero regression", font=f_p, fill=(180, 180, 180, 255))
    draw.text((320, y + 125), "What: 5-Stage Lifecycle, Evaluation Harness, Deduplicated Storage Locks", font=f_p, fill=(180, 180, 180, 255))
    draw.text((320, y + 155), "Verification: 5/5 Harness Tiers PASS | Line limits 100% verified", font=f_p, fill=(255, 255, 255, 255))
    return img


def render_scene_11(t: float) -> Image.Image:
    """Scene 11: Grand Finale Monolith Emblem."""
    img = Image.new("RGBA", (W, H), (4, 4, 4, 255))
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, 80, 25)

    cx, cy = W // 2, H // 2
    # Monolithic geometric emblem
    for r in (220, 340, 480):
        draw.rectangle([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=(50, 50, 50, 255), width=1)

    f_fin = get_font(16, mono=True)
    draw.text((cx - 240, cy + 240), "THE APEX MULTI-AGENT ENGINEERING HARNESS", font=f_fin, fill=(255, 255, 255, 255))
    draw.text((cx - 180, cy + 270), "BUILT WITH GOOGLE DEEPMIND & GEMINI 3.8", font=f_fin, fill=(180, 180, 180, 255))
    return img


SCENE_RENDERERS = [
    render_scene_0, render_scene_1, render_scene_2, render_scene_3,
    render_scene_4, render_scene_5, render_scene_6, render_scene_7,
    render_scene_8, render_scene_9, render_scene_10, render_scene_11,
]


def render_scene_background(scene_idx: int, t: float) -> Image.Image:
    """Dispatch to the dedicated scene background renderer."""
    idx = max(0, min(len(SCENE_RENDERERS) - 1, scene_idx))
    return SCENE_RENDERERS[idx](t)


if __name__ == "__main__":
    im = render_scene_background(0, 1.0)
    print(f"[OK] Scene renderer ready. Rendered size: {im.size}")
