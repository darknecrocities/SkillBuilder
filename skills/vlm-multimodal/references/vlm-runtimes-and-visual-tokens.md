# VLM Runtimes, Visual Token Math & Keyframe Sampling

> **Objective**: Eliminate visual token explosions, slow VLM prefill latency, and naive video-frame loops across local and cloud multimodal pipelines.

---

## 1. Visual Token Cost by Architecture

Unlike text (~`3.8` chars/token), a single high-res image can consume `1,500–4,000+` visual tokens and dominate KV-cache memory:

| VLM Family | Patch / Tile Mechanism | Recommended Pre-Resize Cap | Approx Tokens / Image |
| :--- | :--- | :--- | :--- |
| **Qwen2.5-VL** | Dynamic `28x28` pixel patches (`1` token per patch) | Clamp `max_pixels = 1280 * 28 * 28` (`~1M` px) | `~256–1,280` tokens |
| **Llama-3.2-Vision** | `560x560` image tiles (up to 4 tiles) | Fit inside `1120x1120` or `560x560` for thumbnails | `~1,600–6,400` tokens |
| **Gemini 2.5 Flash** | Fixed/tiled media resolution (`MEDIA_RESOLUTION_LOW/MEDIUM`) | `<= 1568px` long edge (or `MEDIA_RESOLUTION_LOW` for batch) | `258` (low) / `~1,290` (high) |

---

## 2. Pre-Encode Image Downscaling & Ollama / `mlx-vlm` Call

Always normalize EXIF orientation and resize before base64 encoding, and pass a strict JSON schema + timeout:

```python
import base64
import io
import requests
from PIL import Image, ImageOps


def encode_vlm_image(path: str, max_edge: int = 1280) -> str:
    with Image.open(path) as raw:
        img = ImageOps.exif_transpose(raw).convert("RGB")
        img.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode("ascii")


def inspect_image_ollama(path: str, schema: dict) -> dict:
    payload = {
        "model": "qwen2.5vl:7b",
        "messages": [{"role": "user", "content": "Extract receipt fields.", "images": [encode_vlm_image(path)]}],
        "format": schema,
        "stream": False,
    }
    res = requests.post("http://127.0.0.1:11434/api/chat", json=payload, timeout=(3.0, 25.0))
    res.raise_for_status()
    return res.json()
```

---

## 3. Video Keyframe & Scene-Delta Sampling

Never feed consecutive redundant frames from `cv2.VideoCapture` into a VLM:
- **Temporal Stride**: Decode at `fps` intervals (`frame_idx % int(fps) == 0`) for `<= 1 fps` sampling.
- **L1/Histogram Scene Gate**: Compute mean absolute difference between grayscale `64x64` thumbnails (`np.mean(np.abs(curr - prev)) > 12.0`); discard static frames before invoking any VLM.
- **Cloud Long Video**: Upload MP4 once via `google-genai` `client.files.upload()` instead of uploading hundreds of individual JPEGs.
