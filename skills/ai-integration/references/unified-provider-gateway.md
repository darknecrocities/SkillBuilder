# Unified Provider Gateway & Environment Contract

> **Objective**: Allow any application (FastAPI, Next.js, Electron, Flutter, CLI) to switch seamlessly between Ollama, `llama.cpp`, MLX, vLLM, and Gemini without touching domain code.

---

## 1. Standard `.env.example` AI Contract

Include these keys in every AI-enabled project so local, staging, and production runtimes remain uniform:

```env
AI_PROVIDER=ollama                # ollama | llama_cpp | mlx | vllm | gemini
AI_PRIVACY_MODE=local_only        # local_only | hybrid_consent
AI_BASE_URL=http://127.0.0.1:11434/v1
AI_TEXT_MODEL=qwen2.5:7b-instruct-q4_K_M
AI_VLM_MODEL=qwen2.5vl:7b
AI_TIMEOUT_CONNECT_S=3.0
AI_TIMEOUT_READ_S=20.0
VLM_MAX_EDGE_PX=1280
CV_MODEL_PATH=models/yolov8n.onnx
CV_CONF_THRESHOLD=0.40
GEMINI_API_KEY=                   # Required only when AI_PRIVACY_MODE=hybrid_consent
```

---

## 2. Typed Gateway Interface & Privacy Gate (Python)

```python
from enum import Enum
import os
from typing import Protocol, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PrivacyMode(str, Enum):
    LOCAL_ONLY = "local_only"
    HYBRID_CONSENT = "hybrid_consent"


class ModelGateway(Protocol):
    async def generate_structured(self, prompt: str, schema: type[T], image_b64: str | None = None) -> T: ...
    async def health_check(self) -> dict[str, str]: ...


async def execute_with_privacy_gate(
    local_gw: ModelGateway,
    cloud_gw: ModelGateway | None,
    prompt: str,
    schema: type[T],
    image_b64: str | None = None,
) -> T:
    try:
        return await local_gw.generate_structured(prompt, schema, image_b64=image_b64)
    except (TimeoutError, ConnectionError) as err:
        privacy = PrivacyMode(os.getenv("AI_PRIVACY_MODE", PrivacyMode.LOCAL_ONLY.value))
        if privacy != PrivacyMode.HYBRID_CONSENT or cloud_gw is None:
            raise RuntimeError("LOCAL_AI_UNAVAILABLE_AND_CLOUD_BLOCKED_BY_PRIVACY") from err
        return await cloud_gw.generate_structured(prompt, schema, image_b64=image_b64)
```

---

## 3. Non-Blocking `/health/models` Probe

Expose a `1.5s`-bounded probe endpoint verifying: (1) CV ONNX session loaded, (2) Local LLM/VLM daemon reachable, and (3) Active privacy mode (`local_only` vs `hybrid_consent`). Never block application boot if an optional local daemon is offline—render explicit degraded recovery actions in UI.
