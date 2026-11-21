# Gemini SDK (`google-genai`) & Model Selection Matrix

> **Objective**: Standardize production Python/TypeScript calls on the unified `google-genai` SDK with predictable latency, cost, and safety settings.

---

## 1. Official SDK Setup (Zero Legacy `google-generativeai`)

```python
import os
from google import genai
from google.genai import types

# Reads GEMINI_API_KEY from environment cleanly (never hardcode keys)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
```

---

## 2. Task-to-Model Selection Matrix

| Workload Tier | Recommended Model | Temperature | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **High-Volume / Routing** | `gemini-2.5-flash-lite` | `0.0–0.1` | Classification, intent routing, PII scrub, simple extraction |
| **Balanced Workhorse** | `gemini-2.5-flash` | `0.1–0.3` | Structured JSON extraction, RAG synthesis, tool-calling agents |
| **Deep Reasoning / Review** | `gemini-2.5-pro` | `0.2–0.4` | Complex multi-file architecture, adversarial review, forensics |

---

## 3. Streaming, Timeouts & Resilience

1. **Always Configure Timeouts**: Wrap network/API calls with explicit deadlines (`http_options={"timeout": 15000}` ms) so stalled streams never hang worker queues.
2. **Async Streaming**: Use `client.aio.models.generate_content_stream(...)` in FastAPI/Node SSE endpoints and wire `AbortController` / client disconnect cancellation cleanly.
3. **Multimodal Hygiene**: Upload large videos/PDFs (`> 20 MB`) via `client.files.upload()` and poll file processing state asynchronously or delete temporary files after session completion.
4. **System Instructions Separation**: Keep immutable role/schema rules in `system_instruction` and untrusted user/document data strictly inside `contents`.
