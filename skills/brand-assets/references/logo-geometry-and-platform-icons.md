# Logo Geometry & Cross-Platform Icon Specifications

> **Objective**: Construct mathematically crisp app logos and export complete platform icon sets without tangent breaks, clipping bugs, or unreadable favicons.

---

## 1. Anti-Slop Logo Prohibitions

| AI Slop Trope | Why It Fails in Production | Professional Alternative |
| :--- | :--- | :--- |
| **Abstract Swirling Ribbon** | Relies on 10+ gradient stops; turns into grey mud at `16px` and fails monochrome embroidery/print. | Distinct interlocking geometric primitives with crisp negative-space gaps (`>= 24px` on `512` grid). |
| **Glowing Brain / Circuit Nodes** | Literal AI cliché; interior hairlines vanish below `64px`. | Domain-grounded abstract mark or tight typographic monogram. |
| **4-Pointed Sparkle Accent (`✦`)** | Universal stamp signaling synthetic AI wrapper slop. | Remove sparkles completely; let primary silhouette carry identity. |
| **Auto-Traced 500-Node SVG** | Jittery anchor points inflate DOM size and break crisp subpixel alignment. | Hand-crafted `M/L/C/A/Z` commands (`< 30` nodes total for the primary mark). |

---

## 2. Master $512 \times 512$ Grid & Apple Continuous Squircle

Construct master icons on a `512x512` grid (`8x8` modules of `64px`):
- **Outer Canvas**: `512 x 512`
- **Safe Icon Bounding Box**: `384 x 384` (64px inset per side)
- **Key Angles**: $0^\circ$, $45^\circ$, $90^\circ$ (or clean circular arcs tangent to grid intersections).

Apple icons reject plain `rx="112"` rounded rectangles because curvature jumps abruptly from $0$ to $1/r$ at the straight-to-arc join. Approximate the Lamé superellipse ($|x/a|^4 + |y/b|^4 = 1$) cleanly in SVG:

```svg
<path d="M 140 32 C 48 32, 32 48, 32 140 L 32 372 C 32 464, 48 480, 140 480 L 372 480 C 464 480, 480 464, 480 372 L 480 140 C 480 48, 464 32, 372 32 Z" />
```

---

## 3. Android Adaptive Icons (`108dp` / `66dp` Safe Zone)

Android OEM launchers apply arbitrary masks (circle, squircle, teardrop, rounded square):
1. **Canvas**: `108 x 108` logical units (`viewBox="0 0 108 108"`).
2. **Background Layer**: Full-bleed `108x108` solid/subtle surface (`ic_launcher_background`). Never include transparent corners.
3. **Foreground Layer**: Keep all critical mark geometry strictly inside the **center `66dp` diameter circle** (radius `33` around `(54, 54)`) so no OEM mask ever clips the logo.

---

## 4. Optical Centering vs. Mathematical Centering

Asymmetric shapes (play triangles, right-pointing arrows, speech bubbles) look visually off-center when placed at `boundingBox.center`:
- **Rule**: Compute visual center-of-mass rather than bounding-box midpoint. Shift a right-pointing triangle rightward by $\approx 1/6$ of its width (`+8px` to `+14px` on a `512` grid) so optical weight balances evenly.
- **Theme-Adaptive `favicon.svg`**: Embed `@media (prefers-color-scheme: dark)` inside the SVG `<style>` block so browser tabs adapt automatically without shipping duplicate dark/light favicon files.
