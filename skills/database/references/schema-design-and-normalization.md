# Schema Design, Normalization & Tenant Isolation Manual

> **Objective**: Model relational schemas with strong integrity constraints, multi-tenant isolation, and predictable evolution.

---

## 1. Non-Negotiable Schema Constraints

- **Primary Keys**: Use UUIDv7 (time-ordered, B-tree friendly) or `BIGINT GENERATED ALWAYS AS IDENTITY`; avoid random UUIDv4 on ultra-high-insert clustered tables where page splits hurt write throughput.
- **Database-Enforced Invariants**: Enforce `NOT NULL`, `UNIQUE`, `FOREIGN KEY ... ON DELETE RESTRICT/CASCADE`, and `CHECK` constraints (`price_cents >= 0`, `status IN ('draft','active','archived')`) directly in SQL DDL — never rely solely on client/API validation.
- **Temporal & Money Precision**:
  - Store timestamps as `TIMESTAMPTZ` (UTC).
  - Store currency exclusively in integer minor units (`amount_cents BIGINT`, `currency CHAR(3)`), **never** `FLOAT`/`DOUBLE`.

---

## 2. Normalization vs. Intentional Denormalization

1. **Default to 3NF**: Eliminate duplicate mutable strings (store `customer_id`, not `customer_email`, across 5 order tables).
2. **Justified Denormalization**: Snapshot immutable point-in-time facts (e.g., `unit_price_cents_at_purchase` on `order_items`) so historical invoices never mutate when catalog prices change.
3. **Tenant Scoping Column**: Include `tenant_id` on every tenant-owned table and lead composite primary/unique indexes with `tenant_id` (`PRIMARY KEY (tenant_id, id)` or `UNIQUE (tenant_id, slug)`).
4. **Soft Deletes (`deleted_at`)**: Prefer explicit `deleted_at TIMESTAMPTZ` + partial unique indexes (`WHERE deleted_at IS NULL`) for audit-critical entities, gating hard drops behind `/database` Sensitive Deletion Gate + SHA-256 single-slot backup (`manage_deduplicated_backup.py`).
