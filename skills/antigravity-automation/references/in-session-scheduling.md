# Antigravity In-Session Scheduling & Background Tasks

In-session automations run within an ongoing agent conversation. Antigravity provides native tooling for one-shot timers, recurring crons, asynchronous background processes, and reactive wakeups.

---

## 1. The `schedule` Tool Specification

The `schedule` tool enables non-blocking scheduling without consuming active turn compute:

```python
# One-Shot Delay Timer
schedule(
    DurationSeconds=120,
    Prompt="Notification: 2-minute build verification window completed. Run test suite now.",
    TimerCondition="never"  # 'never', 'any', or specific sender subagent ID
)

# Recurring In-Session Cron
schedule(
    CronExpression="*/15 * * * *",
    Prompt="Scheduled Health Check: Verify server response codes and report anomalies.",
    MaxIterations=10,
    IsDaemon=False
)
```

### Critical Rules:
- **Zero Busy-Waiting**: Never use shell `sleep` commands or while-true polling loops. The `schedule` tool automatically wakes the agent.
- **TimerCondition**: When set to `"any"` or a subagent conversation ID, arriving messages cancel the timer early and wake the agent immediately.
- **`IsDaemon`**: Set `IsDaemon: true` **only** if the cron must survive after the current conversation completes.

---

## 2. Background Daemons with `run_command` and `manage_task`

For long-running compilers, dev servers, or file watchers:

```python
# Launch background task
run_command(
    CommandLine="npm run dev",
    IsDaemon=True,
    WaitMsBeforeAsync=500,
    toolSummary="Dev server startup"
)
```

Use `manage_task` to inspect and control:
- `Action: "list"`: Enumerate all running background tasks.
- `Action: "status"`: Check logs and exit code for a specific `TaskId`.
- `Action: "send_input"`: Deliver stdin to interactive processes.
- `Action: "kill"`: Terminate runaway processes.
