# Clean Code and Maintainability Standards

This guide outlines code-level best practices to ensure all written code is readable, maintainable, testable, and robust.

---

## 1. Intentional Naming

- **Communicate Intent**: Name variables, functions, and classes after their purpose and domain meaning, not their internal data structure or technical mechanism.
  - *Bad*: `data_list`, `tmp_obj`, `handleStuff()`, `flag2`
  - *Good*: `activeUserAccounts`, `pendingInvoiceRecord`, `reconcileBillingStatements()`, `isPaymentAuthorized`
- **Boolean Variables**: Prefix booleans with status indicators such as `is`, `has`, `can`, or `should` (`isValid`, `hasPermission`, `canRetry`).
- **Function Names**: Use active verb phrases for functions with side effects (`calculateTax()`, `dispatchNotification()`) and nouns/adjectives for pure accessors (`userName()`, `totalBalance`).

---

## 2. Focused Functions and Small Scopes

- **Single Responsibility**: A function should do one thing well. If a function handles input validation, database querying, business logic calculation, and email formatting, split it into discrete steps.
- **Function Size**: Aim for functions between 10 and 40 lines. When a function grows beyond 50 lines, it almost always contains hidden sub-steps that deserve their own named helper functions.
- **Minimize Parameters**: Limit function arguments to 3 or fewer. If more inputs are needed, bundle them into a typed parameter object or configuration struct.

---

## 3. Explicit Typing & Boundary Validation

- **Strong Typing**: Leverage TypeScript strict mode, Python type annotations (`typing`), Go structs, or Rust types. Avoid `any`, raw `Object`, or untyped dictionaries for domain entities.
- **Validate at Boundaries**: Treat all external inputs (HTTP bodies, query parameters, environment variables, third-party payloads, CLI arguments) as untrusted.
  - Validate and parse using schema libraries like **Zod**, **Pydantic**, or **validator**.
  - Transform untrusted raw inputs into strongly-typed domain value objects immediately at the edge.

---

## 4. Control Flow & Clarity

- **Guard Clauses & Early Returns**: Eliminate deeply nested `if/else` ladders by verifying preconditions early and returning immediately.
  ```typescript
  // Bad: Deep nesting
  function processOrder(order: Order) {
    if (order) {
      if (order.items.length > 0) {
        if (order.isPaid) {
          // core logic here
        }
      }
    }
  }

  // Good: Guard clauses
  function processOrder(order: Order) {
    if (!order || order.items.length === 0) {
      throw new InvalidOrderError("Order must contain items");
    }
    if (!order.isPaid) {
      throw new PaymentRequiredError("Order payment pending");
    }
    // Clean, unnested core logic here
  }
  ```
- **Visible Side Effects**: Keep functions pure where possible. If a function mutates state, executes disk I/O, or makes network calls, make this evident in the naming and return types.

---

## 5. Deliberate Error Handling

- **Never Swallow Exceptions**: Never write empty `catch` blocks or ignore errors silently.
  - *Bad*: `catch (err) { /* do nothing */ }`
  - *Good*: Log with context, convert to a domain error, or rethrow with enriched details.
- **Fail Fast**: Check assumptions and invariants at the beginning of operations.
- **Typed Domain Errors**: Define domain-specific error classes (e.g., `NotFoundError`, `ConflictError`, `ValidationError`) rather than throwing generic strings or untyped exceptions.

---

## 6. Dead Code & Comments Discipline

- **Remove Dead Code Immediately**: Do not keep commented-out code blocks or unreferenced functions "just in case." Version control (Git) retains all history.
- **Explain the "Why", Not the "What"**:
  - *Redundant Comment*: `// Increment i by 1` -> `i++;`
  - *Valuable Comment*: `// Stripe webhook events can arrive out of order; ensure idempotent processing via event id check.`
- **Avoid "Utils" and "Helpers" Dumping Grounds**: Do not create general `utils.ts` or `helpers.py` files with dozens of unrelated functions. Organize helpers by domain (e.g., `string_formatting.ts`, `currency_math.ts`).
