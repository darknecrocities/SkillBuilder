# AI & LLM Systems Error Catalog

Defects, failure modes, and recovery protocols for LLM APIs and autonomous agents.

---

### [AI-ERR-001] Model Schema Validation Failure
- **Symptom**: `pydantic_core._pydantic_core.ValidationError: 1 validation error for OutputSchema ...`
- **Root Cause**: Model returned markdown wrapping (e.g. ` ```json `) or omitted required schema property.
- **Remediation**:
  1. Pass Pydantic schema directly via `types.GenerateContentConfig(response_schema=MySchema, response_mime_type="application/json")`.
  2. Implement a sanitizer stripping markdown fences:
     ```python
     clean_json = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.text.strip(), flags=re.MULTILINE)
     ```

---

### [AI-ERR-002] Hallucinated Tool Parameters
- **Symptom**: Model calls `query_database(sql=...)` with invented parameter `filters_json` not declared in tool schema.
- **Root Cause**: Tool schema parameter description was ambiguous or conflicting with previous conversational context.
- **Remediation**: Add explicit JSON Schema parameter types and set `additionalProperties: false`.

---

### [AI-ERR-003] HTTP 429 Quota / Rate Limit Exhaustion
- **Symptom**: `google.genai.errors.APIError: 429 Resource has been exhausted (e.g. check quota)`.
- **Root Cause**: High-frequency parallel calls or token-per-minute (TPM) limit reached.
- **Remediation**:
  1. Wrap requests in exponential backoff retry with jitter (initial delay 2s, factor 2, jitter 0.5).
  2. Implement client-side token bucket rate limiter.
