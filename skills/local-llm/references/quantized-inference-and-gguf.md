# Quantized Inference, GGUF Sizing, Ollama & MLX Tuning Manual

> **Objective**: Run private local LLMs at peak throughput without OOM crashes, quantization degradation, or silent Ollama connection hangs.

---

## 1. Quantization Selection Matrix

| Format | Bits / Weight | Perplexity Loss vs FP16 | Best Hardware | Ideal Workload |
| :--- | :--- | :--- | :--- | :--- |
| **`Q4_K_M`** | `~4.8` bpw | Minimal (`~1.5%`) | Consumer GPUs (`8–16 GB`), Apple UMA | General chat, routing, fast code drafting |
| **`Q5_K_M`** | `~5.7` bpw | Very low (`~0.7%`) | `12–24 GB` VRAM / M-Pro/Max | Complex structured JSON, TypeScript/Python generation |
| **`Q8_0`** | `~8.5` bpw | Near zero (`<0.2%`) | High-RAM Mac / Workstation | Embeddings, classification, sensitive tool calling |
| **`MLX 4-bit`** | `~4.5` bpw | Minimal | Apple Silicon M1–M4 UMA | Zero-PCIe-copy local macOS inference (`80–130 tok/s`) |

---

## 2. Accurate VRAM & KV-Cache Sizing

$$\text{VRAM}_{\text{total}} = \text{Weights} + \text{KV Cache} + \text{Compute Scratch (0.4–1.0 GB)}$$

- **8B `Q4_K_M` at `8,192` Context**: Weights `(8.0 * 4.5 / 8) = 4.5 GB` + KV Cache `~1.25 GB` + CUDA scratch `~0.35 GB` = **`~6.1 GB` VRAM**.
- **KV-Cache Trap**: Expanding `num_ctx` from `4,096` to `32,768` multiplies KV-cache memory by `8x` and can trigger silent CPU fallback (`10x` slowdown) in Ollama / `llama.cpp`. Always pin `num_ctx` deliberately (`8192` default) and enable **Flash Attention** (`-fa` / `OLLAMA_FLASH_ATTENTION=1`) + `q8_0` KV quantization when scaling context.

### Apple Silicon MLX High-Throughput Service
```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")
response = generate(model, tokenizer, prompt="Extract entities...", max_tokens=512, verbose=False)
```

---

## 3. Ollama Discovery & SSE Streaming Resilience (`domodomo` Pattern)

1. **Non-Blocking Health Probe**: Probe `GET http://127.0.0.1:11434/api/tags` with a strict `1.5s–3.0s` timeout before mounting local AI UI controls; surface explicit `"Ollama offline — start daemon or switch to WebLLM"` recovery state.
2. **NDJSON / SSE Cancellation**: Always pass an `AbortSignal` to streaming `fetch()` calls and call `reader.cancel()` on user stop or component unmount so local GPU generation halts immediately.
3. **Zero Silent Cloud Fallback**: Never silently route private local prompts to a remote cloud API when Ollama fails unless the user explicitly opted into hybrid cloud fallback.
