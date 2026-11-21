# Connection Pooling, ACID Transactions & Deadlock Prevention

> **Objective**: Prevent connection-pool exhaustion, dirty reads, lost updates, and cross-request transaction leaks.

---

## 1. Pool Sizing & Timeout Invariants

- **PostgreSQL Pool Sizing**: Keep per-instance app pools small (`max: 10–20` connections) and front serverless workloads (Cloud Run / Vercel / Lambda) with PgBouncer or Supabase Supavisor in transaction pooling mode.
- **SQLite Production Pragmas (WAL Mode)**:
  ```sql
  PRAGMA journal_mode = WAL;
  PRAGMA synchronous = NORMAL;
  PRAGMA busy_timeout = 5000;
  PRAGMA foreign_keys = ON;
  ```
- **Mandatory Timeouts**: Configure `connectionTimeoutMillis: 3000`, `idleTimeoutMillis: 30000`, and `statement_timeout = 5000` (5s max query budget).

---

## 2. Transaction Boundaries & Isolation Levels

1. **Keep Transactions Short**: Never hold an open DB transaction while awaiting external HTTP calls, LLM APIs, or email/webhook delivery — compute/fetch externally first, then commit atomically.
2. **Always Release in `finally`**: Acquire pooled clients via `try { await client.query('BEGIN'); ... await client.query('COMMIT'); } catch (err) { await client.query('ROLLBACK'); throw err; } finally { client.release(); }`.
3. **Deadlock Avoidance**: Lock multiple rows/accounts in **deterministic ascending ID order** (`ORDER BY id ASC FOR UPDATE`) so concurrent workers never form circular waits.
4. **Isolation Choice**: Use `READ COMMITTED` + atomic `UPDATE ... WHERE balance >= $1` or optimistic `version = version + 1` checks; escalate to `SERIALIZABLE` only with automatic retry on `40001` serialization failures.
