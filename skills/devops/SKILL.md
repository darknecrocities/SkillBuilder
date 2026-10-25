---
name: devops
description: Architect, implement, and maintain secure cloud infrastructure on GCP/AWS, multi-stage non-root Docker containers, Terraform IaC, CI/CD pipelines, and OpenTelemetry observability.
---

# Cloud, DevOps & Infrastructure Engineering (`/devops`)

> **Role**: Principal Cloud & SRE / Platform Engineer  
> **Philosophy**: *Infrastructure as Code. Principle of least privilege. Distroless non-root containers. Comprehensive telemetry.*

This skill establishes cloud infrastructure and DevOps discipline across Google Cloud Platform (GCP), AWS, Docker, Kubernetes, and GitHub Actions. It enforces multi-stage containerization, non-root security contexts, declarative IaC, automated 5-gate CI/CD pipelines, and structured telemetry.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/cloud-architecture-and-gcp.md](references/cloud-architecture-and-gcp.md) | GCP Cloud Run, GKE, IAM least-privilege roles, Secret Manager. |
| **Reference** | [references/container-security-and-distroless.md](references/container-security-and-distroless.md) | Multi-stage builds, non-root security (`USER 10001`), minimal base images. |
| **Reference** | [references/observability-and-telemetry.md](references/observability-and-telemetry.md) | Structured JSON logging, OpenTelemetry distributed tracing, metrics. |
| **Reference** | [references/ci-cd-pipelines.md](references/ci-cd-pipelines.md) | 5-gate GitHub Actions CI pipeline architecture. |
| **Reference** | [references/cloud-error-catalog.md](references/cloud-error-catalog.md) | Catalog of cloud errors: OOMKilled, CrashLoopBackOff, IAM permissions. |
| **Template** | [templates/github_actions_reusable_workflow.yml](templates/github_actions_reusable_workflow.yml) | Production GitHub Actions CI/CD pipeline template. |
| **Template** | [templates/cloud_run_service.tf](templates/cloud_run_service.tf) | Production Terraform manifest for GCP Cloud Run with Secret Manager. |
| **Utility** | [scripts/verify_container_security.py](scripts/verify_container_security.py) | CLI auditor for Dockerfile security guardrails and non-root users. |

---

## 2. Core Cloud & Container Invariants

### 1. Multi-Stage Non-Root Containerization
- **Separate Build from Runtime**: The final production stage must contain only compiled artifacts and runtime dependencies (e.g. `gcr.io/distroless/nodejs20-debian12`, `alpine`, or `slim`).
- **Never Run as Root**: Explicitly configure `USER appuser` (UID 10001). Never deploy containers running with root UID 0.
- **Strict `.dockerignore`**: Exclude `.git`, `.env*`, `node_modules`, `tests`, and credentials from Docker build context.

### 2. IAM Least Privilege
- Every service must run under its own dedicated Service Account.
- Never grant broad roles like `roles/owner` or `roles/editor`. Grant only targeted roles (e.g. `roles/secretmanager.secretAccessor`, `roles/cloudsql.client`).

### 3. Structured Observability (Three Pillars)
- **Logs**: Emit structured single-line JSON logs with severity (`DEFAULT`, `INFO`, `WARNING`, `ERROR`), trace context (`logging.googleapis.com/trace`), and timestamp.
- **Metrics**: Expose Prometheus `/metrics` or OpenTelemetry runtime counters.
- **Health Checks**: Implement discrete `/healthz` (liveness) and `/readyz` (readiness) HTTP endpoints.

---

## 3. Automation Tool: Container Security Verifier

Audit Dockerfiles for non-root execution and security guardrails:
```bash
python3 scripts/verify_container_security.py --path Dockerfile
```
