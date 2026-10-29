# Core Web Vitals (CWV) Audit & Budgets

---

## 1. Google 2026 Core Web Vitals Thresholds

Metric | Good (P75) | Needs Improvement | Poor
:--- | :--- | :--- | :---
**Largest Contentful Paint (LCP)** | $\le 2.5\,\text{s}$ | $2.5\,\text{s} - 4.0\,\text{s}$ | $> 4.0\,\text{s}$
**Interaction to Next Paint (INP)** | $\le 200\,\text{ms}$ | $200\,\text{ms} - 500\,\text{ms}$ | $> 500\,\text{ms}$
**Cumulative Layout Shift (CLS)** | $\le 0.1$ | $0.1 - 0.25$ | $> 0.25$

---

## 2. Practical Remediations

- **LCP Remediation**: Preload hero images (`<link rel="preload" as="image" href="...">`). Eliminate render-blocking CSS/JS before hero content.
- **INP Remediation**: Yield to the main thread during heavy JavaScript tasks using `scheduler.yield()` or `setTimeout(..., 0)`.
- **CLS Remediation**: Always specify explicit `width` and `height` attributes (or `aspect-ratio`) on images, videos, and dynamic ads.
