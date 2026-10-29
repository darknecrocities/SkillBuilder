# Google Cloud Run Production Standards

---

## 1. Container Configuration

- **Non-Root User**: Build with non-root user (`USER 10001` or `USER node`).
- **Port Binding**: Listen on the port defined by `PORT` environment variable (default 8080).
- **Concurrency**: Set concurrency between 40 and 80 for Node.js / Go / FastAPI workloads.
- **CPU Allocation**: Allocate CPU only during request processing (`--no-cpu-throttling` false) unless running background tasks.

---

## 2. Health & Startup Probes

Define startup and liveness probes in `service.yaml`:
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 15
startupProbe:
  httpGet:
    path: /readyz
    port: 8080
  failureThreshold: 10
  periodSeconds: 3
```
