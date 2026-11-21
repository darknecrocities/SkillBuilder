# CSS Container Queries (`@container`) & Modern Layout Guide

> **Objective**: Make every UI module genuinely portable across sidebars, bento cells, split panes, and modals by anchoring component geometry to its parent container rather than global viewport breakpoints.

---

## 1. Container Context vs. Viewport Breakpoints

Viewport media queries (`@media (min-width: 768px)`) break when a card sits inside a `320px` sidebar on a `1440px` monitor. Always bind component internal layout changes to a named container:

```css
.metric-shell {
  container-type: inline-size;
  container-name: metric-shell;
}

.metric-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
}

@container metric-shell (min-width: 440px) {
  .metric-card {
    display: grid;
    grid-template-columns: 152px 1fr auto;
    align-items: center;
    gap: 1.25rem;
    padding: 1.25rem 1.5rem;
  }
}
```

### Container Query Units (`cqi` / `cqw`)
Scale internal headlines or icon spacing relative to parent width (`clamp(0.95rem, 2.8cqi, 1.35rem)`), avoiding sudden jumps when sidebars resize.

---

## 2. Tailwind CSS v4 `@container` & Subgrid Patterns

```tsx
export function TelemetryPanel() {
  return (
    <section className="@container rounded-2xl border border-zinc-800/80 bg-zinc-950 p-4">
      <div className="grid grid-cols-1 gap-4 @md:grid-cols-[160px_1fr] @xl:grid-cols-[200px_1fr_auto]">
        <div className="font-mono text-xs uppercase tracking-wider text-zinc-400">p95 Latency</div>
        <div className="font-mono text-2xl tabular-nums text-zinc-100">42.8 ms</div>
        <div className="hidden @xl:block text-xs text-emerald-400">Nominal</div>
      </div>
    </section>
  );
}
```

---

## 3. `@starting-style` & CSS Scroll-Driven Micro-Motion

Replace heavy JS mount observers for simple entry/exit CSS transitions:

```css
.popover-panel {
  opacity: 1;
  transform: translateY(0) scale(1);
  transition: opacity 200ms cubic-bezier(0.16, 1, 0.3, 1),
              transform 200ms cubic-bezier(0.16, 1, 0.3, 1),
              display 200ms allow-discrete;
}

@starting-style {
  .popover-panel {
    opacity: 0;
    transform: translateY(6px) scale(0.98);
  }
}
```

---

## 4. Anti-Patterns & Failure Modes
- **Nested Container Trap**: Never read `container-type: inline-size` on the same element whose CSS rule tries to query `@container` — the query always targets an *ancestor* container.
- **Intrinsic Width Collapse**: Setting `container-type: inline-size` removes intrinsic child width sizing on inline-flex/auto-width grids; always give the container wrapper an explicit `width: 100%` or grid track.
- **Reduced Motion**: Wrap CSS `@starting-style` and `::view-transition-*` animations in `@media (prefers-reduced-motion: reduce) { transition: none; animation: none; }`.
