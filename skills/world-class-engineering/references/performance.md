# Performance and Resource Efficiency Standards

This reference guides performance profiling, resource budgeting, optimization workflows, and caching strategies.

---

## 1. Evidence-First Optimization Cycle

Premature optimization is a major source of bugs and code obfuscation. Follow this disciplined cycle:

```mermaid
flowchart LR
    Measure["1. Profile & Establish Baseline"] --> Identify["2. Identify True Bottleneck"]
    Identify --> Optimize["3. Apply Targeted Optimization"]
    Optimize --> Verify["4. Measure Delta & Regressions"]
```

1. **Measure First**: Never optimize code based on intuition alone. Use profilers (e.g., Chrome DevTools, `cProfile`, Go `pprof`, `clinic.js`) and APM telemetry to locate real hotspots.
2. **Prioritize Macro-Bottlenecks Over Micro-Optimizations**:
   - Macro: Eliminating N+1 database queries, reducing network round trips, adding appropriate composite indexes, using compression (gzip/brotli), streaming large files.
   - Micro: Bitwise shifts, loop unrolling, object pooling (rarely worthwhile unless building core runtime libraries or graphics engines).
3. **Never Sacrifice Correctness or Security**: Never disable input validation, authentication, or type safety to shave milliseconds unless mathematically proven necessary and protected by compensatory controls.

---

## 2. Common Bottlenecks & Remediation

| Domain | Bottleneck | Remediation |
| :--- | :--- | :--- |
| **Database** | N+1 Query Problem | Batch loading (e.g., DataLoader pattern, SQL `IN (...)` queries, ORM `JOIN FETCH` / `select_related`). |
| **Database** | Full Table Scans | Add indexes matching the query `WHERE`, `ORDER BY`, and `JOIN` clauses. Check query plans via `EXPLAIN ANALYZE`. |
| **Network** | Chatty Microservice / API Calls | Consolidate endpoints, leverage GraphQL or BFF (Backend-for-Frontend), implement batch requests. |
| **Frontend** | Oversized JavaScript Bundles | Dynamic imports (`React.lazy()`, code splitting), tree-shaking dead exports, analyzing bundles via `webpack-bundle-analyzer` or `rollup-plugin-visualizer`. |
| **Memory** | Memory Leaks & Retained Closures | Detach event listeners upon component unmount, close open streams/sockets, avoid unbounded global collections. |
| **Compute** | Heavy Blocking CPU on Main Thread | Offload CPU-heavy computation to Worker threads (Node.js `worker_threads`, Web Workers) or background worker queues (Celery, BullMQ). |

---

## 3. Caching Strategy & Invalidation Rules

> *"There are only two hard things in Computer Science: cache invalidation and naming things."* — Phil Karlton

Before introducing any cache:
- **Define the Invalidation Mechanism**:
  - **Time-to-Live (TTL)**: For data that tolerates eventual consistency (e.g., product catalog cached for 5 minutes).
  - **Event-Driven Purging**: Invalidate or update cache keys immediately when mutating data (e.g., `user:123` purged on `UPDATE users WHERE id=123`).
  - **Content-Addressable Keys**: Cache assets based on cryptographic content hashes (`main.[hash].js`), enabling permanent caching (`Cache-Control: max-age=31536000, immutable`).
- **Prevent Cache Stampedes (Thundering Herd)**:
  - Implement mutex locking, probabilistic early expiration (XFetch), or stale-while-revalidate patterns so only one worker queries the database on cache miss.

---

## 4. Bounded Concurrency & Backpressure

- **Never Use Unbounded Queues or Worker Pools**: Unbounded concurrency causes out-of-memory (OOM) crashes under traffic spikes.
- **Set Explicit Concurrency Limits**: Use semaphores or bounded pools (e.g., `p-limit` in Node.js, worker pools in Go).
- **Graceful Backpressure**: When internal processing queues fill up, return HTTP 429 (Too Many Requests) or HTTP 503 (Service Unavailable) rather than crashing the process.
