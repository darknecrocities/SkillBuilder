# Defensive Error Handling, Exception Safety & Resilience Manual

This manual establishes engineering standards for try/catch exception handling, information disclosure defense, and process lifecycle resilience.

---

## 1. The Zero-Silent-Swallowing Rule

Catching exceptions without structured logging, telemetry, or intentional recovery leaves systems in an inconsistent state and blinds engineering teams:

```typescript
// ❌ VULNERABLE: Silent error swallowing blinds telemetry and conceals database corruption
try {
  await db.transaction(async (tx) => {
    await tx.updateAccount(fromId, -amount);
    await tx.updateAccount(toId, amount);
  });
} catch (e) {
  // Silent swallow - transaction state unknown!
}

// ✅ DEFENSIVE: Explicit error boundary with structured logging, metrics, and typed rethrow
try {
  await db.transaction(async (tx) => {
    await tx.updateAccount(fromId, -amount);
    await tx.updateAccount(toId, amount);
  });
} catch (error) {
  const correlationId = crypto.randomUUID();
  logger.error("Transaction failed during fund transfer", {
    correlationId,
    fromId,
    toId,
    error: error instanceof Error ? error.message : "Unknown error",
  });
  throw new DomainTransactionException("Fund transfer failed", { cause: error, correlationId });
}
```

### Python Exception Hygiene
```python
# ❌ VULNERABLE: Bare except catches SystemExit and KeyboardInterrupt, concealing errors
try:
    process_payment(order_id)
except:
    pass

# ✅ DEFENSIVE: Specific exception handling with audit trails and contextual chaining
try:
    process_payment(order_id)
except PaymentGatewayError as err:
    logger.error("Payment gateway rejected order", extra={"order_id": order_id, "error": str(err)})
    raise OrderProcessingException(f"Payment failed for order {order_id}") from err
```

---

## 2. Zero Information Disclosure (RFC 7807 Problem Details)

In production, internal error details (database tables, SQL queries, file system paths, library versions, and stack traces) must **never** be transmitted to the client. Attackers use internal stack traces to map application topologies and exploit zero-day libraries.

### RFC 7807 Standard Error Contract
All API errors must follow `application/problem+json`:

```json
{
  "type": "https://api.example.com/errors/invalid-credentials",
  "title": "Invalid Credentials",
  "status": 401,
  "detail": "The provided username or password is incorrect.",
  "instance": "/api/v1/auth/login",
  "error_id": "err_c9f2b84a1e"
}
```

### Error Sanitization Pipeline
```text
┌─────────────────────────┐
│ Raw Internal Exception  │  --> DatabaseError: relation "users" does not exist at L14
└─────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│  Security Error Filter  │  --> Strip stack trace, assign opaque error_id ("err_c9f2b8")
└─────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│ Client-Facing Response  │  --> RFC 7807: "An internal database error occurred." (Status: 500)
└─────────────────────────┘
```

---

## 3. Fail-Safe Degradation Patterns

Isolate non-critical auxiliary features (telemetry, cache warming, recommendation engines, webhook dispatch) with local try/catch boundaries so core business transactions succeed even if background tasks fail:

```typescript
export async function completeOrder(orderId: string): Promise<OrderResult> {
  // 1. Core Critical Path: Must succeed or throw
  const order = await orderRepository.finalize(orderId);

  // 2. Auxiliary Path: Fail-safe degradation
  try {
    await analyticsClient.track("order_completed", { orderId });
  } catch (auxError) {
    // Non-blocking warning: order completion must NOT fail if analytics is offline
    logger.warn("Non-critical analytics dispatch failed", { orderId, error: auxError });
  }

  return { success: true, orderId: order.id };
}
```

---

## 4. Process Boundary & Crash Resilience

Node.js and Python processes must handle uncaught exceptions and graceful shutdown signals without dropping in-flight requests or corrupting socket connections:

```typescript
// Graceful Shutdown Handler (Node.js)
process.on("unhandledRejection", (reason: unknown) => {
  logger.fatal("Unhandled Promise Rejection detected", { reason });
  gracefulShutdown(1);
});

process.on("uncaughtException", (error: Error) => {
  logger.fatal("Uncaught Exception at process boundary", { error: error.message, stack: error.stack });
  gracefulShutdown(1);
});

function gracefulShutdown(exitCode: number) {
  server.close(() => {
    database.disconnect().finally(() => {
      process.exit(exitCode);
    });
  });

  // Force shutdown after 10-second timeout if connections hang
  setTimeout(() => process.exit(exitCode), 10_000).unref();
}
```
