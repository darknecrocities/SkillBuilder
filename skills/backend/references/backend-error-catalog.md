# Backend Systems Error & Concurrency Failure Catalog

> **Objective**: Fast triage and root-cause remediation for database deadlocks, auth races, unhandled rejections, and timeout cascades.

---

## 1. Failure Matrix & Root-Cause Fixes

| Error Signature / Symptom | Underlying Root Cause | Deterministic Fix |
| :--- | :--- | :--- |
| **Double charge / duplicate entity on slow mobile network** | Non-idempotent `POST` retried by client without `Idempotency-Key`. | Require `Idempotency-Key` stored in Redis/Postgres unique constraint (`PENDING`/`COMPLETED`). |
| **Lost update on concurrent balance/counter writes** | Read-modify-write in application memory without row lock or version check. | Use atomic SQL (`SET balance = balance - $1 WHERE id = $2 AND balance >= $1`) or optimistic `version = version + 1`. |
| **Connection pool exhausted under traffic spike** | Missing `statement_timeout`, leaked transaction on thrown error, or `N+1` queries inside loop. | Wrap transactions in `try/finally`, set `statement_timeout = 5000ms`, batch queries (`WHERE id = ANY($1)`). |
| **Silent 500 / Hanging Express/FastAPI request** | Swallowed `catch (e) {}` or missing `next(err)` / unhandled async task. | Remove empty catches, route errors to RFC 7807 handler, enforce `SIGTERM` pool drain. |
| **Cross-tenant record read (BOLA/IDOR)** | Query filters only by `WHERE id = $1`. | Scope every read/mutation with `WHERE id = $1 AND tenant_id = $2`. |
| **FastAPI blocking event loop (`10x` latency)** | Calling synchronous `requests.get()` or heavy CPU loop inside `async def` route. | Use `httpx.AsyncClient` for async I/O or regular `def` / `run_in_threadpool` for blocking calls. |
