# Memory Leak Profiling & Lifecycle Cleanup Manual

> **Objective**: Diagnose and eliminate retained heap growth across long-lived React/SPA sessions, Node/Python services, Canvas/Rive stages, and mobile apps.

---

## 1. High-Frequency Leak Sources & Fixes

| Leak Vector | Diagnostic Signature | Mandatory Cleanup Pattern |
| :--- | :--- | :--- |
| **Browser `URL.createObjectURL`** | Rising native blob memory across repeated image/PDF previews | Call `URL.revokeObjectURL(url)` in `onload`/`onerror` or `useEffect` cleanup |
| **Orphaned Listeners / Observers** | Detached `HTMLDivElement` nodes accumulating in Chrome Heap Snapshot | Pair every `addEventListener`, `ResizeObserver`, `IntersectionObserver` with `removeEventListener` / `.disconnect()` |
| **Web Workers, Rive & Three.js** | GPU/WASM memory climbing on route switches | Call `worker.terminate()`, `rive.cleanup()`, `geometry/material/texture.dispose()`, `renderer.dispose()` |
| **Unbounded Module Caches** | `const cache = new Map()` growing without eviction in Node/Python | Use bounded `LRU` (`maxSize = 500–2000`) or TTL eviction instead of raw global `Map`/`dict` |
| **Unclosed Streams / Timers** | Process fails to exit on `SIGTERM` or memory drifts linearly | Cancel `AbortController`, `clearInterval`, `audioCtx.close()`, and drain DB pools on shutdown |

---

## 2. Heap Snapshot Comparison Protocol (Chrome DevTools / Node)
1. Take **Snapshot 1** at steady idle state (`gc()` forced).
2. Execute the suspected user flow (open/close modal, process 5 files, switch routes) `5–10` times.
3. Force GC and take **Snapshot 2**.
4. Filter by `"Objects allocated between Snapshot 1 and 2"` — any retained `Detached HTMLElement`, `Worker`, `Rive`, or growing `Array` count reveals the exact retainer path.
