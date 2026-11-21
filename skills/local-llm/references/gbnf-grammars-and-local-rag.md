# GBNF Grammars & In-Process Local RAG (`sqlite-vec` / DuckDB)

> **Objective**: Guarantee syntactically valid structured outputs from quantized local models and fast sub-10ms local vector retrieval with zero external database containers.

---

## 1. Constraining Token Logits via GBNF Grammars

Small local models (`3B–8B`) frequently wrap JSON in markdown fences or drop trailing commas when prompted loosely. GBNF grammars mask invalid token logits at every decoding step in `llama.cpp` so malformed output cannot be sampled:

```ebnf
root        ::= "{" ws "\"action\":" ws action "," ws "\"confidence\":" ws num "," ws "\"reason\":" ws string ws "}"
action      ::= "\"allow\"" | "\"deny\"" | "\"review\""
num         ::= ("0" ("." [0-9]{1,2})?) | "1.0"
string      ::= "\"" [^"\\\n\r]{1,160} "\""
ws          ::= [ \t\n]*
```

- **Keep Enumerations Tight**: Avoid unbounded `.*` loops inside GBNF rules; bound string lengths and forbid unescaped newlines where single-line fields are expected.
- **Ollama Equivalent**: Pass `format: zodToJsonSchema(MySchema)` on Ollama `/api/chat` structured output requests (backed internally by GBNF).

---

## 2. In-Process Vector Retrieval (`sqlite-vec` vs. DuckDB `vss`)

| Engine | Best Fit | Persistence | Key Advantage |
| :--- | :--- | :--- | :--- |
| **`sqlite-vec`** | Desktop apps, Electron, FastAPI local services | Single `.db` file (WAL mode) | Relational joins + vector KNN + FTS5 BM25 in one ACID file |
| **`DuckDB` (`vss`)** | Analytics, batch embedding sweeps, local notebooks | `.duckdb` file | Columnar SIMD cosine distance + Parquet ingestion |

### Hybrid Local Query Hygiene
- Store normalized `chunk_id`, `doc_hash` (skip re-embedding unchanged files!), and `embedding_model` version so model swaps trigger clean re-indexing rather than mixing incompatible vector spaces.
- Never load full 50 MB raw documents into prompt context; retrieve top-`K` (`K = 4–6`) reranked chunks within a fixed token cap (`<= 2,500` tokens).
