# Production Serving Engines (`vLLM` / `SGLang`), WebGPU & KV-Cache Tuning

> **Objective**: Scale local LLM serving from single-user laptops to multi-tenant GPU microservices while bounding KV-cache VRAM and startup latency.

---

## 1. Serving Engine Matrix Beyond Single-User Daemons

| Engine | Best Fit | Throughput Mechanism | Key Production Flags |
| :--- | :--- | :--- | :--- |
| **`vLLM`** | Multi-user FastAPI / microservice GPUs | PagedAttention + continuous batching | `--enable-prefix-caching --quantization fp8 --max-model-len 8192` |
| **`SGLang`** | High-speed structured JSON / agent loops | RadixAttention prefix reuse + constrained FSM | `--kv-cache-dtype fp8_e5m2 --mem-fraction-static 0.85` |
| **`Transformers.js` v3** | In-browser WebGPU zero-backend apps | ONNX `q4f16` inside Web Worker | Pin WebGPU adapter fallback + dispose `pipeline()` on unmount |

---

## 2. KV-Cache Quantization, Prefix Caching & Speculative Decoding

1. **KV-Cache Compression**: Unquantized FP16 KV cache explodes on `>16k` context windows. Enable Flash Attention (`-fa` / `OLLAMA_FLASH_ATTENTION=1`) + `q8_0` KV cache (`OLLAMA_KV_CACHE_TYPE=q8_0` or `--cache-type-k q8_0 --cache-type-v q8_0`) to cut context VRAM by `~45%` with negligible quality loss.
2. **Prefix Caching**: Keep static system instructions and tool schemas at the exact start of the prompt prefix so `llama.cpp` slot caching / `vLLM --enable-prefix-caching` / `SGLang` RadixAttention skip redundant prefill computation.
3. **Speculative Decoding**: Pair a `32B–70B` target model with a `0.5B–3B` draft model of the same tokenizer family (`--model-draft`) for `1.8x–2.6x` decode speedup on memory-bandwidth-bound GPUs.
4. **OpenAI-Compat `/v1` Contract**: Always connect clients via `/v1/chat/completions` (`AI_BASE_URL`) rather than bespoke SDK endpoints so `Ollama`, `llama-server`, `vLLM`, and `MLX` remain drop-in interchangeable (`/ai-integration`).
