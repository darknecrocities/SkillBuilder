# Master Software Engineering Error Catalog

A cross-discipline knowledgebase of real-world software defects, diagnostic commands, and battle-tested resolutions.

---

## 1. Frontend & UI Errors

### [ERR-FE-001] React Hydration Mismatch
- **Category**: Frontend
- **Symptom**: `Text content did not match. Server: "..." Client: "..."` or `Hydration failed because the initial UI does not match that which was rendered on the server.`
- **Root Cause**: Server-rendered HTML differences caused by client-only APIs (`window`, `localStorage`, `Date.now()`, or dynamic random IDs) executed during the initial render.
- **Diagnostic Command**: Inspect component render tree for browser globals accessed outside `useEffect` or client guards.
- **Resolution**:
  1. Move non-deterministic or browser-specific logic into `useEffect` or `useSyncExternalStore`.
  2. For client-only widgets, use dynamic import with `{ ssr: false }`.
  3. Avoid rendering timestamps on initial server HTML without a fixed locale/timezone format.
- **Regression Prevention**: Add Jest/Vitest test validating SSR markup matches client hydration output.

---

### [ERR-FE-002] Infinite State Re-render Loop
- **Category**: Frontend
- **Symptom**: `Maximum update depth exceeded. This can happen when a component repeatedly calls setState inside componentWillUpdate or componentDidUpdate.`
- **Root Cause**: Calling a state updater directly in the component render phase or having an unstable dependency reference in `useEffect` (e.g. object/array literal created inline).
- **Diagnostic Command**: Check dependency arrays in `useEffect` and `useCallback` for unstable object references.
- **Resolution**:
  1. Wrap inline callback triggers inside `useCallback` or event handlers.
  2. Use primitive values or memoized selectors in effect dependency arrays.
- **Regression Prevention**: ESLint `react-hooks/exhaustive-deps` rule enabled as error in CI.

---

## 2. Backend & API Errors

### [ERR-BE-001] Unhandled Promise Rejection Crash
- **Category**: Backend
- **Symptom**: Node.js process terminates abruptly with `UnhandledPromiseRejection: This error originated either by throwing inside of an async function without a catch block...`
- **Root Cause**: An asynchronous operation failed without a `.catch()` block or missing `await` inside a `try/catch` block.
- **Diagnostic Command**: Run with `--trace-warnings` or search code for floating asynchronous calls without `await`.
- **Resolution**:
  1. Ensure all async operations are awaited or returned inside a `try/catch`.
  2. Attach global process handlers: `process.on('unhandledRejection', (reason, promise) => { logger.error(...) })`.
- **Regression Prevention**: Enable TypeScript compiler flag `no-floating-promises` in `tsconfig.json`.

---

### [ERR-BE-002] Outbound Request Timeout / Hanging Connection
- **Category**: Backend
- **Symptom**: Worker exhausts thread pool or connection pool; incoming requests hang until gateway timeout (HTTP 504).
- **Root Cause**: Outbound HTTP/gRPC request initiated without explicit socket/read timeouts.
- **Diagnostic Command**: Check network metrics; inspect client initialization for missing `timeout` configuration.
- **Resolution**:
  1. Configure explicit 3s connection timeout and 15s execution timeout on all fetch/axios/gRPC clients.
  2. Implement AbortController with deadline propagation.
- **Regression Prevention**: Unit test mocking slow network endpoint ensuring client throws TimeoutException within budget.

---

## 3. Database Errors

### [ERR-DB-001] PostgreSQL Transaction Deadlock
- **Category**: Database
- **Symptom**: `ERROR: deadlock detected. Detail: Process 12345 waits for ShareLock on transaction 67890...`
- **Root Cause**: Concurrent transactions acquiring locks on multiple rows or tables in differing order.
- **Diagnostic Command**: `SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';`
- **Resolution**:
  1. Enforce strict monotonic lock acquisition ordering across all application transactions (e.g., sort IDs ascending before locking).
  2. Keep transactions minimal: never perform external HTTP calls or heavy CPU work inside a database transaction.
  3. Implement bounded exponential backoff retry on SQLSTATE `40P01`.
- **Regression Prevention**: Concurrent integration test simulating parallel overlapping transactions.

---

### [ERR-DB-002] N+1 Query Cascade
- **Category**: Database
- **Symptom**: Severe latency degradation under load; database query logs show hundreds of identical queries for a single HTTP request.
- **Root Cause**: Lazy-loading relational attributes inside an iteration loop without batch loading.
- **Diagnostic Command**: Enable ORM query logging or inspect query counter in test runner.
- **Resolution**:
  1. Use eager loading (`include` in Prisma, `with` in Drizzle, `JOIN FETCH` in SQL).
  2. Implement DataLoader pattern for batched key lookups.
- **Regression Prevention**: Automated test asserting query count per endpoint <= 3 regardless of result set size.

---

## 4. Cloud & DevOps Errors

### [ERR-CL-001] Kubernetes / Container OOMKilled
- **Category**: Cloud
- **Symptom**: Container terminates with exit code 137 (`OOMKilled: true`).
- **Root Cause**: Container memory consumption exceeded configured `resources.limits.memory`.
- **Diagnostic Command**: `kubectl describe pod <pod-name> | grep -A 3 "Last State:"`
- **Resolution**:
  1. Set runtime memory ceilings (e.g. Node `--max-old-space-size`, JVM `-Xmx`).
  2. Profile heap usage with memory snapshots.
  3. Set container memory request equal to limit to avoid unpredictable node eviction.
- **Regression Prevention**: Load testing in staging validating memory stability over 30 minutes.

---

### [ERR-CL-002] Container Non-Root Permission Denied
- **Category**: Cloud
- **Symptom**: `EACCES: permission denied, open '/app/data/storage.json'` or container fails to start after dropping root privileges.
- **Root Cause**: Files or directories created by root during build phase without granting ownership to unprivileged user (UID 10001).
- **Diagnostic Command**: Inspect Dockerfile for `RUN mkdir` followed by `USER appuser`.
- **Resolution**:
  1. Add `RUN chown -R appuser:appuser /app` before the `USER appuser` directive in Dockerfile.
- **Regression Prevention**: Automated container security audit script verifying local startup as non-root user.

---

## 5. AI & LLM Errors

### [ERR-AI-001] Structured Output Schema Validation Failure
- **Category**: AI
- **Symptom**: Model output fails client-side schema parsing (`ZodError: Expected array, received object` or JSON parse error).
- **Root Cause**: Model hallucinates extra markdown framing (e.g. ` ```json `) or returns malformed payload when prompt lacks strict JSON mode or schema definition.
- **Diagnostic Command**: Log raw response text before JSON parsing.
- **Resolution**:
  1. Use Gemini `response_mime_type="application/json"` with `response_schema`.
  2. Sanitize output with regex stripping surrounding markdown fences before parsing.
  3. Implement automatic 1-turn retry feeding the schema validation error back to the model.
- **Regression Prevention**: Unit test testing parser against real and malformed model outputs.
