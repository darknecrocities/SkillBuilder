# API Design, REST Conventions & Cursor Pagination Manual

> **Objective**: Author predictable, backward-compatible REST and RPC API contracts with strict schemas and O(1) cursor pagination.

---

## 1. Resource Naming & HTTP Verb Semantics

- Use plural noun collections (`/v1/projects`, `/v1/projects/{projectId}/tasks`), never verb endpoints (`/v1/getTasks`) except explicit state transitions (`/v1/invoices/{id}/finalize`).
- **Response Shapes**:
  - `POST` creation returns `201 Created` + `Location: /v1/projects/{id}` + created resource JSON.
  - `DELETE` returns `204 No Content` (empty body) or `200 OK` with soft-delete tombstones.
  - `PATCH` applies partial updates (JSON Merge Patch); `PUT` replaces full state idempotently.

---

## 2. Keyset (Cursor) Pagination Over `OFFSET`

`OFFSET 50000` forces Postgres/SQLite to scan and discard 50,000 rows per request and drifts under concurrent inserts. Always use opaque cursor pagination on indexed `(created_at, id)` tuples:

```sql
SELECT id, title, created_at
FROM tasks
WHERE tenant_id = $1
  AND (created_at, id) < ($2, $3)
ORDER BY created_at DESC, id DESC
LIMIT $4;
```

```json
{
  "data": [ ... ],
  "page": {
    "next_cursor": "eyJjcmVhdGVkX2F0IjoiMjAyNi0xMS0yMSIsImlkIjoiOTgxIn0=",
    "has_more": true
  }
}
```

---

## 3. Contract-First Validation (`OpenAPI 3.1` + `Zod` / `Pydantic v2`)
- Reject unknown fields on mutation payloads (`z.object(...).strict()` / `extra="forbid"`) so client typos never fail silently.
- Maintain OpenAPI 3.1 examples for both `2xx` success and `4xx`/`5xx` `application/problem+json` error envelopes.
