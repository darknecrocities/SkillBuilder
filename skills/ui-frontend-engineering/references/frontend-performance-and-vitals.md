# Frontend Performance & Core Web Vitals

Architectural techniques for optimizing modern web applications for speed, responsiveness, and visual stability.

---

## 1. The Core Web Vitals Trifecta

| Metric | Full Name | Target Ceiling | Root Problem | Key Optimization |
| :--- | :--- | :--- | :--- | :--- |
| **LCP** | Largest Contentful Paint | < 2.5s | Slow server response, large images | Preload hero image, use modern formats (AVIF/WebP) |
| **INP** | Interaction to Next Paint | < 200ms | Heavy JS execution blocking main thread | Debounce inputs, offload work to Web Workers |
| **CLS** | Cumulative Layout Shift | < 0.1 | Unsized media, injected banners | Reserve container dimensions via `aspect-ratio` |

---

## 2. Code-Splitting & Dynamic Imports
- Split routes using dynamic imports (`next/dynamic` or `React.lazy`).
- Defer non-critical third-party scripts (analytics, customer support widgets) until the main thread is idle (`strategy="lazyOnload"`).
- Audit bundle size in CI using tools like `@next/bundle-analyzer`.
