# OpenTelemetry Semantic Conventions & Distributed Tracing

---

## 1. Trace Context Propagation

Always extract and inject W3C TraceContext headers (`traceparent`, `tracestate`) across HTTP, gRPC, and message queues:

```http
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

- Version: `00`
- Trace ID: 16-byte hex string (shared across all spans in the distributed transaction)
- Parent Span ID: 8-byte hex string
- Trace Flags: `01` (recorded / sampled)

---

## 2. Span Semantic Attributes

Span Category | Required Attributes
:--- | :--- | :---
HTTP Server | `http.request.method`, `url.path`, `http.response.status_code`, `client.address`
Database | `db.system` (`postgresql`, `sqlite`), `db.operation`, `db.collection.name`
RPC | `rpc.system` (`grpc`), `rpc.service`, `rpc.method`
