# Structured JSON Logging, Correlation IDs & PII Scrubbing

> **Objective**: Make production failures instantly searchable via structured JSON logs while guaranteeing zero credentials or raw PII ever leak into log aggregators.

---

## 1. Canonical JSON Log Schema

Emit single-line JSON to `stdout`/`stderr` (never multi-line pretty-printed blocks in production):

```json
{
  "timestamp": "2026-11-21T12:45:03.182Z",
  "level": "error",
  "service": "api-gateway",
  "event": "PAYMENT_PROVIDER_TIMEOUT",
  "correlation_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "tenant_id": "ten_01J9X",
  "duration_ms": 15004,
  "error_code": "ERR_UPSTREAM_TIMEOUT"
}
```

---

## 2. Mandatory PII & Secret Redaction Rules

1. **Automated Key Scrubbing**: Configure logger redact lists (`pino` `redact`, Python `structlog` processor) to mask `password`, `token`, `secret`, `authorization`, `cookie`, `api_key`, `ssn`, and `credit_card` recursively before serialization.
2. **No `console.log()` on `stdio` MCP Servers**: When building `stdio` MCP tools, route all structured JSON logs to `stderr` so JSON-RPC frames on `stdout` stay clean.
3. **Never Log Raw User Files or Full Prompts**: Log byte counts, SHA-256 checksums, and document IDs instead of dumping raw file contents or prompts.
4. **Canonical Error Logging**: Log full internal error details once at the boundary handler (`correlation_id` attached), avoiding noisy duplicate `console.error` logs across every intermediate catch block.
