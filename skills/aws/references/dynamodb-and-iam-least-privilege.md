# Amazon DynamoDB Single-Table Design & IAM Least Privilege

---

## 1. DynamoDB Single-Table Architecture

Attribute | Convention | Example
:--- | :--- | :---
`PK` (Partition Key) | Entity namespace + ID | `USER#usr_123`, `ORG#org_456`
`SK` (Sort Key) | Sub-entity / event timestamp | `METADATA`, `ORDER#2026-10-29`
`GSI1PK` / `GSI1SK` | Secondary lookup index | `STATUS#PENDING`, `DATE#2026-10-29`

### Query Discipline:
- Always query with exact `PK` and optional `SK` condition (`begins_with`, `between`).
- Prohibit unindexed table scans (`dynamodb:Scan`) across production workloads.

---

## 2. IAM Least Privilege Standards

1. Scope permissions down to specific ARN resources (never `Resource: "*"` on write actions).
2. Separate Deployment roles from Execution roles.
3. Attach explicit condition keys (e.g. `aws:PrincipalTag`, `aws:SourceVpc`).
