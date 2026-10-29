# DuckDB In-Process Analytics & Dead-Letter Queue (DLQ) Patterns

---

## 1. DuckDB In-Process Analytics

DuckDB operates directly on Parquet and Arrow buffers with vectorized SQL execution:

```python
import duckdb

con = duckdb.connect(database=":memory:")
con.execute("""
    SELECT
        account_id,
        count(*) as transaction_count,
        sum(amount) as total_volume
    FROM read_parquet('data/*.parquet')
    GROUP BY account_id
    HAVING total_volume > 10000
""")
results = con.fetchall()
```

---

## 2. Dead-Letter Queue (DLQ) Architecture

Any transformation or schema validation failure must route records to a Dead-Letter Queue (DLQ) rather than dropping data or terminating the pipeline:

```json
{
  "raw_record": {"id": "rec_123", "amount": "invalid_number"},
  "error": "ValueError: Could not parse float from 'invalid_number'",
  "pipeline_stage": "transform_currency",
  "timestamp": "2026-10-29T19:35:00Z"
}
```
