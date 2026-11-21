# Backend Resilience, Rate Limiting & Middleware Pipeline

> **Objective**: Protect backend services from slowloris hangs, retry storms, duplicate mutations, and cascading downstream failures.

---

## 1. Ingress Middleware Execution Order

Always mount middleware in strict defense-in-depth order:
1. **Correlation ID (`X-Correlation-ID`)**: Generate or preserve valid UUIDv4 trace header on request ingress.
2. **Slowloris & Body Caps**: Enforce `3s` handshake / `15s` body timeout and `100 KB` JSON payload ceiling (`10 MB` explicit multipart route only).
3. **CORS Allowlist**: Explicit origin list; never combine `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`.
4. **Rate Limiter**: Token bucket / sliding window per IP (`5–10/min` on `/auth/*`) and per tenant (`100–300/min` on APIs) returning `429` + `Retry-After`.
5. **Authentication & Tenant Context**: Verify JWT/session signature and attach typed `{ userId, tenantId, role }`.
6. **RFC 7807 Global Error Boundary**: Catch unhandled domain/transport errors, log full trace internally with correlation ID, and emit sanitized Problem Details JSON.

---

## 2. Circuit Breaker & Bounded Retry Rules

| Downstream Condition | Retry Policy | Circuit Breaker |
| :--- | :--- | :--- |
| **`GET` / `HEAD` / Idempotent `PUT` + `502/503/504`** | Max 3 attempts, exponential backoff + full jitter | Open circuit after `50%` failures over 20 requests (`30s` half-open cooldown) |
| **`POST` without `Idempotency-Key`** | **Never retry automatically** (risks double charges/writes) | Fail fast with `503` + correlation ID |
| **`400` / `401` / `403` / `404` / `422`** | **Never retry** | Return client error immediately |
