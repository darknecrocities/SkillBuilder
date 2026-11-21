# Next.js App Router, Page-Data Matrix & Bilingual Rewrites

> **Objective**: Structure deterministic Next.js App Router hierarchies with clean static-vs-dynamic boundaries, zero layout cascades, and canonical bilingual routing.

---

## 1. Layout Isolation & Parallel / Intercepting Routes

- **Shared `layout.tsx`**: Keep root and section layouts purely structural (fonts, metadata, nav shell). Never execute blocking slow fetches in the root layout unless cached and streamed via `<Suspense>`.
- **Route Groups (`(marketing)`, `(app)`)**: Separate public marketing chrome from authenticated workspace shells without polluting URL segments.
- **Loading & Error Boundaries**: Every dynamic segment (`[id]/`) should provide co-located `loading.tsx` (matching exact card/table heights so `CLS < 0.05`) and `error.tsx` recovery UI.

---

## 2. Static vs. Dynamic Route Contract (`bettersanfernando` Pattern)

Maintain a documented route inventory (`docs/PAGE-DATA-MATRIX.md`) classifying every route explicitly:

| Route Type | Next.js Config | Use Case |
| :--- | :--- | :--- |
| **Pre-rendered Record** | `generateStaticParams()` | Service directories, barangay pages, docs, marketing pages |
| **Search / Filter Directory** | `export const dynamic = "force-dynamic"` | Interactive query parameter filters (`?q=...&category=...`) |
| **Canonical Redirect** | `permanentRedirect(...)` (`308`) | Redirect legacy `/contact` -> `/government/contact` and `/en/...` -> `/` |

---

## 3. Unprefixed Default Locale + Prefixed Secondary Locale

```typescript
// middleware.ts pattern for canonical unprefixed primary locale
import { NextResponse, type NextRequest } from "next/server";

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  if (pathname === "/en" || pathname.startsWith("/en/")) {
    const cleanPath = pathname.replace(/^\/en/, "") || "/";
    return NextResponse.redirect(new URL(cleanPath, req.url), 308);
  }
  if (!pathname.startsWith("/fil") && !pathname.startsWith("/api") && !pathname.startsWith("/_next")) {
    const url = req.nextUrl.clone();
    url.pathname = `/en${pathname === "/" ? "" : pathname}`;
    return NextResponse.rewrite(url);
  }
  return NextResponse.next();
}
```
