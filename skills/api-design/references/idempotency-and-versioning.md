# Idempotency Keys, API Versioning & Safe Retries Manual

> **Objective**: Guarantee safe network retries without duplicate charges/records and evolve APIs cleanly without breaking active mobile/web clients.

---

## 1. Idempotency-Key Lifecycle (`POST` / `PATCH`)

Accept `Idempotency-Key: <UUIDv4>` on all state-creating or payment endpoints:

| Existing Key State | Request Payload Hash | HTTP Response |
| :--- | :--- | :--- |
| **Not found** | Store key as `PENDING` (60s lock) | Execute handler, persist `status_code` + `body` (`24h` TTL), return result |
| **`PENDING`** | Any | `409 Conflict` (`"Request with this Idempotency-Key is currently processing"`) |
| **`COMPLETED`** | **Matches** original SHA-256 hash | Replay stored `status_code` + JSON response immediately |
| **`COMPLETED`** | **Differs** from original hash | `422 Unprocessable Entity` (`"Idempotency-Key reused with different payload"`) |

Never store idempotency state only in process RAM in multi-instance deployments — use Redis (`SET key val NX EX`) or a Postgres `idempotency_keys` table with unique `(tenant_id, key)`.

---

## 2. API Versioning & Non-Breaking Evolution

1. **Additive Changes (Non-Breaking)**: Adding optional response fields or optional request parameters with defaults requires no version bump.
2. **Breaking Changes**: Renaming fields, tightening constraints, or changing types requires a new explicit major prefix (`/v2/...`) and deprecation headers (`Deprecation: true`, `Sunset: <RFC 7231 date>`) on `/v1/...`.
3. **Never Leak Internal DB Schemas Directly**: Map internal table rows through explicit DTO serializers so column refactors never break API consumers.
