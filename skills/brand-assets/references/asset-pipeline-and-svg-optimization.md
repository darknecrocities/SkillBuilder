# Asset Pipeline, SVG Optimization & Resource Delivery

> **Objective**: Ship fast, sharp, zero-CLS visual assets across web and mobile with clean SVG DOM trees, zero ID collisions, and modern raster compression.

---

## 1. SVG Hygiene & Optimization Rules

1. **Strip Editor Bloat**: Remove `<metadata>`, `<!-- Generator: Adobe Illustrator ... -->`, `data-name`, empty `<g>` wrappers, and unused `<defs>`.
2. **Coordinate Precision**: Round floating-point coordinates to `<= 2` decimal places (`128.45` instead of `128.4519827361`).
3. **Never Embed Base64 Rasters**: `<image href="data:image/png;base64,...">` inside `.svg` defeats vector scaling and bloats bundles. Export real raster AVIF/WebP or redraw as pure vector paths.
4. **Namespace Gradient & Clip IDs**: Inline `<defs><linearGradient id="g1">` causes silent visual corruption when two SVGs on the same page both define `#g1`. Always namespace IDs (`id="brand-og-bg"` or React `useId()`).
5. **Icon Sprites vs. Inline**: Use Lucide/component vectors for UI controls (`16–24px`); use external `<img src="/icons/...">` or SVG `<symbol>` sprites for repeated large marks.

---

## 2. Raster Compression & Zero-CLS Budgets

| Asset Class | Target Format | Size Budget | Mandatory Attributes |
| :--- | :--- | :--- | :--- |
| **Hero / Product Photos** | **AVIF** primary, **WebP** fallback | `<= 180 KB` (`<= 1600px` wide) | `width`, `height`, `sizes`, `fetchPriority="high"` (LCP only) |
| **Thumbnails / Avatars** | **WebP** / **AVIF** | `<= 25 KB` | Explicit `aspect-square`, `loading="lazy"` |
| **OpenGraph Social Card** | **PNG** / **JPEG** (`1200x630`) | `<= 250 KB` | `<meta property="og:image:width" content="1200">` (required for social crawlers; SVG alone is not supported by all crawlers) |
| **Splash Screens** | Vector mark on solid token canvas | `<= 15 KB` | Match OS dark/light launch theme to prevent white flash |

---

## 3. Verification Checklist Before Release
- [ ] Every `<img>` and `<svg>` reserves explicit `width`/`height` or CSS `aspect-ratio` (`CLS < 0.05`).
- [ ] `verify_brand_assets.py --path . --strict` passes with zero bloated SVGs or missing `viewBox` attributes.
- [ ] OpenGraph card (`1200x630`) exported as raster PNG alongside source SVG template for Discord/X/LinkedIn unfurls.
