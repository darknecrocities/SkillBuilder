# AWS Well-Architected Serverless, S3 Security & Deletion Protection

> **Objective**: Build resilient AWS Lambda, API Gateway, and S3 architectures with least-privilege IAM, private buckets, and stateful retention.

---

## 1. S3 Bucket Hardening & Encryption

Every S3 bucket provisioned via CDK, Terraform, or CloudFormation MUST enforce:
1. **Block All Public Access**: `BlockPublicAcls: true`, `BlockPublicPolicy: true`, `IgnorePublicAcls: true`, `RestrictPublicBuckets: true`.
2. **Encryption at Rest**: `SSE-KMS` (customer-managed key with rotation) or `SSE-S3` + bucket key enabled.
3. **Enforce TLS in Transit**: Bucket policy denying any request where `aws:SecureTransport == "false"`.
4. **Stateful Retention**: Set `RemovalPolicy.RETAIN` (CDK) / `lifecycle { prevent_destroy = true }` (Terraform) — never enable `force_destroy = true` or `autoDeleteObjects: true` in production without explicit user confirmation.

---

## 2. AWS Lambda Resilience & Connection Hygiene

- **Initialize Clients Outside Handler**: Create AWS SDK v3 clients and DB pools in module scope so warm invocations reuse TCP/TLS connections; cap Lambda concurrency (`reservedConcurrentExecutions`) to protect RDS/Aurora connections (or use RDS Proxy).
- **Idempotency & DLQs**: Wire SQS/SNS/EventBridge async triggers to an **SQS Dead-Letter Queue (DLQ)** (`maxReceiveCount = 3`) and enforce AWS Lambda Powertools idempotency keys on mutating handlers.
- **Timeouts**: Align Lambda timeout (`<= 15s` API / explicit step timeouts) strictly below API Gateway (`29s` max) and downstream SDK request timeouts (`3s` connect / `10s` read).
