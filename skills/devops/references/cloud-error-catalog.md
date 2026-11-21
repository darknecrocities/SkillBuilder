# Cloud & Container DevOps Error Catalog

> **Objective**: Rapid diagnosis of Docker build bloat, root-user failures, OOMKilled containers, and CI/CD permission errors.

---

## 1. Failure & Remediation Matrix

| Error Signature / Symptom | Root Cause | Production Remediation |
| :--- | :--- | :--- |
| **`Permission denied` when running as `USER 10001`** | Files copied before user switch remain `root`-owned, or app tries binding privileged port `< 1024` (`:80`/`:443`). | Copy with `COPY --chown=10001:10001`, bind unprivileged port `8080`, and use `WORKDIR /app`. |
| **`OOMKilled` (Exit Code 137)** | Node/Python memory exceeds container cgroup limit (`--max-old-space-size` unset or unbounded file read). | Stream large payloads, set Node `--max-old-space-size` to `75%` of container RAM limit, raise Cloud Run/K8s memory ceiling. |
| **Container image exceeds `1.5 GB`** | Shipping `node_modules` devDependencies, build compilers (`gcc`), or `.git` in final image. | Multi-stage Dockerfile (`builder` -> `node:22-alpine` / `distroless`), copy only runtime artifacts, maintain `.dockerignore`. |
| **Readiness probe flaps / cascade restarts** | `/healthz` liveness endpoint pings external DB, causing K8s/Cloud Run to kill pods during brief DB failover. | Split `/healthz` (process-only) from `/readyz` (dependency check with `1.5s` timeout). |
| **Exposed `GOOGLE_APPLICATION_CREDENTIALS` JSON** | Static service account key downloaded into repo or GitHub Secret. | Delete key immediately, rotate IAM binding, switch to **Workload Identity Federation (OIDC)**. |
