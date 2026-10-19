# Gemini API & Google GenAI SDK Patterns

Best practices for building with Gemini models using the modern `google-genai` SDK.

---

## 1. SDK Initialization & Modern Syntax
Always use the unified `google-genai` SDK (`from google import genai`):

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Analyze the failure mode in this stack trace...",
    config=types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=1000,
    ),
)
print(response.text)
```

---

## 2. Model Selection Matrix

| Model Tier | Ideal Workload | Latency Target | Token Ceiling |
| :--- | :--- | :--- | :--- |
| **gemini-2.5-flash** | High-speed classification, API routing, code linter | Ultra Low (< 1s) | 1,000,000 tokens |
| **gemini-2.5-pro** | Complex refactoring, architecture plans, multi-step math | Deep Reasoning | 2,000,000 tokens |
| **gemini-live** | Bidirectional real-time audio/video streaming | Sub-500ms streaming | Real-time sessions |
