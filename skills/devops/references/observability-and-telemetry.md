# Container Observability, Health Probes & Telemetry Wiring

> **Objective**: Ensure every deployed container exposes deterministic health probes, structured JSON logs, and OpenTelemetry traces without leaking sensitive headers.

---

## 1. Liveness vs. Readiness Probe Contract

| Probe Endpoint | Purpose | Failure Behavior |
| :--- | :--- | :--- |
| **`GET /healthz` (Liveness)** | Confirms process event loop / runtime is responsive (`200 { "status": "alive" }`). | Orchestrator restarts container if hung. **Do NOT query external DBs here** (avoids cascading restarts on transient DB blips). |
| **`GET /readyz` (Readiness)** | Verifies critical local dependencies (DB pool `SELECT 1`, Redis ping, `.riv`/assets mounted) within `1.5s` timeout. | Load balancer removes pod from rotation (`503`) until dependency recovers. |

---

## 2. Structured Container Logging & Trace Propagation

- **JSON to `stdout`**: Write single-line structured JSON (`timestamp`, `level`, `message`, `service`, `trace_id`, `span_id`, `correlation_id`, `duration_ms`) to `stdout`/`stderr`; never write rotating log files inside ephemeral containers.
- **Scrub Sensitive Fields**: Redact `authorization`, `cookie`, `set-cookie`, `password`, `api_key`, and `token` keys before serializing logs.
- **Graceful Telemetry Flush**: Call `sdk.shutdown()` / `tracerProvider.forceFlush()` inside the `SIGTERM` shutdown hook so final error spans ship before container exit.
