# Flutter Declarative Routing with GoRouter

---

## 1. GoRouter Setup Standards

```dart
final goRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailsScreen(id: id);
          },
        ),
      ],
    ),
  ],
  redirect: (context, state) {
    final isLoggedIn = authService.isAuthenticated;
    final isLoggingIn = state.matchedLocation == '/login';
    if (!isLoggedIn) return isLoggingIn ? null : '/login';
    if (isLoggingIn) return '/';
    return null;
  },
);
```

### Key Practices:
- Always use `context.go()` for declarative route transitions.
- Handle deep linking and browser URL synchronization on Flutter Web automatically.
