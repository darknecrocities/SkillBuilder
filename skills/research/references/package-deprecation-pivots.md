# Package Deprecation & Production Pivot Catalog

> **Objective**: Immediately replace abandoned, CVEs-ridden, or C++-build-fragile libraries with modern, type-safe, zero-bloat production alternatives.

---

## 1. Approved Ecosystem Pivots

| Legacy / Fragile Package | Failure Mode | Approved Modern Replacement | Migration Advantage |
| :--- | :--- | :--- | :--- |
| **`google-generativeai`** | Deprecated Gemini SDK missing new live/caching APIs | **`google-genai`** (`from google import genai`) | Unified sync/async client, native Pydantic `response_schema`, explicit context caching |
| **`moment` / `moment-timezone`** | `~300 KB` mutable global bundle | **`date-fns`** or native **`Intl.DateTimeFormat`** | Tree-shakeable immutable functions or 0 KB platform built-in |
| **`request` / heavy `axios`** | Unmaintained (`request`) or unneeded bundle weight | Native **`fetch`** / **`undici`** (`AbortSignal.timeout`) | Built into Node 18+/20+ and browsers; native streaming |
| **`node-sass`** | C++ `node-gyp` build failures on ARM64/new Node | **`sass-embedded`** or **Tailwind CSS v4** | Native Dart Sass binary / CSS-first `@theme` engine |
| **`sqlite3` (async C++ build)** | Compilation failures on macOS/Docker | **`better-sqlite3`** (Node) or **`aiosqlite`** (Python) | Prebuilt binaries, `5–10x` faster prepared statements, WAL mode |
| **`enzyme`** | Coupled to React internal component state/instances | **`@testing-library/react`** + **Playwright** | Tests accessible user roles/labels (`Test Behavior, Not Implementation`) |
| **`pydantic` v1** | Slow Python-loop validation, deprecated `@validator` | **`pydantic` v2** (`@field_validator`, `model_validate`) | Rust `pydantic-core`, `5–10x` faster serialization & strict mode |
| **`canvas` (Cairo system deps)** | Fails in minimal Alpine/distroless containers | **`@napi-rs/canvas`** or pure **SVG** generation | Zero system Cairo/Pango apt dependencies via N-API prebuilds |

---

## 2. Pivot Execution Checklist
1. Never add a wrapper around the deprecated library — migrate callers cleanly and remove the legacy dependency (`Migrate Callers Then Delete Legacy APIs`).
2. Verify license compatibility (`MIT`, `Apache-2.0`, `BSD-3`) and run `npm audit` / `pip-audit` after swapping.
3. Run a 20-line smoke POC in `scratch/` confirming native bindings execute on the target OS/architecture before touching application files.
