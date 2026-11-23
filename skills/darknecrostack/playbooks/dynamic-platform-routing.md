# Playbook: Dynamic Platform & Target Routing (`dynamic-platform-routing`)

Shared instruction playbook for **`/darknecrostack`** and **`/full-scale-mode`**. Detect the active target (`mobile`, `app`, `web`, `universal`, or `ai-edge`) before loading UI, persistence, or subagent tracks so irrelevant rules are pruned (`~1,850+` tokens saved/turn).

## Target Routing Matrix

| Target | Repo / Prompt Signals | Mounted Skills & Playbook | Pruned Skills | Mandatory Execution Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`mobile`** | `ios/`, `android/`, `pubspec.yaml`, `app.json`, SwiftUI, Compose, Kotlin, iOS/Android | `/mobile-ui`, `/frontend`, `/state-management`, `playbooks/mobile-responsive.md` | `/web-ui` | Enforce `Compact`/`Medium`/`Expanded` layouts, safe areas, `44pt`/`48dp` targets, native springs. |
| **`app`** | `electron`, `tauri`, `desktop app`, `indexeddb`, `opfs`, `local-first`, `sqlite` | `/frontend`, `/local-first-data`, `/browser-media-wasm`, `/mcp-engineering` | `/mobile-ui`, unused cloud infra | Enforce Worker offloading, `URL.revokeObjectURL`, local-first public/private boundaries. |
| **`web`** | `next.config.*`, `tailwind.config.*`, `vite.config.*`, React, CSS, HTML | `/web-ui`, `/frontend`, `/routing`, `/state-management`, `playbooks/visual-parity.md` | `/mobile-ui` | Enforce `@container` queries, OKLCH, `44x44px` targets, `375px–1920px+` viewports. |
| **`universal`** | Both `mobile` + `web` (or `app` + `web`) manifests/targets | Fork isolated tracks (`Track-Web` vs `Track-Mobile` via `worker.md`) | Opposite platform inside each track | Never mount `/web-ui` and `/mobile-ui` inside the same subagent context. |
| **`ai-edge`** | `Modelfile`, `gguf`, `weights/`, `mmproj`, YOLO, VLM, Ollama, MLX | `/computer-vision`, `/vlm-multimodal`, `/local-llm`, `/ai-integration` | Client UI skills unless UI requested | Enforce `CV -> VLM -> LLM` cascade, `AI_PRIVACY_MODE`, bounded `maxsize=2` queues. |

## Steps
1. **Run Dynamic Inspection**: Execute `route_task.py --prompt "<goal>" --path .` or `verify_full_scale_orchestration.py --path . --asr`.
2. **Partition Subagents by Target**: For `universal` repos, assign separate `worker.md` briefs for Web, Mobile, App, and Backend/AI tracks.
3. **Execute & Verify**: Follow the matched target playbook (`mobile-responsive.md`, `visual-parity.md`, or `feature.md`) and close with `/prove-it-works`.
