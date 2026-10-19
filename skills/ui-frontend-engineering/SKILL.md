---
name: ui-frontend-engineering
description: Architect, implement, and maintain responsive, accessible, high-performance web and mobile user interfaces using modern design systems (Tailwind CSS v4, Radix/shadcn), React 19, Next.js, and Flutter.
---

# UI & Frontend Systems Engineering

> **Role**: Principal Frontend & UI/UX Systems Architect  
> **Philosophy**: *Pixel-perfect craft. Uncompromising accessibility. Fast Core Web Vitals. Bulletproof state synchronization.*

This skill establishes frontend engineering discipline across web and mobile platforms. It enforces semantic HTML, WCAG 2.2 AA accessibility, responsive design system tokens, resilient client state management, and continuous performance auditing.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/anti-vibe-coding-standard.md](references/anti-vibe-coding-standard.md) | Anti-Vibe-Coding standard: forbidding purple/green glow, card-soup, badges, emojis. |
| **Reference** | [references/design-systems-and-tailwind.md](references/design-systems-and-tailwind.md) | Tailwind CSS v4, design tokens, Radix UI & shadcn/ui component patterns. |
| **Reference** | [references/responsive-and-accessible-ui.md](references/responsive-and-accessible-ui.md) | Mobile-first viewport rules, focus management, ARIA roles, keyboard nav. |
| **Reference** | [references/frontend-performance-and-vitals.md](references/frontend-performance-and-vitals.md) | Core Web Vitals (LCP, INP, CLS), code-splitting, lazy loading, bundle budgets. |
| **Reference** | [references/state-management-and-data-fetching.md](references/state-management-and-data-fetching.md) | TanStack Query, Zustand, optimistic UI updates, cache invalidation. |
| **Reference** | [references/frontend-error-catalog.md](references/frontend-error-catalog.md) | Catalog of frontend errors: hydration mismatches, layout shifts, infinite loops. |
| **Template** | [templates/AccessibleComponent.tsx](templates/AccessibleComponent.tsx) | Accessible, keyboard-navigable component template. |
| **Template** | [templates/ResponsiveLayout.tsx](templates/ResponsiveLayout.tsx) | Mobile-first responsive shell with sticky header and sidebar navigation. |
| **Utility** | [scripts/verify_frontend_quality.py](scripts/verify_frontend_quality.py) | CLI auditor for accessibility markup and frontend quality gates. |

---

## 2. Core Frontend Principles

### 1. Semantic HTML & WCAG 2.2 AA Accessibility
- Always use native semantic elements (`<button>`, `<nav>`, `<main>`, `<article>`, `<dialog>`) before reaching for `<div>` or `<span>`.
- Interactive custom elements must support keyboard navigation (`Tab`, `Enter`, `Space`, `Escape`).
- Every image must have an explicit `alt` attribute. Every form input must have an associated `<label>`.
- Interactive icon buttons must have `aria-label` or visually hidden screen reader text.

### 2. Design Tokens & Atomic Composition
- Enforce consistent typography, spacing, and color palettes via design tokens (Tailwind CSS v4 CSS variables).
- Separate UI components into **Presentational** (pure, stateless, themed) and **Container/Logic** (state, queries, mutations).

### 3. Core Web Vitals & Performance Ceilings
- **LCP (Largest Contentful Paint)**: < 2.5s. Preload hero images and critical fonts.
- **INP (Interaction to Next Paint)**: < 200ms. Avoid blocking the main JavaScript thread with heavy operations.
- **CLS (Cumulative Layout Shift)**: < 0.1. Explicitly reserve dimensions (`width`, `height`, `aspect-ratio`) for images and embeds.

### 4. Client State & Optimistic Mutations
- Distinguish between **Server Cache** (remote entity state managed via TanStack Query / SWR) and **Client State** (transient UI state managed via Zustand / React Context).
- Implement optimistic updates on mutations with automatic rollback on error.

### 5. Strict Anti-Vibe-Coding Aesthetic Guardrails
- **No Neon Gradients or Glows**: Prohibit purple/indigo gradients and neon green glowing borders. Use high-contrast neutral scales (zinc/slate).
- **No Card-Soup**: Prohibit wrapping every item in high-elevation rounded cards. Use typographic hierarchy, white space, and subtle 1px dividers.
- **No Emojis as UI Icons**: Strictly prohibit using raw emojis in buttons, nav links, or headers. Use semantic vector SVG icons (Lucide, Radix) with `aria-hidden="true"`.
- **No Frivolous Badges**: Prohibit cosmetic "v1.0.0", "AI-Powered", or decorative pill chips. Allow badges only for real system lifecycle state.
- **Human Technical Copywriting**: Prohibit synthetic AI marketing hype ("seamlessly elevate your synergy"). Use concise, direct, factual descriptions.

---

## 3. Automation Tool: Frontend Quality Verifier

Audit HTML and JSX files for accessibility compliance:
```bash
python3 scripts/verify_frontend_quality.py --path src/components/
```
