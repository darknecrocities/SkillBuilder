# MCP Transport Lifecycle, Tool Contracts & Sandboxing Manual

> **Objective**: Ensure local and remote MCP servers stay resilient under malformed tool arguments, symlink escape attempts, noisy child processes, and abrupt client disconnects.

---

## 1. Transport Selection & Stream Purity

| Transport | Best Fit | Critical Failure Mode | Mitigation |
| :--- | :--- | :--- | :--- |
| **`stdio`** | Local IDE / CLI agents | Any `console.log()` or library banner corrupts JSON-RPC framing on `stdout`. | Route all app logs to `process.stderr` (`console.error`); validate child exit signals (`SIGTERM`/`SIGINT`). |
| **`Streamable HTTP` / `SSE`** | Browser clients, local daemons | Leaked SSE intervals/connections on client abort, missing CORS origin lock. | Bind `req.on("close")` to abort work and clear timers; restrict CORS to explicit `localhost` origins. |

---

## 2. Tool Naming & Schema Design Rules

1. **Verb-Noun Clarity**: Name tools unambiguously (`read_workspace_file`, `search_civic_records`) and state side effects (`[READ-ONLY]` vs `[MUTATING]`) in the description.
2. **Strict Input Bounds**:
   - Cap string lengths (`.max(4096)`), array counts (`.max(100)`), and pagination limits (`limit <= 200`).
   - Use `additionalProperties: false` / `.strict()` so hallucinated parameter keys fail fast with clear schema feedback.
3. **Structured Error Envelopes**: Never leak internal stack traces or absolute host secrets; return deterministic error codes (`FILE_NOT_FOUND`, `PATH_OUTSIDE_WORKSPACE`, `TIMEOUT_EXCEEDED`, `INVALID_SCHEMA`) with actionable hints so the calling model can recover cleanly.

---

## 3. Filesystem & Subprocess Guardrails

- **Symlink Traversal Defense**: `path.resolve(root, input).startsWith(root)` is bypassed by symlinks pointing outside `root`. Always resolve via `fs.realpathSync` / `os.path.realpath` on existing paths or parent directories.
- **Read/Write Separation**: Expose read tools (`readOnlyHint: true`) separately from mutating write tools; check file size (`stat.size <= 5 MB`) before loading into memory.
- **Bounded Command Output**: Truncate `stdout`/`stderr` buffers beyond `1 MB` and enforce hard timeouts (`timeoutMs <= 30_000`) so runaway commands cannot OOM the host.
- **Zero Credential Echo**: Scrub `.env` tokens and bearer headers from tool outputs and exception messages.
