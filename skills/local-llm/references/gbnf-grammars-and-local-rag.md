# GBNF Grammars & In-Process Local RAG

---

## 1. GBNF Grammars for Guaranteed JSON

GBNF (GGML BNF) restricts logits during decoding to guarantee strict conformance to a schema:

```gbnf
root   ::= "{" ws "\"status\":" ws status "," ws "\"confidence\":" ws number "}"
status ::= "\"pass\"" | "\"fail\"" | "\"warn\""
number ::= [0-9] "." [0-9] [0-9]
ws     ::= [ \t\n]*
```

---

## 2. In-Process Local RAG with DuckDB / SQLite-vss

1. Embed text chunks using local small embedding models (e.g. `nomic-embed-text` or `all-MiniLM-L6-v2`).
2. Store vector float arrays in SQLite or DuckDB with cosine distance indexing.
3. Retrieve top-$K$ candidates locally and pass to quantized LLM prompt without outbound network calls.
