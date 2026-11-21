# Zero-Downtime Expand / Contract Migrations Manual

> **Objective**: Evolve production database schemas safely alongside rolling deployments so old and new application code never break during migration windows.

---

## 1. The 4-Phase Expand / Contract Protocol

Never execute destructive `ALTER TABLE RENAME COLUMN`, `DROP COLUMN`, or `SET NOT NULL` directly while older app containers still serve requests:

| Phase | Database Change | Application Code | Safety Check |
| :--- | :--- | :--- | :--- |
| **1. Expand** | Add nullable new column / table (`ALTER TABLE users ADD COLUMN full_name TEXT;`) | Dual-write both old & new columns; read old | Single-slot SHA-256 backup verified (`manage_deduplicated_backup.py`) |
| **2. Backfill** | Batch backfill historical rows in throttled chunks (`LIMIT 1000` + sleep) | Dual-write continues; read new with fallback to old | Monitor replication lag & lock wait time |
| **3. Switch** | Add `NOT VALID` constraint + `VALIDATE CONSTRAINT` (non-blocking) | Read & write strictly new column | Deploy & verify all instances run new code |
| **4. Contract** | Drop old column/table only after explicit user confirmation (`Sensitive Deletion Gate`) | Clean single-column code | Backup digest logged before `DROP` |

---

## 2. Lock-Safety Guardrails (PostgreSQL)
- Always set `SET lock_timeout = '3s';` at the top of migration scripts so a blocked DDL statement aborts cleanly instead of queuing every normal `SELECT`/`INSERT` behind it.
- Use `ADD CONSTRAINT ... CHECK (...) NOT VALID` followed by `VALIDATE CONSTRAINT` to enforce invariants without holding an `ACCESS EXCLUSIVE` table lock during full scans.
