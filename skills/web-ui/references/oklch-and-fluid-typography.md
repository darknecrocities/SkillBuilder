# OKLCH Perceptual Color Spaces & Fluid Typography

---

## 1. OKLCH Color Space

OKLCH matches human perceptual brightness (lightness $L$, chroma $C$, hue $H$):

```css
:root {
  --color-primary: oklch(0.65 0.22 250);
  --color-surface: oklch(0.98 0.01 240);
  --color-text: oklch(0.18 0.02 240);
}
```

### Advantages:
- Predictable contrast ratios across dark and light themes.
- Zero perceptual clipping in gamut mapping.

---

## 2. Fluid Typography with `clamp()`

Scale typography smoothly across screen widths without stepped media query jumps:

```css
/* Scales smoothly from 1rem (375px) to 1.5rem (1280px) */
font-size: clamp(1rem, 0.79rem + 0.89vw, 1.5rem);

/* Hero heading scales from 2rem (375px) to 4rem (1440px) */
font-size: clamp(2rem, 1.3rem + 2.98vw, 4rem);
```
