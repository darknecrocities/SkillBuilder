#!/usr/bin/env python3
"""Generates High-Contrast Monochrome Repository Plates and UI Panels.

Reads real files from the SkillBuilder repository and renders pixel-perfect
monochrome editor windows, terminal telemetry, and architecture wireframes
to be composited into the showcase video scenes.
Complies with SkillBuilder cognitive limits (<500 lines).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080


def get_font(size: int, mono: bool = True) -> ImageFont.FreeTypeFont:
    """Load standard macOS system fonts with fallback."""
    font_path = "/System/Library/Fonts/SFNSMono.ttf" if mono else "/System/Library/Fonts/Helvetica.ttc"
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
        except OSError:
            return ImageFont.load_default()


def render_code_window(title: str, lines: list, width: int = 1400, height: int = 700) -> Image.Image:
    """Render an ultra-clean brutalist/Swiss monochrome code editor window."""
    img = Image.new("RGBA", (width, height), (10, 10, 10, 240))
    draw = ImageDraw.Draw(img)

    # Outer border and titlebar
    draw.rectangle([0, 0, width - 1, height - 1], outline=(60, 60, 60, 255), width=1)
    draw.rectangle([0, 0, width - 1, 40], fill=(22, 22, 22, 255))
    draw.line([0, 40, width - 1, 40], fill=(60, 60, 60, 255), width=1)

    # Window control dots (monochrome shades)
    draw.ellipse([14, 14, 26, 26], fill=(70, 70, 70, 255))
    draw.ellipse([34, 14, 46, 26], fill=(90, 90, 90, 255))
    draw.ellipse([54, 14, 66, 26], fill=(120, 120, 120, 255))

    # Title label
    f_title = get_font(13, mono=True)
    draw.text((84, 12), title, font=f_title, fill=(200, 200, 200, 255))

    # Code body with line numbers
    f_code = get_font(14, mono=True)
    y_offset = 58
    for i, line in enumerate(lines[:28]):
        line_num = f"{i + 1:3d}  "
        draw.text((20, y_offset), line_num, font=f_code, fill=(80, 80, 80, 255))
        # Keyword highlighting in shades of white and gray
        color = (255, 255, 255, 255)
        if line.strip().startswith(("#", "//", "/*", "*")):
            color = (130, 130, 130, 255)
        elif any(k in line for k in ("def ", "class ", "import ", "from ", "export ", "async ")):
            color = (240, 240, 240, 255)
        draw.text((70, y_offset), line[:110], font=f_code, fill=color)
        y_offset += 22

    return img


def render_terminal_panel(title: str, logs: list, width: int = 1200, height: int = 500) -> Image.Image:
    """Render a high-tech terminal output plate with green/white monochrome indicators."""
    img = Image.new("RGBA", (width, height), (5, 5, 5, 245))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width - 1, height - 1], outline=(50, 50, 50, 255), width=1)
    draw.rectangle([0, 0, width - 1, 32], fill=(18, 18, 18, 255))
    f_head = get_font(12, mono=True)
    draw.text((16, 8), f"TERMINAL // {title}", font=f_head, fill=(180, 180, 180, 255))

    f_log = get_font(13, mono=True)
    y = 48
    for line in logs[:18]:
        color = (255, 255, 255, 255)
        if "[PASS]" in line or "[OK]" in line:
            color = (230, 230, 230, 255)
        elif "[WARN]" in line:
            color = (180, 180, 180, 255)
        elif "[ERROR]" in line:
            color = (255, 255, 255, 255)
        draw.text((24, y), line[:95], font=f_log, fill=color)
        y += 24

    return img


def render_telemetry_hud(t: float, frame_idx: int, scene_name: str) -> Image.Image:
    """Render an edge HUD overlay with timecodes, frame counters, and targeting reticles."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    f_mono = get_font(12, mono=True)

    # Corner framing brackets
    m, l = 40, 30
    draw.line([(m, m), (m + l, m)], fill=(120, 120, 120, 255), width=1)
    draw.line([(m, m), (m, m + l)], fill=(120, 120, 120, 255), width=1)
    draw.line([(W - m, m), (W - m - l, m)], fill=(120, 120, 120, 255), width=1)
    draw.line([(W - m, m), (W - m, m + l)], fill=(120, 120, 120, 255), width=1)
    draw.line([(m, H - m), (m + l, H - m)], fill=(120, 120, 120, 255), width=1)
    draw.line([(m, H - m), (m, H - m - l)], fill=(120, 120, 120, 255), width=1)
    draw.line([(W - m, H - m), (W - m - l, H - m)], fill=(120, 120, 120, 255), width=1)
    draw.line([(W - m, H - m), (W - m, H - m - l)], fill=(120, 120, 120, 255), width=1)

    # Top Telemetry Bar
    timecode = f"SKILLBUILDER • {int(t // 60):02d}:{int(t % 60):02d}:{int((t * 30) % 30):02d} • FRAME {frame_idx:05d} • 30 FPS"
    draw.text((m + 40, m - 5), timecode, font=f_mono, fill=(220, 220, 220, 255))
    sys_status = f"PRODUCT SPECIFICATION • STAGE: {scene_name}"
    draw.text((W - m - 460, m - 5), sys_status, font=f_mono, fill=(180, 180, 180, 255))

    # Bottom Telemetry Bar
    repo_tag = "SKILLBUILDER AGENTIC HARNESS • 36 MODULAR SKILLS"
    draw.text((m + 40, H - m - 12), repo_tag, font=f_mono, fill=(150, 150, 150, 255))
    metrics_tag = "5-TIER VERIFICATION PASS • 500-LINE SOURCE LIMIT"
    draw.text((W - m - 490, H - m - 12), metrics_tag, font=f_mono, fill=(150, 150, 150, 255))

    # Subtle crosshairs at center screen edges
    draw.line([(W // 2 - 15, H // 2), (W // 2 + 15, H // 2)], fill=(50, 50, 50, 255), width=1)
    draw.line([(W // 2, H // 2 - 15), (W // 2, H // 2 + 15)], fill=(50, 50, 50, 255), width=1)

    return overlay


if __name__ == "__main__":
    print("[OK] showcase_repo_assets ready.")
