# API Idempotency & Versioning Standards

---

## 1. Idempotency Key Handling (`Idempotency-Key`)

For mutating operations (`POST /payments`, `POST /orders`, `POST /refunds`), clients supply a unique `Idempotency-Key` header:

```http
POST /v1/payments HTTP/1.1
Host: api.example.com
Idempotency-Key: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d
Content-Type: application/json

{"amount": 4900, "currency": "USD"}
```

### Server Flow:
1. Check Redis/database for `idempotency:<client_id>:<key>`.
2. If state is `PENDING`, return HTTP `409 Conflict` (request in progress).
3. If state is `COMPLETED`, replay the cached HTTP status, headers, and response payload.
4. If not found, acquire lock with TTL (e.g. 24 hours), execute mutation, cache output, and release lock.

---

## 2. API Versioning Conventions

- **URI Versioning**: Use `/v1/`, `/v2/` prefixes for breaking structural changes.
- **Additive Evolution**: Add optional fields without incrementing major version numbers.
- **Deprecation Header**: Emit `Deprecation: @<timestamp>` and `Sunset: <date>` for expiring endpoints.
