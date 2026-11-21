# Core Web Vitals Audit (`LCP`, `CLS`, `INP`) & Bundle Budgets

> **Objective**: Maintain green Core Web Vitals (`LCP <= 2.5s`, `CLS <= 0.05`, `INP <= 200ms`) across mobile 4G and desktop viewports.

---

## 1. Metric Targets & Root-Cause Playbook

| Vital | Target Ceiling | Primary Causes of Regression | Deterministic Fix |
| :--- | :--- | :--- | :--- |
| **LCP** (Largest Contentful Paint) | `<= 2.5s` (`<= 1.8s` ideal) | Un-prioritized hero image (`loading="lazy"` on LCP!), render-blocking CSS/fonts, waterfall RSC fetches | Add `fetchPriority="high"` + `preload` on LCP asset, self-host/subset fonts (`font-display: swap`), parallelize data fetches |
| **CLS** (Cumulative Layout Shift) | `<= 0.05` | Images/SVGs/Rive mascots missing `width`/`height` or `aspect-ratio`, late-injected banners pushing content | Reserve fixed `aspect-ratio` boxes, use exact-height skeleton loaders, animate `transform` only |
| **INP** (Interaction to Next Paint) | `<= 200ms` (`<= 100ms` ideal) | Heavy synchronous JSON/Canvas work on click, giant un-memoized lists re-rendering on keystroke | Offload media/search to Web Workers, debounce `150–300ms` inputs, virtualize lists `> 100` rows, use `startTransition` |

---

## 2. Bundle Size & Third-Party Script Discipline

- **Initial JS Route Budget**: Keep route-level client JS `<= 150 KB` gzipped (`<= 250 KB` max for rich tools).
- **Dynamic Imports**: Lazy-load heavy optional libraries (`three`, `@rive-app/react-canvas`, PDF/QR engines, charts) via `React.lazy` / `next/dynamic` so landing routes stay instant.
- **Benchmark Verification (`Explain the Number`)**: Measure Lighthouse/Playwright Web Vitals on a **production build** (`pnpm build && pnpm start`) with CPU `4x` throttling — never measure perf on `next dev` / Vite HMR!
