# Playbook: Runtime Forensics

Use when debugging production crashes, OOM kills, zombie workers, `createObjectURL` leaks, or unhandled async rejections.

## Steps
1. **Capture Exact Runtime Evidence**: Collect full stack trace, exit signal (`SIGKILL`/`OOM`), heap snapshot delta, or browser console/network log.
2. **Audit Resource Lifecycles**: Check teardown paths (`AbortController`, `URL.revokeObjectURL`, `worker.terminate()`, Rive `cleanup()`, DB pool `end()`, WebAudio `close()`).
3. **Check Silent Swallowing**: Scan for `catch (e) {}` or swallowed promise rejections hiding the true failure point.
4. **Apply Surgical Fix + Leak Regression Test**: Fix lifecycle ownership and add a test proving cleanup executes on error and unmount paths.
