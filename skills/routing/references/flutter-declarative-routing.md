# Flutter Declarative Routing (`go_router`) & Deep-Link Auth Gates

> **Objective**: Enforce type-safe declarative navigation, reactive auth redirects, stateful shell tabs, and cold-start deep link handling in Flutter applications.

---

## 1. Typed `GoRouter` Configuration with `StatefulShellRoute`

```dart
final appRouterProvider = GoRouter(
  initialLocation: '/home',
  redirect: (context, state) {
    final loggedIn = authState.isAuthenticated;
    final goingToLogin = state.matchedLocation == '/login';
    if (!loggedIn && !goingToLogin) {
      final from = Uri.encodeComponent(state.uri.toString());
      return '/login?redirect=$from';
    }
    if (loggedIn && goingToLogin) {
      return state.uri.queryParameters['redirect'] ?? '/home';
    }
    return null;
  },
  routes: [
    GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
    StatefulShellRoute.indexedStack(
      builder: (context, state, shell) => AppNavScaffold(navigationShell: shell),
      branches: [
        StatefulShellBranch(routes: [
          GoRoute(path: '/home', builder: (_, __) => const HomeScreen()),
        ]),
        StatefulShellBranch(routes: [
          GoRoute(
            path: '/items/:id',
            builder: (_, state) => ItemDetailScreen(id: state.pathParameters['id']!),
          ),
        ]),
      ],
    ),
  ],
);
```

---

## 2. Deep-Link & Navigation Safety Rules

1. **Preserve Tab Scroll & State**: Always use `StatefulShellRoute.indexedStack` for bottom navigation tabs instead of re-building tab roots on `context.go()`.
2. **Validate Path/Query Params**: Never force-unwrap `state.pathParameters` blindly on malformed deep links; validate IDs and route unknown/expired IDs to a dedicated `errorBuilder` screen.
3. **Never Redirect Loops**: Only return non-null from `redirect` when the destination differs from `state.matchedLocation`, and pass `refreshListenable` from the auth notifier so router redirects fire reactively on token expiry.
4. **Preserve Cold-Start Deep Links**: Encode the intended deep-link URI in `?redirect=...` during auth interruption so login returns the user directly to the requested screen.
