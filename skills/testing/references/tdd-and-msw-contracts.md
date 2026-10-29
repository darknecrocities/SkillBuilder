# TDD Discipline & Mock Service Worker (MSW) Contracts

---

## 1. Test-Driven Development (TDD) Red-Green-Refactor Cycle

```text
1. Red: Author a unit or contract test that asserts expected behavior and fails cleanly
2. Green: Implement minimal production code necessary to satisfy the assertion
3. Refactor: Decompose and optimize the implementation while maintaining green status
```

---

## 2. Mock Service Worker (MSW) Network Mocking

Intercept network requests at the network layer rather than patching global `fetch`:

```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

export const handlers = [
  http.get('/v1/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Jane Doe',
      role: 'admin'
    });
  }),
];

export const server = setupServer(...handlers);
```
