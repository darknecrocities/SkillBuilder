---
name: local-llm
description: Local LLM architecture, quantized inference (GGUF Q4_K_M/Q8_0), Ollama, llama.cpp, Apple Silicon MLX, WebLLM, GBNF structured grammars, in-process local RAG, and 3-tier hybrid edge-cloud routing.
---

# Local LLM Architecture, Quantized Inference & Edge AI

The `local-llm` skill governs private, resilient, and cost-efficient on-device and edge artificial intelligence. It standardizes quantized inference runtimes (`llama.cpp`, `Ollama`, Apple Silicon `MLX`, browser-based `WebLLM`), mathematical VRAM sizing, GBNF deterministic grammar constraints, embedded vector databases, and resilient 3-tier hybrid edge-cloud routing.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/quantized-inference-and-gguf.md](references/quantized-inference-and-gguf.md) | Quantization trade-offs, GGUF Q4_K_M vs Q8_0 benchmarks, runtime engines. |
| **Reference** | [references/gbnf-grammars-and-local-rag.md](references/gbnf-grammars-and-local-rag.md) | GBNF grammar constraints for guaranteed JSON, in-process local vector retrieval. |
| **Utility** | [scripts/verify_local_llm_hygiene.py](scripts/verify_local_llm_hygiene.py) | Scans code for unquantized model imports, missing GBNF validation, and unbuffered context allocations. |

---

## 2. Heterogeneous Inference Runtime Matrix

| Runtime Engine | Target Architecture | Formats | Optimal Deployment | Key Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **`llama.cpp` (`llama-server`)** | C/C++ native | GGUF (`Q4_K_M`, `Q8_0`) | Linux / Docker / CUDA | Continuous batching (`-cb`), prompt caching, `-ngl 999` GPU offloading. |
| **`Ollama`** | Go daemon | GGUF | Workstations / Dev Teams | Declarative `Modelfile`, OpenAI-compatible REST API (`:11434/v1`). |
| **Apple Silicon `MLX` (`mlx-lm`)** | Apple Metal | MLX 4-bit / 8-bit | macOS M-series Fleets | Unified Memory Architecture (UMA) eliminating PCIe bus lag; 80–120+ tok/s. |
| **`WebLLM`** | Wasm + WebGPU | Quantized GGUF | Client Web Browsers | 100% private, client-side zero-server-cost execution. |

### Apple Silicon MLX High-Throughput Service
```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")
response = generate(
    model,
    tokenizer,
    prompt="<|begin_of_text|><|start_header_id|>user<|end_header_id|>\nExtract entities...<|eot_id|>",
    max_tokens=512,
    verbose=False
)
```

---

## 2. Quantization Science & VRAM Sizing

Never guess hardware requirements. Compute exact memory footprint before provisioning:

$$\text{VRAM}_{\text{req}} = \left(\frac{\text{Parameters (B)} \times \text{Bits per weight}}{8}\right) + \text{KV Cache} + \text{Context Window Overhead}$$

### Recommended Quantization Profiles
- **`Q4_K_M` (Production Default)**: ~4.5 bits/weight. Retains 98.5% of FP16 perplexity while cutting memory overhead by 72%.
- **`Q5_K_M` (High-Precision Logic)**: ~5.5 bits/weight. Ideal for complex code generation and strict mathematical deduction.
- **`Q8_0` (Near-Lossless Baseline)**: ~8.5 bits/weight. Mandatory for embedding vectors and critical semantic classification.

### Production Example (8B Parameter Model at Q4_K_M, 8,192 Context):
$$\text{Weight Memory} = \frac{8.0 \times 4.5}{8} = 4.5\,\text{GB}$$
$$\text{KV Cache} = 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times \text{seq\_len} \times 2\,\text{bytes} \approx 1.25\,\text{GB}$$
$$\text{Total VRAM} \approx 4.5 + 1.25 + 0.35\,(\text{CUDA overhead}) \approx 6.1\,\text{GB}$$

---

## 3. Deterministic Structured Output via GBNF Grammars

Unconstrained local models hallucinate formatting errors under high load. Restrict token logit sampling at the C++ runtime level using GGML BNF (GBNF) Grammars so invalid tokens are mathematically impossible to emit:

```ebnf
# root.gbnf - Strict JSON Object Schema
root ::= "{" ws "\"id\":" ws string "," ws "\"confidence\":" ws number "," ws "\"action\":" ws action_enum "}"
action_enum ::= "\"approve\"" | "\"escalate\"" | "\"reject\""
string ::= "\"" [^"\\]* "\""
number ::= [0-9]+ ("." [0-9]+)?
ws ::= [ \t\n\r]*
```

### Passing Grammar to `llama-server`
```bash
curl http://localhost:8080/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Evaluate transaction...",
    "grammar": "root ::= \"{\" ws \"\\\"status\\\":\" ws (\"\\\"ok\\\"\" | \"\\\"failed\\\"\") \"}\" ws ::= [ \\t\\n]*",
    "temperature": 0.1
  }'
```

---

## 4. In-Process Local RAG & Vector Storage

Prohibit heavyweight external vector database containers for local agent workflows. Use zero-dependency in-process vector engines:
- **`sqlite-vec`**: C-based SQLite extension for vector search within standard relational tables.
- **`DuckDB` (`vss` extension)**: Fast OLAP vector indexing directly in local disk storage.

```sql
-- In-Process DuckDB Vector Search
INSTALL vss;
LOAD vss;

CREATE TABLE document_embeddings (
    doc_id VARCHAR PRIMARY KEY,
    content TEXT,
    embedding FLOAT[384]
);

SELECT doc_id, content, array_cosine_distance(embedding, [0.12, -0.45, ...]) AS distance
FROM document_embeddings
ORDER BY distance ASC
LIMIT 5;
```

---

## 5. 3-Tier Hybrid Edge-Cloud Routing Gateway

Implement intelligent tiered cascades to balance data privacy, latency, and reasoning depth:

1. **Tier 1 (Local Edge Classifier - < 150ms)**:
   - Lightweight on-device models (Llama-3.2-3B, Qwen-2.5-3B at `Q4_K_M`).
   - Private PII scrub, intent classification, local command routing.
2. **Tier 2 (Local Workhorse Engine - 150ms–800ms)**:
   - Medium offline models (Llama-3.3-70B, Qwen-2.5-32B, DeepSeek-R1-Distill) running via Apple Silicon MLX or dedicated GPU `llama-server`.
   - Complex code generation, schema-constrained extraction, and offline report synthesis.
3. **Tier 3 (Cloud Frontier Fallback)**:
   - Gemini 2.5 Flash / Pro via `google-genai` SDK.
   - Triggered when: local confidence score $< 0.75$, multimodal visual input required, web grounding needed, or Tier 1/2 encounters an OOM/timeout.

```python
# Fallback Routing Pattern
async def route_llm_request(prompt: str, context: dict) -> str:
    try:
        # Tier 1 & 2 Local Attempt with 3s connection / 15s body timeout
        return await call_local_runtime(prompt, timeout=(3.0, 15.0), grammar=STRICT_JSON_GBNF)
    except (LocalOOMException, TimeoutError, LowConfidenceError):
        # Tier 3 Resilient Frontier Fallback
        return await call_gemini_frontier(prompt, context)
```
