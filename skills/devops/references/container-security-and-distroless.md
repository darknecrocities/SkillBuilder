# Hardened Multi-Stage Containers & Distroless Security Manual

> **Objective**: Build minimal, reproducible, non-root production containers with small attack surfaces and fast cold starts.

---

## 1. Multi-Stage Non-Root Dockerfile Blueprint

```dockerfile
# Stage 1: Dependencies & Build
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY . .
RUN npm run build && npm prune --omit=dev

# Stage 2: Minimal Non-Root Runtime
FROM node:22-alpine AS runner
RUN addgroup -g 10001 -S appgroup && adduser -u 10001 -S appuser -G appgroup
WORKDIR /app
ENV NODE_ENV=production PORT=8080

COPY --from=builder --chown=10001:10001 /app/package.json ./
COPY --from=builder --chown=10001:10001 /app/node_modules ./node_modules
COPY --from=builder --chown=10001:10001 /app/dist ./dist

USER 10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1
CMD ["node", "dist/server.js"]
```

---

## 2. Container Security Checklist
- [ ] **Non-Root Mandatory**: `USER 10001` (or distroless `nonroot` `65532`) — never run container processes as UID `0`.
- [ ] **`.dockerignore` Complete**: Exclude `.git`, `.env`, `.env.*`, `node_modules`, `coverage`, `.backups`, `scratch`.
- [ ] **No Secrets in `ENV`/`ARG`**: Inject secrets at runtime via Secret Manager / mounted tmpfs secrets (`ARG` values stay baked into image layer history!).
- [ ] **Read-Only Root Filesystem**: Mount `/tmp` as writable emptyDir/tmpfs and run container with `read_only: true` + `cap_drop: [ALL]` in `docker-compose.yml` / K8s.
