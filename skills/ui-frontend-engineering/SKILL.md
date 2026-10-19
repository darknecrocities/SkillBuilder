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
| **Reference** | [references/cinematic-motion-and-animations.md](references/cinematic-motion-and-animations.md) | Spring physics, blur-to-focus text reveals, scroll choreography, reduced motion. |
| **Reference** | [references/premium-color-and-materiality-rules.md](references/premium-color-and-materiality-rules.md) | OKLCH color space, obsidian/slate surfaces, hairline specular highlights. |
| **Reference** | [references/design-systems-and-tailwind.md](references/design-systems-and-tailwind.md) | Tailwind CSS v4, design tokens, Radix UI & shadcn/ui component patterns. |
| **Reference** | [references/responsive-and-accessible-ui.md](references/responsive-and-accessible-ui.md) | Mobile-first viewport rules, focus management, ARIA roles, keyboard nav. |
| **Reference** | [references/frontend-performance-and-vitals.md](references/frontend-performance-and-vitals.md) | Core Web Vitals (LCP, INP, CLS), code-splitting, lazy loading, bundle budgets. |
| **Reference** | [references/state-management-and-data-fetching.md](references/state-management-and-data-fetching.md) | TanStack Query, Zustand, optimistic UI updates, cache invalidation. |
| **Reference** | [references/frontend-error-catalog.md](references/frontend-error-catalog.md) | Catalog of frontend errors: hydration mismatches, layout shifts, infinite loops. |
| **Template** | [templates/CinematicHero.tsx](templates/CinematicHero.tsx) | Cinematic hero with blur text reveal, tactile CTA, and specular illumination. |
| **Template** | [templates/ScrollReveal.tsx](templates/ScrollReveal.tsx) | Scroll-driven staggered element reveal with viewport intersection triggers. |
| **Template** | [templates/InteractiveControls.tsx](templates/InteractiveControls.tsx) | Sliding pill tabs (layoutId), numeric counter ticker, tactile spring buttons. |
| **Template** | [templates/AccessibleComponent.tsx](templates/AccessibleComponent.tsx) | Accessible, keyboard-navigable dialog with SVG vector icons. |
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

### 6. Spring-Based Motion Physics & Choreography
- **Springs Over Linear Eases**: Micro-interactions use `stiffness: 450, damping: 32, mass: 0.8` (snappy, tactile, zero overshoot). View transitions use `stiffness: 280, damping: 26`.
- **Typographic Reveals**: Use blur-to-focus reveals (`filter: blur(8px) -> blur(0px)` with vertical translation) and monospace tabular numbers (`font-variant-numeric: tabular-nums`).
- **Scroll Choreography**: Use CSS `animation-timeline: view()` and IntersectionObserver staggers.
- **Mandatory Reduced Motion**: Every animated component must degrade to instant state changes when `prefers-reduced-motion: reduce` is active.

### 7. OKLCH Color Science & Atmospheric Materiality
- **OKLCH Color Space**: Use OKLCH for uniform perceptual luminance and smooth gradient interpolation across wide gamut displays.
- **Deep Obsidian Surfaces**: Layer canvas base (`oklch(0.12 0.01 260)`) and elevated surfaces (`oklch(0.18 0.01 260)`).
- **Hairline Specular Highlights**: Replace heavy drop shadows with 1px subtle borders (`border-white/[0.08]`) and top-edge specular insets (`box-shadow: inset 0 1px 0 0 rgba(255,255,255,0.08)`).
- **Single Signature Accent**: Reserve one signature accent (Electric Amber or Safety Orange) strictly for focus and primary triggers.

---

## 3. Automation Tool: Frontend Quality Verifier

Audit HTML and JSX files for accessibility compliance:
```bash
python3 scripts/verify_frontend_quality.py --path src/components/
```
