# AI Systems Error & Failure Mode Catalog

> **Objective**: Fast diagnosis and deterministic fixes for common LLM, Gemini SDK, RAG, and multi-agent failures.

---

## 1. SDK, Schema & Tool-Calling Errors

| Error Signature | Root Cause | Production Remediation |
| :--- | :--- | :--- |
| `ImportError: google.generativeai` / deprecated API | Using legacy `google-generativeai` package instead of `google-genai`. | Migrate to `from google import genai; client = genai.Client()`. |
| `JSONDecodeError` or missing fields in tool response | Relying on `"Please respond only in JSON"` prompt text instead of schema constraints. | Pass `response_mime_type="application/json"` + `response_schema=PydanticModel` (`temperature <= 0.2`). |
| Agent infinite retry loop on tool error | Tool raises raw exception crashing runner or returns vague `"Error"`. | Catch tool exceptions and return structured JSON `{"error": "CODE", "recoverable": bool, "hint": "..."}`. |
| Subagent ignores `/anti-slop` or `/security` rules | Slash commands do not propagate automatically to spawned subagents. | Start every subagent kickoff with `Read <abs>/skills/darknecrostack/worker.md before anything else.` |
| `429 RESOURCE_EXHAUSTED` burst | Unbounded parallel LLM calls without concurrency cap or jitter. | Bound concurrency (`asyncio.Semaphore(4)`) and retry transient `429`/`503` with exponential backoff + jitter. |

---

## 2. RAG, Memory & Evaluation Failures

| Failure Pattern | Diagnostic Probe | Remediation |
| :--- | :--- | :--- |
| **Multi-tenant data leak in RAG** | Query chunks as Tenant B using keywords unique to Tenant A. | Enforce `WHERE tenant_id = $1` pre-filtering in SQLite/Postgres `pgvector` before similarity ranking. |
| **Context Rot / Lost-in-the-Middle** | Prompt exceeds 70% context window with unpruned files. | Use PDS pruning, file pointers, and subagent summaries; move static specs to Gemini Context Cache. |
| **Silent Eval Regression** | Prompt tweak improves Case A but breaks JSON schema on Case B. | Maintain golden eval suite (`playbooks/eval.md`) running all edge cases after every prompt edit. |
