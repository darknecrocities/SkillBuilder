# CV Runtime Execution Providers & Bounded Frame Pipelines

> **Objective**: Maintain deterministic `<= 33ms` frame processing on live streams without memory leaks, stale-frame lag, or silent CPU fallback.

---

## 1. Bounded Producer-Consumer Frame Ingestion

A camera or RTSP stream running at `30 fps` will OOM a worker within seconds if inference runs at `12 fps` and pushes into an unbounded `queue.Queue()`. Always use a `maxsize=2` drop-oldest ring buffer and release `cv2.VideoCapture` in `finally`:

```python
import queue
import threading
import cv2


class BoundedFrameGrabber:
    def __init__(self, source: str | int) -> None:
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"CV_CAPTURE_OPEN_FAILED: {source}")
        self.frames: queue.Queue = queue.Queue(maxsize=2)
        self._stop = threading.Event()

    def run(self) -> None:
        try:
            while not self._stop.is_set():
                ok, frame = self.cap.read()
                if not ok:
                    break
                if self.frames.full():
                    try:
                        self.frames.get_nowait()
                    except queue.Empty:
                        pass
                self.frames.put_nowait(frame)
        finally:
            self.cap.release()
```

---

## 2. Explicit ONNX Runtime Execution Providers

Calling `ort.InferenceSession("model.onnx")` without `providers=[...]` can silently fall back to single-threaded CPU execution when CUDA/CoreML libraries fail to load. Pin explicit provider priority and inspect `session.get_providers()` at startup:

```python
import onnxruntime as ort

def load_detector(onnx_path: str) -> ort.InferenceSession:
    opts = ort.SessionOptions()
    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    session = ort.InferenceSession(
        onnx_path,
        sess_options=opts,
        providers=["CUDAExecutionProvider", "CoreMLExecutionProvider", "CPUExecutionProvider"],
    )
    return session
```

---

## 3. Edge Quantization & Browser WebGPU Offloading

| Target | Quantization / Export | Critical Guardrail |
| :--- | :--- | :--- |
| **NVIDIA TensorRT** | FP16 default; INT8 with `>= 500` representative calibration frames | Pin engine cache per GPU SM architecture; never cross-load `.engine` files across GPU SKUs. |
| **Apple CoreML** | FP16 / W8A16 (`coremltools`) | Keep fixed input shapes (`640x640`) so ANE compiles once without runtime recompilation stalls. |
| **Browser WebGPU / WASM** | ONNX `fp16` / `q8` inside dedicated Web Worker | Call `tensor.dispose()` after every `session.run()` and terminate Worker on unmount (`/browser-media-wasm`). |
