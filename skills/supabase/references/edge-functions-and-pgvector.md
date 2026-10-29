# Supabase Edge Functions & pgvector Search

---

## 1. Deno Edge Functions

- Written in TypeScript and executed on the Deno runtime worldwide.
- Validate request payloads with Zod before executing database mutations.
- Use `corsHeaders` on OPTIONS pre-flight calls.

---

## 2. pgvector Vector Similarity Search

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(768)
);

CREATE INDEX ON embeddings USING hnsw (embedding vector_cosine_ops);

-- Similarity Search RPC
CREATE OR REPLACE FUNCTION match_documents (
  query_embedding vector(768),
  match_threshold float,
  match_count int
)
RETURNS TABLE (id bigint, content text, similarity float)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    embeddings.id,
    embeddings.content,
    1 - (embeddings.embedding <=> query_embedding) AS similarity
  FROM embeddings
  WHERE 1 - (embeddings.embedding <=> query_embedding) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$;
```
