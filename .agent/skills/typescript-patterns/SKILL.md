---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 9385fdec88c18c81d1cb4e120b8f4334eb7278d518b8437b04ba6a94c512f3d6
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: TypeScript patterns for strict, type-safe, maintainable code in modern TypeScript and JavaScript applications. Covers strict compiler configuration, type design, narrowing, discriminated unions, generics, async and error handling, module boundaries, dependency hygiene, and type-level testing. Use when writing or reviewing TypeScript or JavaScript code.
name: typescript-patterns
origin: ECC
---
# TypeScript Development Patterns
TypeScript patterns and best practices for building robust, type-safe, and maintainable applications. The compiler is most useful when it can prove your program's shape, so the guiding principle here is: push the type system to do real work instead of fighting it. This skill is the "how." For the "what" and "when" (the decisions about which pattern to reach for), see the TypeScript rules — `rules/typescript/coding-style.md` and `rules/typescript/patterns.md` in this repository, installed as `rules/ecc/typescript/coding-style.md` and `rules/ecc/typescript/patterns.md`.
## When to Activate
- Writing new TypeScript or JavaScript code
- Reviewing a PR that touches `.ts` or `.tsx` files
- Refactoring existing TypeScript to remove `any`, tighten types, or add strictness
- Designing types, generics, or module boundaries for a new feature
- Setting up a new TypeScript project or upgrading `tsconfig.json`
- Debugging type errors that cascade through a codebase (usually a design problem, not an annotation problem)
## Core Principles
### 1. Strict Mode Is the Baseline
`strict: true` (which enables `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, and the rest) is not optional in a healthy codebase. If a codebase cannot compile under strict, that is a migration task, not an excuse to leave the flag off.
`noUncheckedIndexedAccess` makes array and record access possibly-undefined, which surfaces a whole class of runtime crashes at compile time. If it produces too much noise, this is the pattern to add, not the flag to remove:
### 2. `any` Is a Bug, Not a Tool
`any` disables the type system exactly where a bug is most likely to hide: at the boundary with untrusted or dynamic data. Prefer `unknown` and narrow it. When you truly need a fallback, prefer an explicit loosening with a comment over a silent `any`.
### 3. Public APIs Get Explicit Types, Locals Get Inference
TypeScript infers local variables well. Exporting functions whose parameter and return types are implicit leaks inference decisions into every consumer and makes intent unreadable.
## Type Design
### Interfaces vs. Type Aliases
`interface` for object shapes that may be extended or implemented; `type` for unions, intersections, tuples, mapped types, and utility types. Prefer string-literal unions over `enum` unless you need runtime value enumeration or interop with code that requires it.
### Discriminated Unions Are the Default State Machine
When a value can be in multiple shapes, model it as a discriminated union with a literal `type`/`kind` field. Exhaustive checking then becomes a free compiler feature: never a runtime fallback, always a compile error on a missing branch.
### Brands and Nominal Safety Where Structure Is Not Enough
Structural typing cannot tell `CustomerId` from `string`. When an ID or unit must not be confused with another, add a brand (a phantom field with a unique symbol key).
Keep brands internal to a boundary module; never expose the cast helper far from the validation that justifies it.
### Generics Model Caller-Dependent Types
If a value's type depends on what the caller supplies, make it generic rather than flattening to `any` or `unknown` and hand-casting at call sites.
Constrain generics so the contract is discoverable: prefer `T extends SomeShape` over free-floating `T` when a shape assumption exists.
### Options Objects over Positional Parameters
Functions with more than a couple of knobs should take a single options object. It makes call sites self-documenting and lets new knobs be added without positional churn.
## Narrowing and Runtime Safety
### Validate at the Boundary, Trust Inside
Untrusted data enters at I/O boundaries: API handlers, message consumers, file loaders. Parse and validate once with a schema, then carry the refined type through the domain. This is where a validation library (for example, Zod) earns its keep — the schema is both the runtime check and the compile-time type.
### Type Predicates and Assertion Functions
Prefer type predicates and assertion functions over unchecked casts when guarding shapes. The guard documents the invariant and the compiler checks its usage.
To fail loudly on a malformed value instead of returning a boolean, use an assertion signature:
### Readonly by Default
Mark array and object parameters `readonly`/`ReadonlyArray` when the function does not mutate them. It prevents accidental mutation and signals intent at the signature. (Per the coding-style rules, prefer the spread operator for immutable updates.)
Runtime immutability (for example, `Object.freeze`) is for hot application boundaries; `readonly` in type positions is the everyday guard.
## Error Handling
### Fail at the Boundary, Handle at the Edge
The `try/catch` belongs where the caller can act on failure — not wrapped around every internal call in a stack of swallowed errors. Use async/await with `try/catch` and narrow `unknown` errors safely (per the coding-style rules).
This endpoint example accepts non-empty IDs made of ASCII letters, digits, underscores, and hyphens, such as `u_1`. Validate that contract before constructing the path or making a request. Adapt the identifier grammar to the real API.
### Result Types for Expected Failures
For expected business failures (validation, not-found, conflict), a discriminated `Result` union makes failure explicit in the type instead of hiding it in the exception flow.
Reserve exceptions for the unexpected. Expected outcomes belong in the return type.
### Preserve Error Context
Use `new Error(message, { cause })` (available since ES2022) so the original failure chain survives rewrapping. Never stringify errors into a message and lose the cause.
## Async Patterns
### Prefer `Promise.allSettled` for Independent Fan-Out
When results are independent and one failure must not drop the others, use `Promise.allSettled` and handle the per-promise outcomes.
Use `Promise.all` when you want fail-fast semantics — genuinely all-or-nothing work.
### Avoid Unbounded Concurrency
Fanning out hundreds of promises at once overwhelms connections and event loop. Bound the concurrency with a small pool.
### Timeouts and Cancellation
Always thread `AbortSignal` through long-running or outbound work so callers can cancel; pair it with `Promise.race` for hard timeouts where the underlying operation cannot be aborted.
## Null and Undefined Discipline
Prefer a discriminated approach over mixing sentinel values. Where "not found" or "absent" is a legitimate state, use `T | undefined` and check explicitly; avoid deeply nesting `?.` chains followed by silent fallbacks that hide bugs.
Avoid truthiness checks that silently accept wrong types (`if (result)` when `result` may be `0` or `''`). Compare against `undefined`/`null` explicitly.
## Module Boundaries and Exports
### Small, Named Modules
Expose a deliberate surface at each module's boundary. Prefer explicit named exports over default exports, and re-export at the public edge so consumers import from the module that owns the type — not from deep internals that can be refactored.
### Avoid Barrel Bloat and Circular Imports
Do not create barrels that import everything at module load (they defeat tree-shaking and grow cold-start). Import concrete paths. Circular imports signal a submission boundary that should fold upward; the type that both sides need belongs in a shared module neither imports.
### Split by Dependency Direction
Let the type graph point the way: types that cross boundaries go in a contract module; implementations import the contract; nothing imports implementations from contracts. In a node/backend codebase that means roughly: `domain` (pure types and rules) → `application` (use cases) → `infrastructure` (adapters), with dependencies pointing only inward.
## Dependencies and Build
### Diagnose, Then Add Dependencies
Prefer built-in `Array`, `Map`, `Promise`, and `Intl` over pulling in utilities for every small operation. A tiny inline function beats a dependency that must be upgraded, audited, and kept compatible. (The Go idiom "a little copying is better than a little dependency" applies to TypeScript too.)
### Runtime Validation, Not Type-of-Trust
Schemas that validate at runtime (Zod, validators, or hand-written guards) are the bridge between untrusted data and compile-time types. Library approaches differ (Zod and other schema-first libraries derive the type from the schema; validators in some ecosystem patterns are type-first with the runtime check derived). Pick one model and be consistent across the codebase.
### Keep the Compiler Incremental and Fast
Large codebases benefit from `composite: true` with project references, an `incremental` build cache, and `moduleResolution: bundler` where the bundler supports it. Slow type-checking is a workflow problem that pushes developers off the type system — invest in narrowing the checked surface over relaxing it.
## Performance
### Types Are Free, Structures Are Not
Type-level gymnastics (mapped types, conditional types, template literal types) cost nothing at runtime but can cost a lot of developer clarity. Keep complex type machinery inside boundary modules; do not export type circus acts as the public API.
### Avoid Unnecessary Object Renaming
Copying and spreading large nested objects repeatedly has real cost in hot paths. Prefer immutable updates with spread at the point of change, but avoid defensive re-copying of unchanged structures (for example, in render paths or per-message handlers).
### Memoize Idempotent Computation
Pure, expensive derivations belong behind a cache if they repeat with the same inputs. Use `Map`-based caches with explicit lifetime instead of ad-hoc global caches that never clear.
## Type-Level Testing
### Assert the Types, Not Just the Runtime
Behavior tests prove runtime behavior; dedicated type tests lock in the public API contract. A type that silently loosens is a regression.
### Use `satisfies` to Preserve Intent
`satisfies` checks a value against a shape without widening it to that shape — the ideal way to keep literal types while still validating structure.
## TypeScript Tooling Integration
### Essential Commands
### Recommended Linter Baseline
The `typescript-eslint` recommended-type-checked ruleset is the practical default: it promotes `no-unsafe-assignment`, `no-unsafe-member-access`, `no-unsafe-argument`, and `no-unsafe-call` from style noise to compiler-like guarantees. Keep the type-aware config; if it is slow, that is a project-structure signal, not a reason to disable it.
## Anti-Patterns to Avoid
- **`any` as a speed hack** — it converts the compiler's proof into a runtime guess. Reach for `unknown` + narrowing instead.
- **`as` casts that lie** — a cast that bypasses a check you did not actually perform is where null-pointer and shape bugs are born. Validate, then cast, and keep the cast inside the module that validates.
- **Deeply nested callbacks / promise chains** — prefer async/await; flat code is narrowable code.
- **`enum` coercion bugs** — string-literal unions give you the same safety without runtime artifacts or reverse-mapping footguns.
- **Giant god types** — a single interface that models several unrelated shapes should be a discriminated union or several interfaces.
- **Optional-only option objects** — `allOptional` config types silently swallow typos at the call site; prefer required fields for the ones the function genuinely depends on.
- **Silent catch** — `catch {}` or `catch (e) { /* nothing */ }` hides failures the caller assumed were handled.
- **Mixing sync and async error paths** — an `async` function always surfaces throws as rejections, even before the first `await`. Only a non-`async` function returning a promise can throw synchronously (before returning it), forcing callers to handle two error shapes. Prefer `async` throughout so every failure is a rejection:
**Remember**: the type system is a proof tool, not a paperwork burden. When a type error resists a reasonable annotation, the design — not the compiler — is usually the thing to change. Prefer boring, explicit, well-scoped TypeScript over clever type engines.
## Related Skills
- `nestjs-patterns` — NestJS architecture patterns for TypeScript backends (modules, controllers, providers, DTO validation)
- `frontend-patterns` — React and Next.js component and state patterns
- TypeScript rules (`rules/typescript/`, installed as `rules/ecc/typescript/`) — the "what" and "when" this skill implements as the "how"
- `prisma-patterns` — database access patterns used in TypeScript applications