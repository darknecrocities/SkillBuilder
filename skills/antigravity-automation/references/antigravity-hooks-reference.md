# Antigravity Lifecycle Hooks Reference (`hooks.json`)

Antigravity Customization System lifecycle hooks intercept events in the agent loop to execute shell commands, validate safety constraints, format code, and collect diagnostics.

---

## 1. Supported Lifecycle Events

Event | When Triggered | Use Cases
:--- | :--- | :---
`SessionStart` | Once when a new conversation session initiates | Environment pre-flight check, backup manifest integrity
`PreToolUse` | Right before a specific tool is executed | Safety gates, blocking destructive SQL/filesystem commands
`PostToolUse` | Immediately after a tool finishes execution | 500-line limit check, linter runs, formatting code
`PreInvocation`| Before calling the AI model | Token budget estimation, context invariant reinforcement
`PostInvocation`| After tool calls finish | Telemetry logging, post-step validation
`Stop` | When the agent execution loop finishes | Final health report, lease lock cleanup

---

## 2. Matcher Patterns & Exit Codes

```json
{
  "safety-gate": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "command": "python3 scripts/hooks/pre_tool_use_safety.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Exit Code Semantics:
- **`Exit Code 0`**: Success / Pass. Execution proceeds unimpeded.
- **`Exit Code 1` / Non-Zero**: Advisory Warning / Failure. Output is surfaced to agent context.
- **`Exit Code 2`**: Hard Intercept. Aborts tool execution immediately and alerts user.
