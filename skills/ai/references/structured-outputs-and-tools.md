# Structured Outputs & Defensive Tool Calling Manual

> **Objective**: Guarantee type-safe JSON responses and resilient function-calling loops that never crash or execute unsafe arguments.

---

## 1. Pydantic v2 / Zod Schema-Constrained Outputs

Always enforce output structure at decoding time rather than regex-parsing markdown code fences:

```python
from enum import Enum
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class Severity(str, Enum):
    LOW = "low"
    HIGH = "high"
    BLOCKER = "blocker"

class Finding(BaseModel):
    file_path: str
    severity: Severity
    rationale: str = Field(max_length=240)

class ReviewReport(BaseModel):
    findings: list[Finding]
    approved: bool

client = genai.Client()
res = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=diff_payload,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ReviewReport,
        temperature=0.0,
    ),
)
report: ReviewReport = res.parsed
```

---

## 2. Defensive Tool-Execution Wrapper

1. **Validate Before Running**: Parse model-generated tool arguments with Pydantic/Zod and sandbox filesystem paths (`realpath` prefix check) before hitting disk or DB.
2. **Max Loop Guard**: Cap autonomous tool loops (`max_iterations = 8–12`) to prevent runaway token spend on cyclic failures.
3. **Structured Error Return**: Return `{"ok": False, "code": "INVALID_PATH", "hint": "Use relative path inside src/"}` instead of propagating unhandled exceptions.
4. **Confirm Irreversible Tools**: Destructive tools (`delete_table`, `send_email`, `deploy_prod`) must require explicit human confirmation before execution.
