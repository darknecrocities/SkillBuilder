# RFC 7807 Problem Details Error Standard (`application/problem+json`)

> **Objective**: Standardize all 4xx/5xx error responses across microservices and API routes so clients handle failures deterministically without leaking server internals.

---

## 1. Canonical Payload Structure

Always serve errors with `Content-Type: application/problem+json`:

```json
{
  "type": "https://api.example.com/problems/validation-failed",
  "title": "Request Validation Failed",
  "status": 400,
  "detail": "One or more input fields failed schema validation.",
  "instance": "/v1/projects/proj_123/tasks",
  "code": "ERR_VALIDATION_FAILED",
  "correlation_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "invalid_params": [
    { "field": "title", "reason": "Must contain between 1 and 200 characters" }
  ]
}
```

---

## 2. Production Security & Serialization Rules

1. **Zero Stack Leaks in Production**: On `500 Internal Server Error`, log `err.stack`, SQL state, and request metadata internally tagged with `correlation_id`, but return **only** generic `"An unexpected internal error occurred"` + `correlation_id` to the caller.
2. **Machine-Readable `code`**: Never force frontend i18n layers to regex-match English `detail` strings; always emit stable `code` enums (`ERR_TOKEN_EXPIRED`, `ERR_CONCURRENCY_CONFLICT`, `ERR_QUOTA_EXCEEDED`).
3. **Rate-Limit Headers on `429`**: Always include `Retry-After` (integer seconds) alongside `RateLimit-Remaining: 0`.
4. **Validation Aggregation**: Return *all* invalid fields in `invalid_params` in one pass rather than failing on the first field only.
