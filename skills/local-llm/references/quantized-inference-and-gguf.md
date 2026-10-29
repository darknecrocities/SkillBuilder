# Local LLM Quantized Inference & GGUF Formats

---

## 1. Quantization Level Trade-Offs

Quantization | Size / RAM | Perplexity Loss | Recommended Target
:--- | :--- | :--- | :---
`Q4_K_M` | $\approx 4.5\text{GB}$ (8B model) | Negligible ($\Delta < 0.05$) | Default for local edge workstations & laptops
`Q5_K_M` | $\approx 5.5\text{GB}$ (8B model) | Minimal | High-precision coding & mathematical analysis
`Q8_0` | $\approx 8.5\text{GB}$ (8B model) | Near FP16 accuracy | Reranking, critical extraction, small 3B models
`FP16` | $\approx 16\text{GB}$ (8B model) | 0 (baseline) | Model evaluation & quantization source

---

## 2. Local Inference Runtime Engine Matrix

- **Ollama**: Developer CLI and background REST server (`http://localhost:11434/api/generate`).
- **llama.cpp**: C++ engine with minimal memory footprint, metal acceleration on Apple Silicon, and GBNF grammar constraints.
- **MLX (Apple Silicon)**: Unified memory GPU execution optimized for M-series chips.
