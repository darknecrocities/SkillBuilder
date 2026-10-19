# Premium Color Science & Atmospheric Materiality

Architectural standards for color palettes, depth perception, and surface materiality. Replaces muddy sRGB grays and rainbow gradients with modern OKLCH color spaces, hairline dividers, and atmospheric illumination.

---

## 1. Why OKLCH Over sRGB and HSL

Standard sRGB and HSL color models suffer from non-uniform perceived lightness: pure yellow at lightness 50% appears blindingly bright, while pure blue at lightness 50% appears dark and muddy.

**OKLCH (Oklab Lightness, Chroma, Hue)** provides:
1. **Perceptually Uniform Lightness**: Lightness `0.7` has the exact same visual luminance across all hues.
2. **Smooth Gradient Interpolation**: Transitions between colors never pass through dirty muddy grays.
3. **P3 Wide Color Gamut Support**: Access to richer, more vibrant displays on modern Apple and high-end hardware.

---

## 2. Surface Elevation Architecture (Tailwind CSS v4)

Never simulate depth with heavy, blurry drop shadows (`shadow-2xl`). Construct depth with **ambient luminance and hairline borders**:

```css
@import "tailwindcss";

@theme {
  /* Surface Luminance Scale (Dark Mode Foundation) */
  --color-canvas: oklch(0.12 0.01 260);      /* Deep obsidian base */
  --color-surface-subtle: oklch(0.15 0.01 260); /* Flat containers */
  --color-surface: oklch(0.18 0.01 260);     /* Interactive panels */
  --color-surface-overlay: oklch(0.22 0.01 260); /* Dialogs, popovers */

  /* Hairline Dividers (Subtle Specular Reflection) */
  --color-border-subtle: rgba(255, 255, 255, 0.08);
  --color-border-hover: rgba(255, 255, 255, 0.16);

  /* Signature Functional Accent: Electric Amber */
  --color-accent-amber: oklch(0.75 0.18 55);
  --color-accent-amber-glow: oklch(0.75 0.18 55 / 0.15);

  /* Text Contrast Hierarchy (APCA / WCAG AAA Compliant) */
  --color-text-primary: oklch(0.96 0.005 260);
  --color-text-secondary: oklch(0.70 0.01 260);
  --color-text-muted: oklch(0.48 0.01 260);
}
```

---

## 3. The "One Signature Accent" Rule

Vibe-coded AI templates decorate screens with multiple clashing gradients (purple headers, green cards, blue buttons).

**The High-Craft Rule**:
- 90% of the interface is executed in disciplined, high-contrast monochrome (obsidian, slate, neutral white).
- **One** signature accent color (e.g. Electric Amber `oklch(0.75 0.18 55)`) is reserved exclusively for:
  1. Interactive keyboard focus rings (`focus-visible:ring-accent-amber`).
  2. Active tab indicators and radio checkmarks.
  3. Single primary conversion action per screen.

---

## 4. Atmospheric Depth & Specular Highlights

Instead of blurry black shadows, use subtle top-edge specular highlights:

```css
/* Premium Specular Card Container */
.surface-card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: 0.75rem;
  /* Top-edge ambient light catch */
  box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  transition: border-color 200ms var(--ease-out-expo);
}

.surface-card:hover {
  border-color: var(--color-border-hover);
}
```
