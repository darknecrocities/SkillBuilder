# Structured Outputs & Function Calling

Deterministic schema enforcement and safe tool orchestration.

---

## 1. Schema-Constrained Outputs (Pydantic Integration)

```python
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class CodeReviewSummary(BaseModel):
    verdict: str = Field(description="APPROVE, REQUEST_CHANGES, or COMMENT")
    security_risk_level: str = Field(description="CRITICAL, HIGH, MEDIUM, LOW, or NONE")
    findings: list[str] = Field(description="Specific actionable code findings")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Review this pull request diff...",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=CodeReviewSummary,
    ),
)
# Validated typed object
review = CodeReviewSummary.model_validate_json(response.text)
```

---

## 2. Defensive Tool Calling Execution
- Always validate arguments provided by the model before executing system commands.
- Return structured tool outputs (`{"status": "success", "result": ...}` or `{"status": "error", "message": ...}`).
