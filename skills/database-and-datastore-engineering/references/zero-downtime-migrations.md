# Zero-Downtime Database Migrations

Techniques for deploying schema changes without table locking or service disruption.

---

## 1. Dangerous vs Safe Operations

| Operation | Risk Level | Safe Pattern |
| :--- | :--- | :--- |
| `ALTER TABLE ... ADD COLUMN ... NOT NULL` | Critical (Table Lock) | Add column as nullable or with `DEFAULT` in modern PG (v11+). |
| `ALTER TABLE ... DROP COLUMN` | Critical (Breaks active code) | Deploy code ignoring column first; drop column in next release. |
| `CREATE INDEX ...` | High (Blocks writes) | Use `CREATE INDEX CONCURRENTLY`. |
| `ALTER TABLE ... RENAME COLUMN` | Critical (Immediate failure) | Add new column -> dual-write -> backfill -> read new -> drop old. |

---

## 2. PostgreSQL Lock Timeout Protection
Always set statement timeouts on migration sessions to avoid queueing locks behind long transactions:

```sql
SET lock_timeout = '3s';
SET statement_timeout = '30s';

-- Perform safe migration step
ALTER TABLE users ADD COLUMN phone_number VARCHAR(30) NULL;
```
