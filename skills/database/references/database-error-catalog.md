# Database & Datastore Error Catalog

Common database errors, deadlocks, and migration traps with actionable remediations.

---

### [DB-ERR-001] Missing Index on Foreign Key
- **Symptom**: `DELETE FROM users WHERE id = $1` takes 12 seconds; full table scan observed on `orders` table.
- **Root Cause**: Foreign key `orders.user_id` lacks an index. Deleting a user forces PostgreSQL to scan the entire `orders` table to check referential constraints.
- **Remediation**:
  ```sql
  CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);
  ```

---

### [DB-ERR-002] Deadlock Detected on Concurrent Multi-Row Updates
- **Symptom**: `ERROR: deadlock detected (SQLSTATE 40P01)`.
- **Root Cause**: Transaction A updates user 1 then user 2; Transaction B updates user 2 then user 1 concurrently.
- **Remediation**:
  1. Enforce deterministic lock ordering: always sort IDs in ascending order in application code before locking rows (`SELECT ... FOR UPDATE`).
  2. Implement exponential backoff retry for error code `40P01`.

---

### [DB-ERR-003] Connection Pool Starvation (Remaining connection slots reserved)
- **Symptom**: `FATAL: remaining connection slots are reserved for non-replication superuser connections`.
- **Root Cause**: Microservice horizontally autoscales to 20 instances, each configured with 20 connections, surpassing the PostgreSQL `max_connections` ceiling.
- **Remediation**:
  1. Reduce per-instance connection pool max size to 3–5.
  2. Deploy PgBouncer in `pool_mode = transaction`.
