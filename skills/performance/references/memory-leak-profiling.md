# Memory Leak Profiling & Retention Prevention

---

## 1. Common Front-End Leak Sources

1. **Uncleaned Event Listeners**: Adding `window.addEventListener('resize', handler)` without returning cleanup `removeEventListener` in `useEffect` / `componentWillUnmount`.
2. **Dangling Timers**: `setInterval` references that remain active after component unmount.
3. **Detached DOM Nodes**: Keeping references to deleted DOM nodes inside closures or global arrays.
4. **Three.js Unreleased GPU Resources**: Forgetting `geometry.dispose()`, `material.dispose()`, `texture.dispose()`.

---

## 2. Chrome DevTools Heap Snapshot Checklist

- Take baseline snapshot (1).
- Perform user action 5 times (open/close modal, navigate back/forth).
- Trigger manual Garbage Collection (trash can icon).
- Take second snapshot (2).
- Filter by "Objects allocated between Snapshot 1 and 2". Any retained count $>0$ indicates a leak.
