# AWS Well-Architected Serverless Guidelines

Guidelines for resilient, secure, and cost-effective serverless architectures on Amazon Web Services.

---

## 1. AWS Lambda Best Practices

Rule | Specification | Rationale
:--- | :--- | :---
Memory Allocation | 1024MB – 2048MB | Lambda allocates proportional vCPU power alongside memory.
Timeout Bounds | 3s – 15s max | Prevent runaway billing and hanging client connections.
Provisioned Concurrency | Target spike endpoints | Eliminates cold start latencies on revenue-critical routes.
Dead-Letter Queues | SQS FIFO or SNS DLQ | Captures poisoned events for inspection without dropping messages.

---

## 2. Amazon S3 Bucket Hardening

1. **Public Access Block**: Enable `BlockPublicAcls`, `IgnorePublicAcls`, `BlockPublicPolicy`, and `RestrictPublicBuckets`.
2. **Server-Side Encryption**: Enforce `aws:kms` with customer-managed keys (SSE-KMS).
3. **Deletion Protection**: Configure S3 Object Lock and enable MFA Delete on root production buckets.
