# Cloud, Container & DevOps Error Catalog

Diagnoses and resolutions for cloud deployment, container orchestration, and CI/CD defects.

---

### [CL-ERR-001] CrashLoopBackOff: Container Exits Immediately
- **Symptom**: Pod status displays `CrashLoopBackOff`; container restarts continuously.
- **Root Cause**: Missing required environment variable, binary architecture mismatch (e.g. built on arm64 Mac without `--platform linux/amd64`), or process bound to `localhost` instead of `0.0.0.0`.
- **Diagnostic Command**: `kubectl logs <pod-name> --previous` or `docker logs <container-id>`.
- **Remediation**:
  1. Ensure server listens on `0.0.0.0:$PORT` rather than `127.0.0.1`.
  2. Verify all boot-time required environment variables are supplied.
  3. Build with Docker Buildx: `docker buildx build --platform linux/amd64 ...`

---

### [CL-ERR-002] GCP Cloud Run IAM Permission Denied (403)
- **Symptom**: `The request was not authenticated` or `User not authorized to invoke service`.
- **Root Cause**: Cloud Run service deployed with ingress restricted or missing `roles/run.invoker` role on caller service account.
- **Remediation**:
  - For public APIs: `gcloud run services add-iam-policy-binding <service> --member="allUsers" --role="roles/run.invoker"`
  - For private services: Grant `roles/run.invoker` to the caller's specific Service Account.

---

### [CL-ERR-003] Docker Build Secret Leakage
- **Symptom**: Security scanner detects `NPM_TOKEN` or `GITHUB_TOKEN` embedded in Docker image layers.
- **Root Cause**: Passing secret as standard `ARG` or copying `.env` during image build.
- **Remediation**: Use Docker BuildKit secret mounts:
  ```dockerfile
  RUN --mount=type=secret,id=npm_token \
      NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
  ```
