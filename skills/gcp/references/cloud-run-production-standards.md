# Cloud Run Production Standards, Scaling & Cold-Start Tuning

> **Objective**: Configure Cloud Run services for fast cold starts, predictable concurrency, VPC egress hygiene, and bounded downstream DB load.

---

## 1. Concurrency, Scaling & Timeout Calibration

| Setting | Production Standard | Rationale |
| :--- | :--- | :--- |
| **Port Contract** | Listen on `process.env.PORT \|\| 8080` bound to `0.0.0.0` | Cloud Run routes HTTP/gRPC exclusively via `$PORT` |
| **Concurrency** | `80` for async I/O (Node/FastAPI async); `1–4` for CPU/ML inference | Prevents OOM and event-loop starvation |
| **Max Instances** | Explicit cap (`max-instances=20`) proportional to DB pool size | Stops traffic spikes from exhausting Cloud SQL connections |
| **Min Instances** | `min-instances=1` on latency-critical user APIs (`0` on batch workers) | Eliminates cold starts on user-facing p95 paths |
| **CPU Allocation** | Request-only billing for HTTP APIs; always-allocated for background queues | Never run unawaited background promises after HTTP response returns when CPU throttles! |

---

## 2. Cloud SQL, Pub/Sub & Graceful Shutdown
- Connect Cloud Run to Cloud SQL over **Auth Proxy / Unix Socket** (`/cloudsql/<INSTANCE_CONNECTION_NAME>`) or Private VPC — never expose `0.0.0.0/0` public DB ingress.
- Ensure Pub/Sub push handlers return `2xx` **only** after durable persistence succeeds, enabling automatic dead-letter topic routing after `max_delivery_attempts = 5`.
- Catch `SIGTERM` (Cloud Run gives `10s` before `SIGKILL`) to drain HTTP connections and close DB pools cleanly.
