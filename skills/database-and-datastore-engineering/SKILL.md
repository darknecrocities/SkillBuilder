---
name: database-and-datastore-engineering
description: Architect, implement, and maintain resilient relational and NoSQL databases, zero-downtime schema migrations (expand/contract), index optimization, and connection pooling.
---

# Database & Datastore Engineering

> **Role**: Principal Database Architect & Data Engineer  
> **Philosophy**: *Data is the foundation. Index intentionally. Migrate without downtime. Guard ACID integrity.*

This skill establishes database architecture and operational discipline across PostgreSQL, SQLite, Google Cloud SQL, Spanner, Redis, and vector stores. It enforces relational integrity, non-blocking migrations, composite indexing, and connection pool hygiene.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/schema-design-and-normalization.md](references/schema-design-and-normalization.md) | Relational constraints, foreign keys, enums, soft deletes vs hard deletes. |
| **Reference** | [references/zero-downtime-migrations.md](references/zero-downtime-migrations.md) | Expand-and-contract migration strategy, non-blocking indexes (`CONCURRENTLY`). |
| **Reference** | [references/indexing-and-query-optimization.md](references/indexing-and-query-optimization.md) | B-tree, GIN indexes, EXPLAIN ANALYZE interpretation, eliminating N+1 queries. |
| **Reference** | [references/connection-pooling-and-transactions.md](references/connection-pooling-and-transactions.md) | PgBouncer configuration, isolation levels, lock minimization. |
| **Reference** | [references/database-error-catalog.md](references/database-error-catalog.md) | Catalog of database errors: deadlocks, pool exhaustion, lock timeouts. |
| **Template** | [templates/migration_expand_contract.sql](templates/migration_expand_contract.sql) | Production 3-step zero-downtime SQL migration template. |
| **Template** | [templates/drizzle_schema_template.ts](templates/drizzle_schema_template.ts) | Production Drizzle ORM schema with relations, indexes, and timestamps. |
| **Utility** | [scripts/verify_database_hygiene.py](scripts/verify_database_hygiene.py) | CLI auditor checking migrations for missing FK indexes and hazardous locks. |

---

## 2. Core Database Invariants

### 1. Zero-Downtime Expand-and-Contract Migrations
- Never rename a column or drop a table in a single migration while an application is running.
- Use the 3-step **Expand and Contract** protocol:
  1. **Expand**: Add the new column/table with nullable/default constraints. Deploy code writing to both old and new.
  2. **Backfill**: Migrate historical records in batches with throttled queries.
  3. **Contract**: Switch code to read exclusively from the new column/table. Drop the deprecated column in a subsequent deploy.

### 2. Foreign Key Indexing Mandate
- Every Foreign Key column (`*_id`) used in joins or lookups must have an explicit B-tree index. Missing FK indexes cause full table scans during joins and cascades.

### 3. Non-Blocking Index Creation in Production
- In PostgreSQL, always use `CREATE INDEX CONCURRENTLY` in production environments to avoid exclusive table read/write locks.

### 4. Connection Pool Hygiene
- Never open unbounded database connections. Configure pooling (e.g. PgBouncer or connection pool sizes = `(2 * CPU_CORES) + effective_spindle_count`).
- Keep transactions short: perform heavy calculations and network I/O outside database transactions.

---

## 3. Automation Tool: Database Hygiene Verifier

Audit SQL migration scripts for hazardous locks or missing indexes:
```bash
python3 scripts/verify_database_hygiene.py --path migrations/
```
