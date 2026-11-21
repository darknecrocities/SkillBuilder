# OpenTelemetry Semantic Conventions & Trace Propagation

> **Objective**: Correlate every request across frontend, API gateway, queues, and database queries using standard W3C TraceContext headers and clean span budgets.

---

## 1. W3C TraceContext & Span Naming

- Propagate `traceparent` and `tracestate` headers across HTTP, Pub/Sub/SQS messages, and background workers so distributed waterfalls stay connected end-to-end.
- **Low-Cardinality Span Names**: Name spans using route templates (`GET /v1/projects/:id`), **never** raw dynamic URLs (`GET /v1/projects/99182-abc`), which explode metric cardinality!

---

## 2. Mandatory Semantic Attributes

| Layer | Standard OpenTelemetry Attributes | Avoid Putting in Attributes |
| :--- | :--- | :--- |
| **HTTP Server** | `http.request.method`, `http.route`, `http.response.status_code`, `url.scheme` | Raw query strings with tokens, `Authorization` headers, cookies |
| **Database** | `db.system` (`postgresql` / `sqlite`), `db.operation.name` (`SELECT`), `db.collection.name` | Unredacted user PII values or passwords inside raw SQL text |
| **AI / LLM Calls** | `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` | Full private user prompts unless explicit opt-in debug mode |

---

## 3. Error Recording & Graceful Flush
- On exceptions inside a span, call `span.recordException(err)` and `span.setStatus({ code: SpanStatusCode.ERROR, message: err.code })`.
- Register `await sdk.shutdown()` inside `SIGTERM`/`SIGINT` handlers so buffered spans export cleanly before process exit.
