# Structured JSON Logging & Correlation IDs

Never output unstructured string lines (`console.log("User logged in")`). Emit machine-parseable structured JSON objects to stdout.

---

## 1. Canonical Log Record Schema

```json
{
  "timestamp": "2026-10-29T19:40:00.123Z",
  "level": "INFO",
  "message": "User session authenticated",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "correlation_id": "req_892138",
  "service": "auth-service",
  "environment": "production",
  "user_id": "usr_99182",
  "duration_ms": 14.2
}
```

---

## 2. PII Sanitization Standards

- Automatically mask `Authorization` tokens, `password`, `ssn`, and credit card numbers.
- Never log raw request bodies on endpoints handling authentication or payment.
