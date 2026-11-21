# Cloud Architecture, Serverless Scaling & Terraform IaC

> **Objective**: Provision stateless, autoscaling cloud workloads backed by Infrastructure-as-Code with zero hardcoded secrets and strict stateful deletion protection.

---

## 1. Stateless Container & Compute Design

- **Zero Local Container State**: Containers on Cloud Run, ECS Fargate, or Kubernetes can recycle at any instant. Store files in S3/GCS, sessions/locks in Redis, and relational state in Cloud SQL/RDS/Supabase.
- **Graceful `SIGTERM` Drain**: Handle `SIGTERM`, reject new readiness probes, wait for active in-flight HTTP requests to complete (`<= 10–15s`), drain DB pools, and exit `0`.
- **Resource & Concurrency Limits**: Explicitly set CPU/memory limits, `min_instances` (for latency-sensitive endpoints), `max_instances` (cost & DB pool protection), and request timeouts.

---

## 2. Terraform IaC & Stateful Deletion Protection

1. **Remote Locked State**: Store Terraform state in encrypted GCS/S3 buckets with state locking and versioning enabled — never commit `terraform.tfstate` to Git.
2. **Deletion Protection**: Always enforce `deletion_protection = true` on Cloud SQL/RDS instances and `lifecycle { prevent_destroy = true }` on stateful buckets and KMS keys.
3. **Environment Parity**: Parameterize `dev`, `staging`, and `prod` via `.tfvars` workspaces without duplicating resource modules.
4. **Pre-Destroy Gate**: Any destructive `terraform destroy` or resource purge requires explicit user confirmation and verified backup digest (`/database` Sensitive Deletion Gate).
