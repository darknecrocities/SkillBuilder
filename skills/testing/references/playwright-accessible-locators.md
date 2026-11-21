# Playwright Accessible Locators & Flake-Free E2E Manual

> **Objective**: Write resilient E2E tests that verify real user-observable behavior (`Test Behavior, Not Implementation`) with zero arbitrary sleeps or brittle CSS selectors.

---

## 1. Accessible Locator Priority Hierarchy

Use locators in strict order of resilience and accessibility alignment:

| Priority | Playwright Locator | Why It Wins |
| :---: | :--- | :--- |
| **1 (Best)** | `page.getByRole("button", { name: "Save Changes" })` | Proves both visual control and accessible ARIA role/name work for screen readers |
| **2** | `page.getByLabel("Email Address")` | Verifies `<label htmlFor>` association |
| **3** | `page.getByPlaceholder(...)` / `page.getByText(...)` | Resilient to Tailwind class or DOM wrapper refactors |
| **4 (Last Resort)** | `page.getByTestId("telemetry-chart")` | Use only for non-text canvas/SVG widgets lacking semantic roles |
| **BANNED** | `page.locator("div.flex > button.bg-zinc-900:nth-child(2)")` | Breaks on every styling tweak and hides missing a11y labels |

---

## 2. Web-First Auto-Waiting Assertions (Zero `waitForTimeout`)

```typescript
// BAD: Flaky under CI load and wastes test time
await page.waitForTimeout(2000);
expect(await page.locator(".toast").isVisible()).toBe(true);

// GOOD: Auto-retries deterministically until assertion holds or timeout fires
await expect(page.getByRole("status")).toContainText("Project saved");
await expect(page).toHaveURL(/\/projects\/[a-z0-9-]+$/);
```

- **Responsive Viewport Matrix**: Run critical E2E smoke assertions at both Mobile (`375x812`) and Desktop (`1280x800`) to catch horizontal overflow (`scrollWidth > innerWidth`) and clipped touch targets automatically.
