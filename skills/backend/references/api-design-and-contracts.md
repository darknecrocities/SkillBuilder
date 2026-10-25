# API Design & RESTful Contracts

Standards for designing predictable, type-safe, and scalable web APIs.

---

## 1. RESTful URL & Verb Conventions

| Operation | HTTP Verb | Path Pattern | Success Code | Idempotent |
| :--- | :--- | :--- | :--- | :--- |
| List entities | `GET` | `/api/v1/workspaces` | `200 OK` | Yes |
| Fetch entity | `GET` | `/api/v1/workspaces/:id` | `200 OK` | Yes |
| Create entity | `POST` | `/api/v1/workspaces` | `201 Created` | No (unless keyed) |
| Replace entity | `PUT` | `/api/v1/workspaces/:id` | `200 OK` | Yes |
| Partial update | `PATCH` | `/api/v1/workspaces/:id` | `200 OK` | No / Yes |
| Delete entity | `DELETE` | `/api/v1/workspaces/:id` | `204 No Content` | Yes |

---

## 2. Cursor-Based Pagination
Prefer cursor-based pagination over offset pagination for high-volume datasets:

```json
{
  "data": [
    { "id": "item_123", "name": "Project Alpha" }
  ],
  "pagination": {
    "next_cursor": "eyJpZCI6Iml0ZW1fMTIzIn0=",
    "has_more": true,
    "limit": 20
  }
}
```
