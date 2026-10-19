---
name: ai-and-llm-engineering
description: Architect, implement, and maintain production AI systems, Gemini API agents, Antigravity multi-agent orchestration, structured JSON outputs, reliable tool calling, and RAG retrieval pipelines.
---

# AI & LLM Systems Engineering

> **Role**: Principal AI Systems Engineer & Agent Architect  
> **Philosophy**: *Deterministic boundaries on probabilistic models. Enforce strict JSON schemas. Verify citations. Guard token budgets.*

This skill establishes production discipline for Generative AI, Large Language Models, and autonomous agent loops. It enforces the official `google-genai` SDK patterns, Antigravity subagent orchestration, strict schema-constrained outputs, defensive tool execution, and token budget optimization.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/gemini-sdk-and-models.md](references/gemini-sdk-and-models.md) | Official `google-genai` SDK patterns, model selection matrix. |
| **Reference** | [references/structured-outputs-and-tools.md](references/structured-outputs-and-tools.md) | Guaranteed JSON schemas, Pydantic type models, robust tool calling. |
| **Reference** | [references/rag-and-vector-search.md](references/rag-and-vector-search.md) | Chunking strategies, semantic embeddings, hybrid reranking, citation checks. |
| **Reference** | [references/token-optimization-and-caching.md](references/token-optimization-and-caching.md) | Context window management, prompt caching, token reduction heuristics. |
| **Reference** | [references/ai-error-catalog.md](references/ai-error-catalog.md) | Catalog of AI errors: schema failures, hallucinated tool calls, context overflows. |
| **Template** | [templates/gemini_structured_agent.py](templates/gemini_structured_agent.py) | Production Gemini agent implementation with typed JSON schemas. |
| **Template** | [templates/gemini_rag_pipeline.py](templates/gemini_rag_pipeline.py) | Complete vector retrieval and citation-backed synthesis pipeline. |
| **Utility** | [scripts/calculate_token_budget.py](scripts/calculate_token_budget.py) | CLI utility to estimate token consumption and optimize prompt payloads. |

---

## 2. Core AI Systems Invariants

### 1. Mandatory Schema-Enforced Structured Outputs
- When programmatic systems consume LLM responses, never parse unstructured markdown.
- Enforce `response_mime_type="application/json"` with `response_schema` (Pydantic model or JSON Schema).
- Parse and validate the response against the schema immediately upon receipt.

### 2. Defensive Tool & Function Calling
- Model tool declarations must define explicit property descriptions and required fields.
- Wrap all tool execution handlers in `try/except` blocks. If a tool fails, return a structured error message to the model rather than crashing the agent loop.
- Tools mutating real-world systems must enforce idempotency and permission checks.

### 3. Grounded Retrieval-Augmented Generation (RAG)
- Every generated factual assertion must cite its source chunk ID (`[Doc: Chunk 12]`).
- Do not inject raw unchunked documents into context. Use semantic or recursive character chunking (500–1000 tokens with 10% overlap).
- Combine dense vector retrieval with keyword/BM25 search (Hybrid Search).

### 4. Context Budget & Prompt Caching
- Reuse static system instructions and documentation across multi-turn sessions to leverage context caching.
- Enforce strict token budget ceilings per agent invocation.

---

## 3. Automation Tool: Token Budget Calculator

Estimate token footprint and optimize prompt payloads:
```bash
python3 scripts/calculate_token_budget.py --text "User system prompt payload"
```
