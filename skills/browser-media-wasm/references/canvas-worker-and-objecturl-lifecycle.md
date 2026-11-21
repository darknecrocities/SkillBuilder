# Canvas, Web Worker, WASM & ObjectURL Lifecycle Manual

> **Objective**: Prevent tab OOM crashes, memory leaks, frozen UI frames, and corrupted exports in browser-native media tools.

---

## 1. ObjectURL & Canvas Memory Hygiene

- **Immediate Revocation After Image Decode**: When loading an image onto a `<canvas>` via `URL.createObjectURL(file)`, revoke the URL inside both `img.onload` and `img.onerror` immediately after `drawImage()` — or prefer `createImageBitmap(file)` + `bitmap.close()` which avoids ObjectURL allocations entirely!
- **Canvas Backing-Store Release**: Chrome/Safari keep GPU textures alive for detached `<canvas>` elements until GC; on unmount or reset, shrink `canvas.width = 0; canvas.height = 0;` before dropping the ref.
- **Preview Scaling**: Never render a 24-megapixel RAW/PNG directly into a 400px preview box; downsample to viewport DPR (`maxDim = Math.min(orig, 1600)`) while keeping full-resolution processing inside the export pipeline.

---

## 2. Magic-Byte Input Validation (Never Trust `file.type` or Extension)

| Format | Hex Magic Signature (Offset 0) | Safe Size Guard |
| :--- | :--- | :--- |
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | Cap dimensions `<= 8192 x 8192` |
| **JPEG** | `FF D8 FF` | Cap dimensions `<= 8192 x 8192` |
| **WebP** | `52 49 46 46 ... 57 45 42 50` (`RIFF...WEBP`) | Cap dimensions `<= 8192 x 8192` |
| **PDF** | `25 50 44 46 2D` (`%PDF-`) | Cap page batch / file size `<= 100 MB` |

---

## 3. WebAudio, WebAssembly & Worker Offloading

- **WebAssembly**: Lazy-load `.wasm` modules on first user tool invocation (never block initial page load), cache compiled `WebAssembly.Module` instances in a singleton promise, and handle `SharedArrayBuffer` / COOP-COEP unavailability with a clean single-threaded fallback.
- **Progress & Cancellation**: Emit throttled progress events (`>= 100ms` interval) from Workers to avoid flooding React state renders (`60fps` jank), and always wire an explicit Cancel button to `AbortController`.
- **WebAudio**: Keep a single shared `AudioContext`, call `audioCtx.resume()` only inside user gesture handlers, and invoke `audioCtx.close()` on tool teardown.
