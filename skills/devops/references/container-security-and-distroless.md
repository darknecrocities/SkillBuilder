# Container Security & Distroless Builds

Hardening container images for production deployment.

---

## 1. Multi-Stage Distroless Docker Pattern

```dockerfile
# Stage 1: Build & Compile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Minimal Distroless Runtime
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

# Non-root user provided by distroless
USER 10001:10001
ENV NODE_ENV=production
EXPOSE 8080
CMD ["dist/main.js"]
```

---

## 2. Container Hardening Checklist
- [ ] No package managers (`apk`, `apt`) or shells (`/bin/sh`) in the production runtime stage.
- [ ] Explicit non-root user directive (`USER 10001:10001`).
- [ ] Root filesystem set to read-only where possible (`--read-only`).
- [ ] No secret tokens embedded in `ENV` or build arguments.
