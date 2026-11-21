# CI/CD Pipelines, Security Gates & Artifact Provenance

> **Objective**: Catch regressions, secret leaks, bloated files, and container CVEs automatically in GitHub Actions / Cloud Build before code merges to `main`.

---

## 1. The 5-Gate CI Pipeline Architecture

1. **Gate 1 — Hygiene & Static Quality**:
   - Line limits (`check_source_line_limits.py --path .`), anti-slop (`sanitize_ai_slop.py --strict`), skill depth/sync (`skill_linter.py --all --strict-depth`), `eslint` / `ruff`.
2. **Gate 2 — Type Safety & Contracts**:
   - `tsc --noEmit`, `mypy` / `pyright`, OpenAPI schema validation, and public-data boundary checks (`bettersanfernando` pattern).
3. **Gate 3 — Automated Test Suites**:
   - Unit, integration, and Playwright E2E suites with real ephemeral databases (SQLite/Postgres test containers).
4. **Gate 4 — Security & Container Scan**:
   - Dependency vulnerability audit (`npm audit` / `pip-audit`), Trivy container image scan (`CRITICAL`/`HIGH` fail build), and secret scanning (`gitleaks`).
5. **Gate 5 — Immutable Build & OIDC Deploy**:
   - Build once, tag with immutable Git SHA (`app:${GITHUB_SHA}`), authenticate to GCP/AWS via **OIDC Workload Identity Federation** (never static long-lived JSON/IAM keys in GitHub Secrets).

---

## 2. GitHub Actions Security Invariants
- Pin third-party actions by full commit SHA rather than mutable `@v4` tags where supply-chain policy applies.
- Grant minimal `permissions: { contents: read, id-token: write }` per job (`GITHUB_TOKEN` least privilege).
- Concurrency group `cancel-in-progress: true` on PRs; disable cancellation on `main` production deploys so releases never abort mid-migration.
