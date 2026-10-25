---
name: observability
description: Observability and telemetry engineering skill. Enforces OpenTelemetry distributed tracing, structured JSON logging with correlation IDs, and health probes.
---

# Observability & Distributed Telemetry (`/observability`)

> **Philosophy**: *If it cannot be observed in production, it cannot be debugged. Correlate every log with a trace ID. Instrument every RPC boundary.*

This skill establishes production observability standards across backend microservices, serverless functions, background workers, and containerized platforms.

---

## 1. The Three Pillars of Telemetry

```mermaid
flowchart LR
    A["Inbound Request"] --> B["Inject Trace & Span IDs (W3C TraceContext)"]
    B --> C["Structured JSON Logging ({level, trace_id, message})"]
    C --> D["Metrics (Prometheus Counters / Histograms)"]
    D --> E["Distributed Traces (OpenTelemetry Spans)"]
```

### Pillar 1: Structured JSON Logging
- **Prohibited**: Unformatted raw `console.log("user logged in " + id)` or `print(f"Error: {e}")`.
- **Mandate**: Structured JSON output with timestamp, log level, correlation IDs, and contextual metadata:
```json
{
  "timestamp": "2026-10-25T20:30:00.000Z",
  "level": "INFO",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "service": "billing-service",
  "message": "Payment intent processed successfully",
  "customer_id": "cus_99182",
  "amount_cents": 4900
}
```

### Pillar 2: Standard Health & Readiness Probes
Every service must expose two distinct HTTP probe endpoints:
1. **`/healthz` (Liveness)**: Returns `200 OK` if the process is running and not deadlocked.
2. **`/readyz` (Readiness)**: Returns `200 OK` only when database connections and downstream dependencies are initialized.

### Pillar 3: OpenTelemetry Context Propagation
- Propagate incoming `traceparent` headers across outgoing HTTP or message queue boundaries.
- Record span exceptions and set span status to `Error` on unhandled failures.

---

## 2. Telemetry Standards Auditor CLI

Audit your codebase for structured logging patterns and healthcheck endpoints:
```bash
python3 skills/observability/scripts/verify_telemetry_standards.py --path .
```
