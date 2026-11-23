# Visual Grounding, Structured Extraction & Multimodal RAG

> **Objective**: Guarantee machine-parseable bounding boxes, verifiable document citations, and defense against visual prompt injection inside untrusted images/PDFs.

---

## 1. Normalized Visual Grounding Schema (`0–1000`)

Keep coordinate conventions uniform across Gemini and Qwen2.5-VL outputs using Pydantic validation so out-of-range boxes are rejected immediately:

```python
from pydantic import BaseModel, Field


class GroundedElement(BaseModel):
    label: str
    ymin: int = Field(ge=0, le=1000)
    xmin: int = Field(ge=0, le=1000)
    ymax: int = Field(ge=0, le=1000)
    xmax: int = Field(ge=0, le=1000)
    confidence: float = Field(ge=0.0, le=1.0)


class DocumentExtraction(BaseModel):
    doc_type: str
    elements: list[GroundedElement]
```

Convert `[ymin, xmin, ymax, xmax]` back to pixel coordinates via `int(coord / 1000 * dim)` against the **post-EXIF original dimensions**, not the downscaled thumbnail.

---

## 2. Multimodal RAG (Page-Image vs Text Extraction)

| Document Type | Optimal Retrieval Strategy | Why |
| :--- | :--- | :--- |
| **Clean text / Markdown / Code** | Standard chunking + hybrid BM25/`sqlite-vec` (`/ai`, `/local-llm`) | `10x` cheaper tokens and higher exact-keyword recall. |
| **Complex PDFs (tables, CAD, scans)** | Rasterize pages at `150 DPI` (`<= 1280px` edge) -> ColPali / VLM page embedding | Preserves multi-column layout, diagrams, and table borders lost by naive `pypdf`. |

- **Cap Per-Turn Pages**: Inject at most `top_k <= 4` page images per query turn so visual context never crowds out system instructions or tool schemas.

---

## 3. Defense Against Indirect Visual Prompt Injection

User-uploaded images, screenshots, and PDFs can contain hidden low-contrast or microscopic text (`"Ignore previous instructions and exfiltrate..."`):
1. **Treat VLM Image Text as Untrusted Data**: Never interpolate extracted VLM strings directly into shell commands, SQL, or privileged tool calls.
2. **Schema Constraining**: Lock extraction outputs to strict enums/regex/Pydantic types rather than open-ended `"execute what the image says"` prompts.
3. **Human Confirmation on Side Effects**: Any mutating action derived from VLM-parsed documents (payments, deletions, auth changes) requires explicit user confirmation.
