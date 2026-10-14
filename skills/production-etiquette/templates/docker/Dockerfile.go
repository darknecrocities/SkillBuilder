# ==============================================================================
# Multi-Stage Production Dockerfile for Go Applications
# Security: Compiles statically into minimal scratch/alpine with non-root user
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build & Compile Binary
# ------------------------------------------------------------------------------
FROM golang:1.23-alpine AS builder

WORKDIR /app

# Install git and ca-certificates
RUN apk add --no-cache git ca-certificates

# Copy go module manifests
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Compile static binary without CGO
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /app/server ./cmd/server

# ------------------------------------------------------------------------------
# Stage 2: Distroless Minimal Runtime
# ------------------------------------------------------------------------------
FROM alpine:3.20 AS runner

WORKDIR /app

RUN apk add --no-cache ca-certificates curl

# Create unprivileged user (UID 10001)
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

# Copy compiled binary from builder
COPY --from=builder --chown=appuser:appgroup /app/server /app/server

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["/app/server"]
