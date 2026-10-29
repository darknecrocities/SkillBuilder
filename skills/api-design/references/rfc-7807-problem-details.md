# RFC 7807 Problem Details for HTTP APIs

Standardize machine-readable error responses across all REST and JSON APIs.

---

## 1. Canonical Schema

```json
{
  "type": "https://api.example.com/errors/resource-not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with ID 'usr_98124' could not be found.",
  "instance": "/v1/users/usr_98124",
  "code": "USER_NOT_FOUND",
  "trace_id": "req_876128491"
}
```

### Required Fields:
- **`type`** (URI reference): Unique identifier for the error type.
- **`title`** (string): Short, human-readable summary that does not change between occurrences.
- **`status`** (integer): Standard HTTP status code matching the response header.
- **`detail`** (string): Specific human-readable explanation of this occurrence.
- **`instance`** (URI reference): Specific endpoint or resource instance that generated the error.

### Custom Extensions:
- **`code`**: Machine-parseable uppercase error enum.
- **`trace_id`**: Correlation ID matching OpenTelemetry span context.
