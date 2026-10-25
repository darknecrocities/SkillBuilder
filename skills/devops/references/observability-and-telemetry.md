# Observability, Structured Logging & OpenTelemetry

Standards for instrumenting cloud workloads for high observability.

---

## 1. Structured JSON Logging Format
In production, emit single-line JSON logs to stdout:

```json
{
  "timestamp": "2026-10-20T00:15:30.123Z",
  "severity": "INFO",
  "message": "User authenticated successfully",
  "logging.googleapis.com/trace": "projects/my-project/traces/a1b2c3d4e5f6",
  "http_request": {
    "request_method": "POST",
    "request_url": "/api/v1/auth/login",
    "status": 200,
    "latency": "0.045s"
  },
  "user_id": "usr_98765"
}
```

---

## 2. Liveness vs Readiness Probes
- **Liveness (`/healthz`)**: Verifies the HTTP server is alive and not deadlocked. If it fails, the container orchestrator restarts the pod.
- **Readiness (`/readyz`)**: Verifies the service can accept incoming traffic (database pool connected, caches warm). If it fails, traffic is diverted without restarting the container.
