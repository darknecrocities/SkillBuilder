# DuckDB In-Process Analytics & Dead-Letter Queue (DLQ) Patterns

> **Objective**: Run fast sub-second analytical aggregations over Parquet/Arrow locally via DuckDB while isolating malformed records safely in replayable DLQs.

---

## 1. DuckDB In-Process Analytical Pattern

DuckDB queries Parquet, CSV, JSON, and Arrow tables directly in-process without maintaining a separate warehouse server:

```python
import duckdb

def aggregate_hourly_events(parquet_glob: str, output_parquet: str) -> int:
    con = duckdb.connect(database=":memory:")
    try:
        con.execute("SET memory_limit = '1GB'; SET threads = 4;")
        con.execute(
            """
            COPY (
              SELECT
                date_trunc('hour', event_ts) AS hour_bucket,
                tenant_id,
                COUNT(*) AS event_count,
                approx_quantile(latency_ms, 0.95) AS p95_latency_ms
              FROM read_parquet(?)
              WHERE event_ts IS NOT NULL
              GROUP BY 1, 2
            ) TO ? (FORMAT PARQUET, COMPRESSION ZSTD);
            """,
            [parquet_glob, output_parquet],
        )
        return con.execute("SELECT COUNT(*) FROM read_parquet(?)", [output_parquet]).fetchone()[0]
    finally:
        con.close()
```

---

## 2. Dead-Letter Queue (DLQ) & Replay Contract

1. **Never Drop Silent Failures**: When a batch fails schema validation or enrichment, serialize `{ dlq_id, ingested_at, source_topic, error_code, error_detail, raw_payload }` to a durable `.jsonl` / SQLite DLQ table / Pub/Sub DLQ topic.
2. **Bounded Poison-Pill Retries**: Track `attempt_count`; after `max_attempts = 3`, move to terminal DLQ storage and emit a structured alert metric rather than spinning infinitely.
3. **Idempotent Replay CLI**: Provide a deterministic replay command that re-validates DLQ records against fixed schemas using the original `idempotency_key` so replayed records never double-count.
