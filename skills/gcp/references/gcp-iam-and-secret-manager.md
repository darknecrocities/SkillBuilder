# GCP IAM Least Privilege, Workload Identity & Secret Manager

> **Objective**: Eliminate static JSON service account keys and broad `roles/editor` / `roles/owner` bindings across Google Cloud deployments.

---

## 1. Dedicated Service Accounts & Minimal Roles

Never run Cloud Run, Cloud Functions, or GKE workloads under the default Compute Engine service account (`*-compute@developer.gserviceaccount.com`, which carries excessive `Editor` permissions):

| Workload Need | Prohibited Broad Role | Least-Privilege Role |
| :--- | :--- | :--- |
| **Read one app secret** | `roles/secretmanager.admin` at project scope | `roles/secretmanager.secretAccessor` bound on **the specific secret resource** |
| **Publish domain events** | `roles/pubsub.admin` | `roles/pubsub.publisher` bound on **the specific topic** |
| **Read/Write GCS assets** | `roles/storage.admin` | `roles/storage.objectUser` bound on **the specific bucket** |
| **Connect to Cloud SQL** | Public IP `0.0.0.0/0` + superuser | `roles/cloudsql.client` + IAM DB auth over Private VPC / Unix socket |

---

## 2. Secret Manager & Workload Identity Federation

1. **Zero Static Keys**: Authenticate GitHub Actions / CI via **Workload Identity Federation (OIDC)** (`google-github-actions/auth@v2` with `workload_identity_provider`), never exported JSON keys.
2. **Runtime Secret Mounting**: Bind secrets in Cloud Run (`--set-secrets="DB_PASS=db-pass:latest"` or mounted volume `/secrets/...`) — never bake credentials into `Dockerfile` or `cloudbuild.yaml` plaintext env vars.
3. **GCS Bucket & Cloud SQL Protection**: Enable uniform bucket-level access, block public access (`public_access_prevention = "enforced"`), and set `deletion_protection = true` on Cloud SQL.
