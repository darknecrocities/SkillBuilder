# Anti-Slop Editorial & Product Illustrations Manual

> **Objective**: Replace generic Corporate Memphis ("Alegria") vector clichés and glossy AI-generated raster scenes with cohesive, domain-authentic illustration systems that reinforce the UI design tokens.

---

## 1. Prohibited Illustration Tropes

1. **Corporate Memphis / Alegria Clones**: Disproportionately tiny heads, noodle limbs, pastel purple/lavender skin, floating abstract blobs behind people holding oversized laptops.
2. **Glossy AI 3D Plastic Renders**: Neon cyan/magenta rim lights, wet glass spheres, and floating holographic UI cards that clash with clean dark/light UI surfaces.
3. **Stock Mismatch**: Mixing three different stroke weights, hand-drawn sketch icons, and 3D clay renders on the same page.

---

## 2. Four Production Illustration Systems (Mapped to `/ui` Art Movements)

Select **one** illustration system matching your product's `/ui` movement and lock its stroke/fill grammar across every empty state, onboarding card, and marketing visual:

| System | Paired `/ui` Movement | Stroke & Geometry Rules | Color Discipline |
| :--- | :--- | :--- | :--- |
| **1. Technical CAD Blueprint** | Technical CAD / DevTools | Crisp `1.5px` uniform strokes, orthographic callout ticks, dashed dimension lines (`stroke-dasharray="3 3"`), zero soft blur. | Canvas neutral + `1px` hairline `#27272a` + single telemetry accent (`#06b6d4` or `#10b981`). |
| **2. Swiss Geometric Risograph** | Swiss Editorial | Bold flat shapes, strict 12-column grid cuts, sharp `0px` or disciplined `8px` corners, subtle `1.5%` paper grain overlay. | High-contrast ink/paper (`#09090b` / `#fafafa`) + single editorial accent (`#e11d48`). |
| **3. Architectural Isometric** | Industrial Tactical | True $30^\circ$ isometric projection (`cos 30° ≈ 0.866`), consistent 90° top-zenith shading across top/left/right planes. | 3-value neutral planes + safety orange (`#ff4400`) or amber (`#f59e0b`) indicator dot. |
| **4. Editorial Ink & Grain** | Japanese Wabi-Sabi | Variable-width organic contour (`1.5px–2.5px`), generous negative space (`>= 45%` canvas empty), sumi-ink warmth. | Washi cream (`#f7f6f2`), sumi ink (`#121214`), muted moss/bamboo (`#2e3a2e`). |

---

## 3. Empty-State & Hero Composition Rules
- **Consistent Stroke Weight**: Every illustration on a screen must share one normalized stroke weight (`1.5px` or `2px` at display size, `vector-effect="non-scaling-stroke"` when responsive).
- **Zero Decorative Text Inside SVGs**: Keep explanatory headings and CTAs in real semantic HTML/DOM text so screen readers, i18n translations, and `200%` font scaling work cleanly.
- **Theme Token Binding**: Bind neutral illustration strokes/fills to CSS custom properties (`currentColor`, `--color-border-subtle`, `--color-accent`) rather than hardcoded light-only hex fills.
