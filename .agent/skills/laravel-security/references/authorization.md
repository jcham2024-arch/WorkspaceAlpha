# Authorization

Scope: Gates, Policies, middleware authorization.
Load when: adding role checks, policies, or admin areas.

## Contents

- Gates in AuthServiceProvider (+ super-admin `before()`)
- PostPolicy registration + controller/Blade usage
- Role middleware

## Checklist

- [ ] One-off rules → Gate; model rules → Policy
- [ ] Policies registered in AuthServiceProvider
- [ ] Sensitive routes behind `role:`/`can:` middleware

## Commands

| Task | Command |
|---|---|
| Authorize in controller | `Gate::authorize('update-post', $post)` |
| Guard a route | `->middleware('can:update,post')` |

## Code

```php
// App\Providers\AuthServiceProvider
public function boot(): void
{
    Gate::define('update-post', fn (User $user, Post $post): bool =>
        $user->id === $post->user_id);
    Gate::define('publish-post', fn (User $user): bool =>
        $user->role === 'editor' || $user->role === 'admin');
    Gate::before(fn (User $user, string $ability): ?bool =>
        $user->role === 'super-admin' ? true : null);
}
```

### Policies (App\Policies\PostPolicy)

```php
class PostPolicy
{
    use HandlesAuthorization;
    public function viewAny(?User $user): bool { return true; }
    public function view(?User $user, Post $post): bool
    { return $post->is_published || ($user && $user->id === $post->user_id); }
    public function create(User $user): bool { return $user->hasVerifiedEmail(); }
    public function update(User $user, Post $post): bool { return $user->id === $post->user_id; }
    public function delete(User $user, Post $post): bool
    { return $user->id === $post->user_id && $post->created_at->diffInDays(now()) <= 30; }
    public function restore(User $user, Post $post): bool { return $user->role === 'admin'; }
    public function forceDelete(User $user, Post $post): bool { return $user->role === 'super-admin'; }
}

protected $policies = [Post::class => PostPolicy::class];

// Controller
public function show(Post $post): View
{
    $this->authorize('view', $post);
    return view('posts.show', compact('post'));
}
```

```blade
@can('update', $post) <a href="{{ route('posts.edit', $post) }}">Edit</a> @endcan
@cannot('update', $post) <span>You cannot edit this post</span> @endcannot
```

### Middleware Authorization

```php
Route::put('/posts/{post}', [PostController::class, 'update'])->middleware('can:update,post');

// app/Http/Middleware/CheckRole.php
class CheckRole
{
    public function handle(Request $request, Closure $next, string $role): mixed
    {
        if (!$request->user() || $request->user()->role !== $role) {
            abort(403, 'Unauthorized. This area requires role: ' . $role);
        }
        return $next($request);
    }
}

protected $routeMiddleware = ['role' => \App\Http\Middleware\CheckRole::class];

Route::middleware(['auth', 'role:admin'])->group(fn () =>
    Route::get('/admin', [AdminController::class, 'index']));
```

## Notes

- `Gate::before` grants super-admins everything; keep the override narrow.
