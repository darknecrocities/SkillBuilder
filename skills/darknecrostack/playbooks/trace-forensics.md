# Playbook: Trace Forensics

Use when diagnosing tail latency spikes, distributed request drops, or multi-hop timeout cascades.

## Steps
1. **Correlate by Trace ID**: Pull `X-Correlation-ID` / W3C `traceparent` spans across ingress, service, DB, and downstream calls.
2. **Locate Critical-Path Span**: Identify whether delay sits in DNS/TLS handshake, queue wait, lock contention, serialized `await` loops, or missing 3s/15s timeouts.
3. **Check Retry Amplification**: Verify retries use bounded exponential backoff + full jitter and never retry non-idempotent POSTs or 4xx responses.
4. **Fix & Verify Latency Distribution**: Parallelize independent I/O, add indexes/timeouts, and compare before/after `p95` spans.
