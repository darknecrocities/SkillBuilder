# Cloud Architecture & Google Cloud Platform (GCP)

Production deployment patterns for scalable and secure cloud infrastructure.

---

## 1. Serverless Compute: Google Cloud Run
- **Container-First**: Package any workload exposing an HTTP port into a lightweight container.
- **Autoscaling**: Configure `min_instances = 1` for latency-critical production workloads to eliminate cold starts; configure `max_instances` to protect downstream databases from connection saturation.
- **Direct VPC Egress**: Connect Cloud Run to Cloud SQL or Memorystore via Serverless VPC Access Connector without exposing databases to the public internet.

---

## 2. Secrets Management with Secret Manager
- Never pass database passwords or API keys in container environment variables directly.
- Mount secrets from Google Secret Manager as volume mounts (`/secrets/...`) or resolve them using GCP Secret Manager SDK at service boot.
- Bind the Service Account using `roles/secretmanager.secretAccessor`.
