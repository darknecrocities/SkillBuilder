# Indexing, EXPLAIN ANALYZE & N+1 Query Elimination Manual

> **Objective**: Eliminate sequential full-table scans, lock-blocking index builds, and N+1 ORM loops under production traffic.

---

## 1. Index Selection & Composite Ordering

| Query Pattern | Optimal Index Type | Ordering Rule |
| :--- | :--- | :--- |
| `WHERE tenant_id = $1 AND status = $2 ORDER BY created_at DESC` | Composite B-Tree `(tenant_id, status, created_at DESC)` | Equality columns **first**, range/sort columns **last** |
| Partial active-only lookup (`WHERE deleted_at IS NULL`) | Partial B-Tree `CREATE INDEX ... WHERE deleted_at IS NULL` | Shrinks index footprint by omitting historical rows |
| JSONB attribute lookup (`metadata @> '{"plan":"pro"}'`) | `GIN` index (`USING GIN (metadata jsonb_path_ops)`) | Avoid indexing high-cardinality unique IDs inside GIN |
| Full-text / fuzzy search | Postgres `GIN (to_tsvector(...))` or SQLite `FTS5` | Never run leading-wildcard `LIKE '%foo%'` on unindexed text |

---

## 2. Production `EXPLAIN (ANALYZE, BUFFERS)` Audit

Before shipping new queries on tables `> 10k` rows, inspect execution plans:
- **Red Flags**: `Seq Scan` on large tables, `Rows Removed by Filter: 98000`, `Nested Loop` exploding over thousands of inner scans, `Sort Method: external merge Disk`.
- **Zero-Lock Creation**: Always run `CREATE INDEX CONCURRENTLY` on live PostgreSQL tables so writes are never blocked (`ALTER TABLE` index locks take production offline).

---

## 3. Eliminating N+1 Queries

```typescript
// BAD: 1 query for orders + N queries for customer rows
for (const order of orders) {
  order.customer = await db.query("SELECT * FROM customers WHERE id = $1", [order.customerId]);
}

// GOOD: Single batched lookup or SQL JOIN scoped to tenant
const ids = [...new Set(orders.map((o) => o.customerId))];
const customers = await db.query(
  "SELECT id, name FROM customers WHERE tenant_id = $1 AND id = ANY($2::uuid[])",
  [tenantId, ids]
);
```
