# Database Hygiene & Migration Error Catalog

> **Objective**: Rapid diagnosis of migration locks, SQLite contention, backup spam, and injection vulnerabilities.

---

## 1. Failure & Remediation Matrix

| Error / Anti-Pattern | Root Cause | Remediation |
| :--- | :--- | :--- |
| **`SQLITE_BUSY: database is locked`** | Default rollback journal mode or missing busy timeout under concurrent readers/writers. | Enable `PRAGMA journal_mode = WAL;` and `PRAGMA busy_timeout = 5000;`. |
| **Production API outage during `ADD COLUMN ... DEFAULT`** | Older PG/MySQL rewrite or queued `ACCESS EXCLUSIVE` lock behind long analytical query. | Set `SET lock_timeout = '3s';` and follow 4-phase Expand/Contract protocol. |
| **Duplicate `.bak.1`, `.bak.2`, `dump_copy.sql` spam** | Agents creating unhashed timestamp backups on every turn regardless of state changes. | Use single-slot SHA-256 backup ledger (`manage_deduplicated_backup.py`). |
| **Data loss from unconditioned `DELETE` / `DROP`** | Missing human confirmation gate or forgotten `WHERE` clause. | Halt for explicit user confirmation + backup SHA-256 hash; require `WHERE` + `tenant_id`. |
| **SQL Injection (`UNSAFE-SQL-INTERPOLATION`)** | f-strings or template literals (`SELECT * FROM users WHERE id = '${id}'`). | Exclusively pass parameterized bindings (`$1`, `?`) and whitelist dynamic `ORDER BY` columns via enum map. |
