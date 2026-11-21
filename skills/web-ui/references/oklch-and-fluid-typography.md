# OKLCH Perceptual Color Spaces & Fluid Typography Manual

> **Objective**: Build themeable, contrast-verified UI palettes and smooth typographic scales without HSL perceptual brightness jumps or step-ladder media queries.

---

## 1. Why OKLCH Replaces RGB / HSL

In HSL, `hsl(60 100% 50%)` (yellow) and `hsl(240 100% 50%)` (blue) share `50%` lightness numerically yet diverge dramatically in human luminance. OKLCH (`oklch(L C H / alpha)`) preserves uniform perceptual lightness `L`, allowing predictable dark/light surface ramps and contrast pairs:

```css
:root {
  --surface-canvas: oklch(0.13 0.008 260);
  --surface-panel: oklch(0.17 0.010 260);
  --surface-elevated: oklch(0.22 0.012 260);
  --border-hairline: oklch(0.34 0.012 260 / 0.45);
  --text-primary: oklch(0.96 0.004 260);
  --text-secondary: oklch(0.74 0.010 260);
  --accent-primary: oklch(0.68 0.17 240);
}
```

### Derived Interactive States via `color-mix()`
```css
.action-surface:hover {
  background-color: color-mix(in oklch, var(--surface-elevated), white 6%);
}
.action-surface:active {
  background-color: color-mix(in oklch, var(--surface-elevated), black 8%);
}
```

---

## 2. WCAG 2.2 AA Contrast Floor

| Role | Dark Canvas (`#09090b`) | Light Canvas (`#fafafa`) | Minimum Ratio |
| :--- | :--- | :--- | :--- |
| **Primary Copy** | `zinc-100` (`#f4f4f5`) | `zinc-950` (`#09090b`) | `>= 12:1` (AAA) |
| **Secondary / Metadata** | `zinc-400` (`#a1a1aa`) | `zinc-600` (`#52525b`) | `>= 4.5:1` (AA) |
| **Prohibited Body Text** | `zinc-500` (`#71717a`, ~`3.9:1`) | `zinc-400` (`#a1a1aa`, ~`2.3:1`) | Fails WCAG AA |

---

## 3. Fluid Typography & Measure Constraints

- **Smooth `clamp()` Curve**:
  - Body: `clamp(0.9375rem, 0.88rem + 0.28vw, 1.0625rem)` (`15px -> 17px`)
  - Section H2: `clamp(1.375rem, 1.1rem + 1.2vw, 2rem)` (`22px -> 32px`)
  - Hero H1: `clamp(2.25rem, 1.5rem + 3vw, 4.25rem)` (`36px -> 68px`)
- **Optical Tracking**: Tighten large display headings (`-0.035em` at `48px+`, `-0.02em` at `24–36px`) and widen uppercase micro-labels (`+0.06em`).
- **Readable Measure**: Cap prose paragraphs at `max-width: 65ch` so wide `1920px` displays never stretch lines across 140 characters.
- **Tabular Numerals**: Apply `font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1, "zero" 1;` on timers, metrics, and financial tables.
