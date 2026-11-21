# Streaming ETL, Backpressure & Apache Arrow Memory Architecture

> **Objective**: Build bounded-memory ETL pipelines that survive multi-gigabyte bursts without OOM kills or corrupted partial loads.

---

## 1. Backpressure & Bounded Queue Rules

Never load unbounded files (`fs.readFileSync`, `df = pd.read_json("huge.json")`) or create unbounded `asyncio.Queue()` / `Promise.all(100000Items)` bursts:
1. **Bounded Channels**: Cap in-flight queues (`asyncio.Queue(maxsize=256)` or Node `highWaterMark`) so slow downstream sinks automatically throttle upstream readers.
2. **Streaming Chunk Iterators**: Process NDJSON, CSV, and Parquet in fixed batches (`batch_size = 1000–5000` rows) via async generators (`yield batch`).
3. **Explicit Timeouts & Circuit Breakers**: Bound upstream extractor reads (`3s` connect / `15s` read) and checkpoint batch offsets atomically.

---

## 2. Apache Arrow Zero-Copy & Schema Validation

- **Columnar Efficiency**: Represent analytical batches as **Apache Arrow** `RecordBatch` / `Table` structures rather than Python `list[dict]`, cutting memory overhead by `5–10x` and enabling zero-copy exchange between DuckDB, Polars, and Parquet writers.
- **Boundary Schema Enforcement**: Validate every incoming record against strict Pydantic v2 / Arrow schema contracts **before** writing to the analytical sink:
  - Valid records proceed to typed Parquet / SQL sink.
  - Malformed records route immediately to the **Dead-Letter Queue (DLQ)** with original raw payload + structured validation reason + timestamp + `correlation_id`.
- **Idempotent Partition Writes**: Write output partitions atomically (write to `.tmp` staging file -> verify row count/checksum -> atomic `os.replace()` into target partition) so crashed runs never leave half-written Parquet files.
