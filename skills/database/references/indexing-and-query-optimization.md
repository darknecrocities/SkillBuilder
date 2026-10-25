# Indexing & Query Optimization

Maximizing database throughput and minimizing latency with evidence-backed indexing.

---

## 1. Indexing Strategies
- **B-tree**: Default index for equality (`=`) and range queries (`<`, `<=`, `>`, `>=`, `BETWEEN`).
- **GIN (Generalized Inverted Index)**: For JSONB attributes, arrays, and full-text search (`tsvector`).
- **Composite Indexes**: Order matters (Equality First, Range Second):
  - Example: `WHERE tenant_id = 5 AND created_at > '2026-01-01'` -> `CREATE INDEX idx_tenant_created ON events (tenant_id, created_at);`

---

## 2. EXPLAIN ANALYZE Checklist
Run `EXPLAIN (ANALYZE, BUFFERS)` to diagnose slow queries:
- Look for `Seq Scan` on tables with > 10,000 rows.
- Verify `Rows Removed by Filter`: if high, an index filter is missing.
- Check `Buffers: shared hit=... read=...`: high `read` indicates disk I/O bottlenecks.
