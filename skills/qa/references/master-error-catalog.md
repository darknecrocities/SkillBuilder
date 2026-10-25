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

## 4. Mobile & OS Lifecycle Errors

### [ERR-MOB-001] Background Memory Pressure Eviction Crash
- **Category**: Mobile
- **Symptom**: App terminates abruptly when backgrounded with `EXC_RESOURCE RESOURCE_TYPE_MEMORY` or silent process eviction by OS watchdog.
- **Root Cause**: High resident memory footprint caused by retaining uncompressed bitmap decoders and background listeners during background transitions.
- **Diagnostic Command**: Profile memory allocations in Xcode Instruments or Android Studio Memory Profiler while triggering background state.
- **Resolution**:
  1. Register for `onTrimMemory` (Android) or `didReceiveMemoryWarning` (iOS) and immediately purge in-memory caches.
  2. Pause background animation timers and release decoded image bitmaps.
  3. Flush unsaved state to disk and retain only lightweight model identifiers.
- **Regression Prevention**: Unit test validating cache eviction listeners trigger on memory warning notifications.

---

### [ERR-MOB-002] Cold-Start Deep-Link Desynchronization
- **Category**: Mobile
- **Symptom**: Tapping a deep link when the app is completely terminated crashes on launch with `NullPointerException: userSession is null` or routes to the login screen instead of the target entity.
- **Root Cause**: The navigation router mounts the destination screen before asynchronous authentication token rehydration finishes from secure storage.
- **Diagnostic Command**: Launch app via terminal URI trigger (`adb shell am start -W -a android.intent.action.VIEW -d "myapp://entity/123"`).
- **Resolution**:
  1. Implement a pending deep-link intent queue that buffers incoming URLs during cold start.
  2. Await authentication verification before releasing buffered deep links to the router.
  3. Provide fallback routing if the target entity is missing or unauthenticated.
- **Regression Prevention**: End-to-end integration test verifying deep-link resolution during cold-start launch.

---

## 5. Network & State Resilience Errors

### [ERR-NET-001] Indefinite Hanging Network Request
- **Category**: Network
- **Symptom**: Application spinner runs perpetually; user interface hangs indefinitely on unstable cellular or flaky Wi-Fi connections.
- **Root Cause**: Missing connection and socket read timeouts on HTTP client, allowing half-open TCP connections to linger indefinitely.
- **Diagnostic Command**: Simulate dropped packets or black-hole proxy on outbound endpoint.
- **Resolution**:
  1. Bind all fetch and HTTP requests to an `AbortController` with a 3-second connection timeout and 15-second read timeout.
  2. Implement user-facing retry button with bounded exponential backoff.
- **Regression Prevention**: Mock client test verifying request aborts and throws `TimeoutError` within configured deadline.

---

### [ERR-STATE-001] Stale Optimistic State Rollback Divergence
- **Category**: State
- **Symptom**: User executes an action (e.g. toggle favorite), optimistic state updates immediately, backend mutation fails, but UI remains in corrupted edited state.
- **Root Cause**: Mutation failure handler did not restore the pre-mutation snapshot or swallowed the error without notifying the state store.
- **Diagnostic Command**: Mock backend endpoint to return HTTP 500 and observe UI rollback behavior.
- **Resolution**:
  1. Capture `snapshot = currentState` immediately before applying optimistic update.
  2. In error catch handler, dispatch `setState(snapshot)` to cleanly rollback state.
  3. Display non-intrusive toast notification explaining mutation failure.
- **Regression Prevention**: Automated test verifying state snapshot restores on simulated network rejection.

---

## 6. Cloud & DevOps Errors

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

## 7. AI & LLM Errors

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
