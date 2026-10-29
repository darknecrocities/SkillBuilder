# GCP IAM Least Privilege & Secret Manager Integration

---

## 1. Secret Manager Mounting

Never inject plaintext secrets in environment variables or container image layers. Bind secrets directly via Cloud Run volume mounts or environment secret references:

```bash
gcloud run deploy my-service \
    --image gcr.io/my-project/my-service:v1 \
    --set-secrets="DATABASE_URL=projects/123456/secrets/prod-db-url:latest"
```

---

## 2. Service Account Scoping

- Create dedicated service accounts per microservice (e.g., `orders-svc@project-id.iam.gserviceaccount.com`).
- Grant least-privilege roles (`roles/secretmanager.secretAccessor`, `roles/cloudsql.client`).
- Prohibit wide administrative roles (`roles/owner`, `roles/editor`) on runtime accounts.
