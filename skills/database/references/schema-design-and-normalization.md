# Schema Design & Relational Normalization

Core principles for robust schema design and data integrity.

---

## 1. Normalization & Integrity Constraints
- **Primary Keys**: Use UUIDv7 or prefixed KSUIDs (e.g. `usr_01H...`) for distributed systems to avoid sequential ID enumeration attacks while maintaining time-ordered index locality.
- **Foreign Keys**: Always specify `ON DELETE` behavior explicitly (`RESTRICT`, `CASCADE`, `SET NULL`). Avoid relying on implicit database defaults.
- **Check Constraints**: Enforce domain validation in the database engine (`CHECK (amount > 0)`, `CHECK (status IN ('draft', 'published'))`).

---

## 2. Timestamps & Soft Deletes
Every entity table must include audit timestamps:
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`

For soft deletes:
- Use `deleted_at TIMESTAMPTZ NULL`.
- Filter with partial indexes: `CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL;`
