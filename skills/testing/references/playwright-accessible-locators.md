# Playwright Accessible Locators & E2E Testing Discipline

Modern E2E tests should interact with the DOM the way users and assistive technology do.

---

## 1. Locator Priority Hierarchy

Priority | Locator Pattern | Avoid
:--- | :--- | :---
1 (Best) | `page.getByRole('button', { name: 'Submit' })` | CSS class selectors (`page.locator('.btn-primary')`)
2 | `page.getByLabel('Email address')` | Raw XPath (`page.locator('//div[3]/input')`)
3 | `page.getByPlaceholder('Search products...')` | Unstable tag paths (`page.locator('div > span > input')`)
4 | `page.getByText('Order Confirmation')` | Brittle ID attributes
5 (Fallback) | `page.getByTestId('checkout-total')` | Only when semantic query cannot be expressed

---

## 2. Test Flakiness Prevention

- Use web-first assertions: `await expect(button).toBeVisible()` automatically retries until timeout.
- Never use arbitrary `await page.waitForTimeout(3000)`. Wait on explicit network idle or locator state.
