# Retrieval-Augmented Generation (RAG) & Hybrid Search

Architecture for grounding LLM synthesis in private documentation.

---

## 1. Document Chunking Strategy
- **Chunk Size**: 500–1,000 characters (or ~150–250 tokens).
- **Chunk Overlap**: 10–15% overlap to preserve context across boundaries.
- **Metadata**: Attach file path, section header, and updated timestamp to every chunk.

---

## 2. Hybrid Search (Dense Vector + BM25)
1. **Vector Retrieval**: Query `text-embedding-004` to retrieve semantic matches.
2. **Lexical Retrieval**: Run BM25 / keyword search for exact entity names, error codes, and function names.
3. **Reciprocal Rank Fusion (RRF)**:
$$RRF(d) = \sum_{m \in M} \frac{1}{60 + r_m(d)}$$
4. **Context Injection**: Pass top-5 ranked chunks to Gemini with strict instruction: "Answer only based on the provided source chunks."
