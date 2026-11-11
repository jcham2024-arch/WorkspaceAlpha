# Data Resolvers

Scope: data-resolvers (angular-developer).
Load when: you need the data-resolvers (angular-developer) detail described in SKILL.md.

## Contents

- Data Resolvers

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Data Resolvers

Data resolvers fetch data before a route activates, ensuring components have the necessary data upon rendering.

## Creating a Resolver

Implement the `ResolveFn` type.

```ts
export const userResolver: ResolveFn<User> = (route, state) => {
  const userService = inject(UserService);
  const id = route.paramMap.get('id')!;
  return userService.getUser(id);
};
```

## Configuring the Route

Add the resolver under the `resolve` key.

```ts
{
  path: 'user/:id',
  component: UserProfile,
  resolve: {
    user: userResolver
  }
}
```

## Accessing Resolved Data

### 1. Via `ActivatedRoute` (Traditional)

```ts
private route = inject(ActivatedRoute);
data = toSignal(this.route.data);
user = computed(() => this.data().user);
```

### 2. Via Component Inputs (Modern)

Enable `withComponentInputBinding()` in `provideRouter` to pass resolved data directly to `@Input` or `input()`.

```ts
// app.config.ts
provideRouter(routes, withComponentInputBinding());

// component.ts
user = input.required<User>();
```

## Error Handling

Navigation is blocked if a resolver fails.

- Use `withNavigationErrorHandler` for global handling.
- Use `catchError` within the resolver to return a `RedirectCommand` or fallback data.

```ts
return userService
  .get(id)
  .pipe(catchError(() => of(new RedirectCommand(router.parseUrl('/error')))));
```

## Best Practices

- **Keep it lightweight**: Fetch only critical data.
- **Provide feedback**: Listen to router events to show a global loading bar during navigation, as the UI stays on the old page until the resolver finishes.
