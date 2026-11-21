# DynamoDB Single-Table Design & IAM Least Privilege

> **Objective**: Achieve predictable single-digit millisecond DynamoDB reads without expensive `Scan` operations or wildcard IAM permissions.

---

## 1. Single-Table Access Pattern Modeling

List all query patterns *before* defining keys (`PK`, `SK`, `GSI1PK`, `GSI1SK`):

| Entity | `PK` | `SK` | Query Supported |
| :--- | :--- | :--- | :--- |
| **Tenant Profile** | `TENANT#<tenantId>` | `META` | `GetItem` by tenant ID |
| **User Membership** | `TENANT#<tenantId>` | `USER#<userId>` | `Query` all users in tenant (`begins_with(SK, "USER#")`) |
| **Project Task** | `TENANT#<tenantId>#PROJ#<projId>` | `TASK#<ulid>` | Time-ordered tasks scoped strictly to tenant |

### Non-Negotiable DynamoDB Guardrails
- **Ban `Scan` in Request Paths**: Never run `dynamodb.scan()` on production API endpoints (`O(N)` table read + throttled RCU spikes). Always use `GetItem`, `BatchGetItem`, or `Query` with explicit partition keys.
- **Conditional Writes (`ConditionExpression`)**: Prevent lost updates and duplicate creations using `attribute_not_exists(PK)` or optimistic `version = :expected`.
- **IAM Least Privilege**: Scope task/Lambda IAM policies to exact resource ARNs (`arn:aws:dynamodb:region:acct:table/app-prod`) and exact actions (`dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:Query`) — never `"Action": "dynamodb:*"` on `"Resource": "*"`.
