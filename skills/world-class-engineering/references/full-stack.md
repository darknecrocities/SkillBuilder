# Full-Stack Engineering Standards

This reference guides the complete application lifecycle across Frontend, Backend, Databases, and External Integrations.

---

## 1. Frontend Engineering

### Component Architecture & State
- **Decouple UI from Business Logic**: Presentational components should focus purely on layout, styles, and rendering. Extract data-fetching, state transitions, and business calculations into custom hooks or state controllers.
- **State Granularity**: Keep state as local as possible. Do not lift state into global stores (Redux, Zustand, React Context) unless multiple disconnected parts of the tree genuinely require synchronization.
- **The 4 Essential UI States**: Every asynchronous component must explicitly handle:
  1. *Loading / Pending*: Skeletons or spinners without content shifting.
  2. *Empty*: Meaningful empty-state graphics and actionable guidance.
  3. *Error*: User-friendly error message with recovery/retry options.
  4. *Success / Content*: Rendered data with smooth transitions.

### Accessibility (a11y) & Responsiveness
- Use semantic HTML (`<nav>`, `<main>`, `<article>`, `<button>`, `<dialog>`) instead of generic `<div>` or `<span>` click handlers.
- Ensure all interactive elements have visible `:focus-visible` outlines, accessible names (`aria-label` or visible text), and support full keyboard navigation (Tab, Enter, Space, Escape).
- Color contrast must meet WCAG AA standards (minimum 4.5:1 for normal text).
- Design responsive layouts with fluid grids, `flex`, or `grid`; test on small mobile, tablet, and desktop viewports.

---

## 2. Backend Engineering

### API Design & Contracts
- **Contract-First**: Define explicit schemas for all requests and responses (OpenAPI, JSON Schema, Protobuf).
- **Consistent Response Envelopes**: Maintain uniform structures across endpoints:
  ```json
  {
    "data": { "id": "usr_123", "name": "Alice" },
    "error": null,
    "meta": { "requestId": "req_abc", "timestamp": "2026-10-14T17:30:00Z" }
  }
  ```
- **Error Responses**: Return standardized error payloads with machine-readable error codes (e.g., `USER_NOT_FOUND`, `INVALID_REQUEST_PAYLOAD`) and appropriate HTTP status codes (400, 401, 403, 404, 409, 422, 500).

### Security, Auth, & Invariants
- **Never Trust the Client**: Frontend validation is for user experience only. The backend must enforce all authentication, authorization (RBAC/ABAC), and schema validation independently.
- **Structured Logging**: Emit logs in JSON format including correlation IDs (`requestId`, `traceId`), timestamp, severity, and context. Never log sensitive credentials, passwords, or PII.
- **Timeouts & Cancellations**: Always configure explicit socket and execution timeouts for incoming requests and outgoing downstream calls. Propagate context cancellation (e.g., Go `context.Context`, Node.js `AbortController`).
- **Idempotency**: Use idempotency keys (headers like `Idempotency-Key: <uuid>`) for non-idempotent operations (POST /payments, refunds) to guarantee duplicate requests do not cause double-charging or corrupt state.

---

## 3. Database Engineering

### Schema & Index Design
- **Explicit Constraints**: Enforce data integrity at the database layer using `NOT NULL`, `UNIQUE`, foreign key constraints (`ON DELETE RESTRICT/CASCADE`), and `CHECK` constraints.
- **Evidence-Based Indexing**: Add indexes based on actual query patterns, joins, and `WHERE` filters. Avoid indexing columns with low cardinality (e.g., boolean flags) unless part of a composite index.
- **Keys**: Prefer standard UUIDv7 or ULID for distributed identifiers where time-ordering is valuable, or auto-incrementing bigints for strictly internal relational tables.

### Safe Migrations & Transactions
- **Zero-Downtime Multi-Phase Migrations**:
  - Phase 1: Add new column as nullable.
  - Phase 2: Deploy application code that reads and dual-writes to old and new columns.
  - Phase 3: Backfill data from old column to new column.
  - Phase 4: Deploy application code that only reads new column.
  - Phase 5: Drop old column.
- **Never Execute Destructive DDL Without Backups**: Never drop columns or tables in production without explicit approval and an active point-in-time recovery backup.
- **Pagination**: Always paginate large result sets using cursor-based pagination (`WHERE id > :cursor LIMIT :limit`) over offset pagination (`OFFSET 10000`) for high-volume tables.

---

## 4. Resilient External API Integrations

- **Typed SDKs/Clients**: Encapsulate third-party API communication behind typed adapter classes or interfaces.
- **Bounded Exponential Backoff**: Implement retries with jitter only for transient errors (HTTP 429, 500, 502, 503, 504, connection timeouts).
- **Never Retry Non-Idempotent Failures Blindly**: Do not retry an unconfirmed `POST` request without an idempotency key or verification that the initial operation did not commit.
- **Circuit Breakers**: When a downstream service experiences sustained failure, trip the circuit breaker to prevent cascading thread pool exhaustion and fail fast gracefully.
