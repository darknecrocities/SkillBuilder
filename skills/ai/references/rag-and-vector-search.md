# Grounded RAG, Hybrid Search & Prompt Injection Defense

> **Objective**: Eliminate retrieval hallucinations, missed keyword matches, and indirect prompt injection inside RAG pipelines.

---

## 1. Hybrid Retrieval Pipeline (Dense + BM25 + RRF)

Pure cosine vector search misses exact identifiers (`ERR_CONNECTION_REFUSED`, `NCT04280705`, `tenant_id`). Combine lexical BM25 with dense semantic embeddings using **Reciprocal Rank Fusion (RRF)**:

$$\text{RRF}(d) = \sum_{r \in \{\text{BM25}, \text{Dense}\}} \frac{1}{60 + \text{rank}_r(d)}$$

### Chunking Invariants
- **Window Size**: `500–900` tokens per chunk with `10–15%` semantic overlap.
- **Boundary Respect**: Split on Markdown headings (`##`), code AST blocks, or paragraph breaks — never slice mid-sentence or mid-table.
- **Rich Metadata**: Store `{ doc_id, source_url, section_title, updated_at, tenant_id }` on every chunk and **filter by `tenant_id` inside the vector query** (prevents cross-tenant data leakage!).

---

## 2. Citation Grounding & Hallucination Guard

Inject chunks wrapped in clear non-executable delimiters and require chunk-ID citations:

```xml
<retrieved_context>
  <chunk id="spec-4.2" source="docs/timeouts.md">
    Ingress connection handshake timeout is 3 seconds; read timeout is 15 seconds.
  </chunk>
</retrieved_context>
```

- **Automated Verification**: Verify every `[chunk_id]` cited in the model response actually exists in the retrieved set, and drop or flag unsupported numeric claims.
- **Fallback Behavior**: If top reranker score `< threshold` (e.g. `< 0.35`), return `INSUFFICIENT_CONTEXT` instead of forcing the LLM to hallucinate.

---

## 3. Indirect Prompt Injection Defense
- Never parse untrusted web/PDF text into system instructions.
- Strip executable HTML/script payloads during ingestion; convert PDFs/HTML to plain Markdown first.
- Require explicit confirmation or narrow read-only scopes before any tool call triggered while summarizing external retrieved documents.
