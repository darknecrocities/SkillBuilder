# SVG Rigging & Lottie (`.lottie`) Fallback Architecture

> **Objective**: When a `.riv` binary is not yet authored or a zero-WASM bundle budget applies (`< 8 KB` gzipped), build an interactive mathematical SVG rig or optimized dotLottie stage without sacrificing crisp geometry or accessibility.

---

## 1. Decision Matrix: `.riv` vs. `.lottie` vs. Rigged SVG

| Criterion | Rive (`.riv`) | dotLottie (`.lottie`) | Mathematical Rigged SVG |
| :--- | :--- | :--- | :--- |
| **Interactive Pointer Gaze** | Native 2D Blend State (`lookX`/`lookY`) | Manual segment scrubbing | Direct CSS/React transform on `<g id="pupils">` |
| **Bundle / Runtime Overhead** | ~180 KB WASM + `<150 KB` `.riv` | ~45 KB player + `<80 KB` `.lottie` | **0 KB external runtime** (`~2–6 KB` JSX/SVG) |
| **Complex Bones & Constraints** | Best-in-class | Keyframe baked | Limited to clean hierarchical `<g>` pivots |
| **Best Use Case** | Flagship interactive companion | Linear onboarding / celebratory burst | Ultra-lightweight UI mascots, empty states, CLI/docs |

---

## 2. Pure Vector SVG Rigging Rules

1. **Hierarchical `<g>` Pivot Groups**:
   - Nest `<g id="head">` -> `<g id="face-track">` -> `<g id="eyes">` -> `<g id="pupils">` with explicit `transform-origin` in SVG coordinate space (`transformBox: "fill-box"`).
2. **Unique Gradient IDs**:
   - Never reuse generic `#grad1` or `#glow` across multiple SVG instances on the same page; prefix with `useId()` in React (e.g. `id={`visor-${uid}`}`).
3. **Zero Raster Embedded Blobs**:
   - Prohibit `<image href="data:image/png;base64,...">` inside mascot SVGs.
4. **Node & Command Budget**:
   - Keep each path concise (`<= 40` commands per part, integer or 2-decimal precision).
5. **GPU Composite Animation Only**:
   - Animate only `transform` (`translate3d`, `scale`, `rotate`) and `opacity` — never mutate SVG `d` strings per frame on the main thread unless throttled inside a small isolated state switch.

---

## 3. Lottie (`.lottie` / `.json`) Optimization Checklist

- Prefer compressed `.lottie` archive over raw `.json` (`60–80%` smaller).
- Strip hidden layers, unused Illustrator masks, and high-vertex rasterized paths before export.
- Gate playback on `IntersectionObserver` visibility and `prefers-reduced-motion`:
  - When `prefers-reduced-motion: reduce` is active, jump cleanly to the resting hero frame (`goToAndStop(restingFrame, true)`).

---

## 4. Accessibility & Reduced Motion Rules

- Decorative mascots paired with text headings must carry `aria-hidden="true"`.
- Standalone status mascots (e.g., error or empty-state illustration) must expose `role="img"` and a concise `aria-label`.
- Always check `window.matchMedia("(prefers-reduced-motion: reduce)")` (Web) or `MediaQuery.disableAnimationsOf(context)` (Flutter) before running continuous breathing or pointer-tracking RAF loops.
