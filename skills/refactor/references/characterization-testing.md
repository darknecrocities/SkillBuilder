# Characterization (Golden Master) Testing Manual

> **Objective**: Pin down the exact current behavior of untested legacy modules *before* changing a single line during a refactor, ensuring zero accidental behavioral drift.

---

## 1. When Characterization Testing Is Mandatory
- Legacy file exceeds `350` lines and has `< 50%` test coverage.
- Replacing raw SQL/callback spaghetti with clean repository/async boundaries.
- Migrating a core algorithm, parser, search indexer, or pricing calculator.

---

## 2. The 5-Step Golden Master Protocol

1. **Freeze Production Code**: Do not rename functions or tidy formatting yet (`Two-Hat Rule`).
2. **Capture Input/Output Matrix**: Build deterministic test cases covering normal inputs, boundary values (`0`, `""`, `null`, max length), unicode/accents, and existing error codes — even if current behavior includes quirky rounding or edge behavior.
3. **Verify Green Baseline**: Run the characterization suite against untouched code and confirm `100%` pass.
4. **Execute Structural Refactor**: Decompose or apply Strangler Fig behind the same public contract (`<= 40` lines/func, `<= 3` nesting, `<= 500` lines/file).
5. **Prove Parity & Upgrade**: Re-run the Golden Master suite (must remain `100%` green), then add fine-grained unit tests for each newly extracted helper.

---

## 3. Example Parity Harness (TypeScript / Python)

```typescript
import { describe, expect, it } from "vitest";
import { legacyCalculateQuote } from "./legacyQuote";

const GOLDEN_FIXTURES = [
  { input: { cents: 0, tier: "standard" }, expected: { total: 0, fee: 0 } },
  { input: { cents: 12500, tier: "pro" }, expected: { total: 12875, fee: 375 } },
  { input: { cents: -1, tier: "standard" }, throws: "INVALID_AMOUNT" },
];

describe("Quote characterization baseline", () => {
  it.each(GOLDEN_FIXTURES)("matches golden fixture %#", ({ input, expected, throws }) => {
    if (throws) expect(() => legacyCalculateQuote(input)).toThrow(throws);
    else expect(legacyCalculateQuote(input)).toEqual(expected);
  });
});
```
