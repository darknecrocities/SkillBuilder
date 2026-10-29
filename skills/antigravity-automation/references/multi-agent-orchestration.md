# Antigravity Multi-Agent Orchestration & Reactive Wakeups

Antigravity features a native subagent messaging mesh that enables parallel execution pipelines with zero polling.

---

## 1. Subagent Lifecycle Tools

Tool | Primary Purpose | Key Parameters
:--- | :--- | :---
`invoke_subagent` | Launch isolated worker subagent in background | `TypeName`, `Role`, `Prompt`, `Workspace`, `Model`
`define_subagent` | Dynamically register a specialized agent type | `Name`, `Description`, `SystemPrompt`, `EnableWriteTools`
`send_message` | Deliver asynchronous message to subagent | `Recipient` (conversationId), `Message`
`manage_subagents` | List active subagents or terminate them | `Action`: `"list"`, `"kill"`, `"kill_all"`

---

## 2. Reactive Wakeup Protocol

The primary agent terminates its turn immediately after dispatching tasks:
```text
Parent Agent dispatches Task A & Task B via invoke_subagent()
Parent Agent calls no more tools (Sleep State)
Subagent A finishes and sends completion message
Antigravity automatically wakes Parent Agent with Subagent message in context
Zero while loops. Zero polling. Zero wasted tokens.
```

---

## 3. Shared Backup Manifest Lease Locking

When multiple concurrent subagents perform disk writes, schema migrations, or cloud modifications:
1. Each subagent reads `.backups/backup_manifest.json`.
2. Inspects existing SHA-256 backup entries.
3. If state is unchanged, reuses the canonical backup slot (zero timestamped `*.bak.1` duplicates).
4. Commits atomic updates before releasing the lease.
