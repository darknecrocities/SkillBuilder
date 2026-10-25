# Token Optimization & Context Caching

Controlling LLM latency, cost, and context bloat.

---

## 1. Gemini Context Caching
When operating on large codebases or large system prompt instructions:
- If prompt prefix exceeds 32,768 tokens (e.g. codebase index or API documentation), establish a **CachedContent** resource.
- Subsequent calls referencing `cached_content` reduce per-call token pricing by up to 75% and significantly lower time-to-first-token latency.

---

## 2. In-Prompt Token Reduction Heuristics
1. **Omit Empty Keys**: Never serialize `null`, `undefined`, or empty list fields in JSON payloads passed to the model.
2. **Compact Schemas**: Shorten key names in high-frequency arrays (`ts` instead of `timestamp_in_milliseconds`).
3. **Progressive Inclusion**: Fetch file definitions on-demand via tools rather than pasting the entire project tree into system instructions.
