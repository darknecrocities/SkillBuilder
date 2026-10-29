# Next.js App Router Architectural Patterns

---

## 1. File-Based Routing Hierarchy

Route Segment | File Name | Purpose
:--- | :--- | :---
Page UI | `page.tsx` | Unique leaf route presentation
Shared Layout | `layout.tsx` | Preserved across child navigations (does not re-render)
Loading Skeleton | `loading.tsx` | Automatic Suspense boundary wrapper
Error Boundary | `error.tsx` | Client error boundary (`"use client"`) catching uncaught exceptions
Not Found UI | `not-found.tsx` | Triggered by `notFound()` invocations

---

## 2. Advanced Route Patterns

- **Parallel Routes (`@modal`, `@sidebar`)**: Render multiple pages simultaneously in the same layout.
- **Intercepting Routes (`(..)photo/[id]`)**: Load routes within current layout (modal photo view) while preserving URL shareability on hard refresh.
- **Route Groups (`(marketing)`, `(dashboard)`)**: Organize folder hierarchy without altering URL paths.
