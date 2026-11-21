# Token Optimization, Context Caching & Prompt Compression

> **Objective**: Cut per-turn LLM token spend by `40–70%` without sacrificing reasoning accuracy or violating context limits.

---

## 1. Progressive Disclosure & Platform Pruning (PDS)

Never dump unrelated platform instructions or massive doc walls into the prompt:
1. **Skill Pruning**: On a web task, suppress `/mobile-ui`; on a mobile task, suppress `/web-ui` (`~1,850` tokens saved per turn).
2. **File Pointers Over Inline Walls**: Pass `Read skills/darknecrostack/worker.md` and `src/routes/auth.ts#L40-95` to subagents rather than pasting 400 lines into the prompt.
3. **Targeted Reads**: Search first (`rg -n`), then read bounded line windows (`150` lines) rather than ingesting entire files.

---

## 2. Gemini Explicit Context Caching (`google-genai`)

When querying large static corpora (codebase specs, legal docs, schemas `> 32k` tokens) across 3+ turns, create an explicit context cache instead of re-sending the prefix every request:

```python
from google import genai
from google.genai import types

client = genai.Client()
cache = client.caches.create(
    model="gemini-2.5-flash",
    config=types.CreateCachedContentConfig(
        display_name="architecture-spec-v1",
        system_instruction="Answer strictly from the architecture specification.",
        contents=[spec_markdown_payload],
        ttl="1800s",
    ),
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="List all rate-limit thresholds for /auth/login.",
    config=types.GenerateContentConfig(cached_content=cache.name, temperature=0.1),
)
```

---

## 3. Output Token Compression & Structured Diffs

| Wasteful Pattern | Optimized Pattern |
| :--- | :--- |
| Repeating 300 unmodified lines around a 4-line fix | Emit exact search/replace patch or unified diff |
| Prose paragraphs explaining 12 parameters | Compact 3-column markdown table |
| Long reasoning + conversational padding | One-sentence goal + direct output + `[measured]` receipt |

---

## 4. Context Window Safety Budget
- Reserve `>= 25%` of the model's context window for tool outputs and verification logs; trigger `/compact` or subagent delegation when active context crosses `70%` capacity.
