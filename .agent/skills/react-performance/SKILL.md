---
tier: experimental
last_reviewed: 2026-11-10
content_hash: ab491855fb27f710f5d0948b9745018b0080610817efe08edf582ad53db6e216
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: "React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-labs/agent-skills). Organizes 70+ rules across 8 priority categories — waterfalls, bundle size, server-side, client fetching, re-render, rendering, JS micro-perf, advanced. Use when writing, reviewing, or refactoring React/Next.js code for performance."
name: react-performance
origin: ECC
---
# React Performance
Performance optimization patterns for React 18/19 and Next.js, adapted from [Vercel Labs `react-best-practices`](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) (MIT, v1.0.0). This skill organizes rules by priority and provides decision-tree guidance for active code review and refactoring.
## When to Activate
- Writing or reviewing React/Next.js code for performance
- Diagnosing slow page loads, slow interactions, or high CPU on the client
- Auditing bundle size or Lighthouse Core Web Vitals regressions
- Removing waterfalls in Server Components / API routes
- Reducing client-side re-renders
- Optimizing long lists, animations, or hydration
- Auditing optimization choices in PRs touching `app/`, `pages/`, `components/`, or data layers
## Priority Index
| Priority | Category | Prefix | When it matters |
|---|---|---|---|
| 1 — CRITICAL | Eliminating Waterfalls | `async-` | Anytime `await` is followed by independent `await` |
| 2 — CRITICAL | Bundle Size Optimization | `bundle-` | First-load JS, route-level imports, third-party libs |
| 3 — HIGH | Server-Side Performance | `server-` | RSC, Server Actions, API routes, SSR |
| 4 — MEDIUM-HIGH | Client-Side Data Fetching | `client-` | SWR / TanStack Query / raw `fetch` in hooks |
| 5 — MEDIUM | Re-render Optimization | `rerender-` | High-frequency state updates, parent-child fan-out |
| 6 — MEDIUM | Rendering Performance | `rendering-` | Long lists, animations, hydration |
| 7 — LOW-MEDIUM | JavaScript Performance | `js-` | Hot loops, frequent allocations |
| 8 — LOW | Advanced Patterns | `advanced-` | Effect-event integration, stable refs |
## 1. Eliminating Waterfalls (CRITICAL)
> "Waterfalls are the #1 performance killer" — every sequential `await` adds full network latency.
### Cheap conditions before await
Check sync conditions (props, env, hardcoded flags) before awaiting remote data.
### Defer awaits until used
Move `await` into the branch that uses it.
### Promise.all for independent work
### Partial dependencies — start early, await late
### Suspense for streaming
Push `<Suspense>` boundaries close to the data so the page paints what it can while slower sub-trees stream in. The trade-off: layout shift when content arrives — reserve space (skeleton or `min-height`).
### Server Components: parallel through composition
## 2. Bundle Size Optimization (CRITICAL)
### Direct imports, not barrels
Barrel `index.ts` files force the bundler to walk the entire module graph even when tree-shaking removes most of it. Direct imports save 200-800ms of first-load JS in many real-world apps.
Next.js 13.5+ has [Optimize Package Imports](https://nextjs.org/docs/app/api-reference/next-config-js/optimizePackageImports) that automates this for listed packages — use it; manual direct imports still required for non-listed libs.
### Statically analyzable paths
### Dynamic imports for heavy components
### Defer third-party scripts
Load analytics, logging, support widgets AFTER hydration. Use `next/script` with `strategy="afterInteractive"` (default) or `"lazyOnload"`.
### Conditional module loading
### Preload on hover/focus
Trigger `<link rel="preload">` or `import()` on hover so the bundle is in cache by the time the user clicks.
## 3. Server-Side Performance (HIGH)
### Authenticate Server Actions like API routes
Every `"use server"` function is a public endpoint. Authenticate AND authorize inside the action — never rely on the calling Client Component's gating.
### `React.cache()` for per-request deduplication
`React.cache` dedupes within a single request. Calling `getUser("1")` from three Server Components in the same render = one DB query.
### LRU cache for cross-request data
For data that does NOT change per request (config, lookup tables), cache outside React with an LRU cache or `unstable_cache`.
### Avoid duplicate serialization in RSC props
When a Server Component renders the same data into multiple Client Components, the data is serialized once per consumer. Lift the Client Component up and pass children.
### Hoist static I/O to module scope
### No mutable module-level state in RSC/SSR
Module state on the server is shared across all requests — a race condition between users. Use request-scoped storage (`headers()`, `cookies()`, async context) instead.
### Minimize data passed to Client Components
Only serialize what the Client needs. Strip fields, paginate, project columns at the DB layer.
### Parallelize nested fetches with Promise.all per item
### Use `after()` for non-blocking work
Next.js 15 `after()` runs work after the response is sent — logging, cache warming, analytics.
## 4. Client-Side Data Fetching (MEDIUM-HIGH)
### SWR / TanStack Query for deduplication
Multiple components calling `useUser(id)` should share one network request and one cache entry. Use SWR or TanStack Query — never roll your own `useEffect` + `fetch` for shared data.
### Deduplicate global event listeners
### Passive listeners for scroll
Improves scrolling smoothness; the listener cannot `preventDefault()`.
### localStorage: version + minimize
- Always store a `version` field; bump on schema change and migrate or discard old data
- Keep payloads small — `localStorage` is synchronous and blocks main thread
## 5. Re-render Optimization (MEDIUM)
### Don't subscribe to state used only in callbacks
### Extract expensive work into memoized components
### Hoist default non-primitive props
### Primitive dependencies in effects
### Subscribe to derived booleans, not raw values
### Derive during render, never via `useEffect`
### Functional `setState` for stable callbacks
### Lazy state initializer for expensive values
### Avoid memo for simple primitives
`useMemo(() => x + 1, [x])` is overhead. Memo earns its keep on object identity and expensive computation.
### Split hooks with independent deps
### Move interaction logic into event handlers
Event handlers run only on the user action — `useEffect` re-runs whenever deps change.
### `startTransition` for non-urgent updates
### `useDeferredValue` for expensive renders
### `useRef` for transient frequent values
For values that change often but should not trigger re-render (timestamps, last-key, accumulators).
### Don't define components inside components
Each render makes a new `Inner` type, defeating reconciliation and unmounting children.
## 6. Rendering Performance (MEDIUM)
### Animate the wrapper, not the SVG
Transforming a `<div>` wrapper around an SVG is GPU-accelerated; transforming the SVG itself triggers paint.
### `content-visibility: auto` for long lists
Browser skips offscreen rendering — major win for lists with hundreds of rows.
### Hoist static JSX
### SVG: reduce coordinate precision
`d="M10.123456,20.654321"` → `d="M10.12,20.65"`. Each digit costs bytes; the visual difference is sub-pixel.
### Hydration no-flicker via inline script
For values needed before hydration (theme, locale), inline a `<script>` that sets `document.documentElement.dataset.*` before React mounts.
### Suppress expected hydration mismatches narrowly
Use ONLY for known-divergent leaf nodes — never on a tree containing other children.
### `<Activity>` for show/hide instead of mount/unmount
React 19 `<Activity mode="visible|hidden">` keeps tree state and effects mounted but hides — cheaper than unmount/remount for tabs and accordions.
### Ternary over `&&` for conditional render
### `useTransition` for loading states
Pair `startTransition` with the action; React shows the previous UI as `isPending` while the next state computes.
### React DOM resource hints
### `defer` / `async` on `<script>` tags
`defer` for ordered execution after DOMContentLoaded; `async` for fire-and-forget.
## 7. JavaScript Performance (LOW-MEDIUM)
- **Batch DOM/CSS changes** — apply via class swap or `cssText`, not property-by-property
- **`Map` for repeated lookups** — `O(1)` vs `O(n)` linear scan
- **Cache property access in loops** — `const len = arr.length`
- **Memoize pure functions** — module-level `Map<key, result>`
- **Cache `localStorage` reads** — sync API; one read per render
- **Combine `filter().map()` into one pass** — `flatMap` or single `for`
- **Check array length first** before expensive comparisons
- **Early return** from functions
- **Hoist RegExp** out of loops — compilation is not free
- **Loop for min/max** instead of `sort()` — `O(n)` vs `O(n log n)`
- **`Set`/`Map` for membership** — `O(1)` vs `Array.includes` `O(n)`
- **`toSorted()` over mutation** when immutability matters
- **`flatMap` to map and filter in one pass**
- **`requestIdleCallback`** for non-critical work
## 8. Advanced Patterns (LOW)
### `useEffectEvent` deps
Values from `useEffectEvent` are stable — do NOT add them to effect deps.
### Event handler refs
For stable callbacks passed to memoized children:
### Init once per app load
For module-level singletons (telemetry, logger), guard with a module-scope flag — not `useEffect`.
### `useLatest` for stable callback refs
## Automated Tools
Many of these rules are now automated:
- **Next.js 13.5+ Optimize Package Imports** — barrel import optimization
- **React Compiler** (RFC, in canary) — auto-memoization
- **Turbopack** — faster builds, better tree-shaking
- **Bundle Analyzer** (`@next/bundle-analyzer`) — visualize first-load JS
When the project ships React Compiler, demote `rerender-*` manual memoization rules to "review-only" — the compiler handles them. Manual `useMemo`/`useCallback` becomes unnecessary noise.
## Lighthouse / Web Vitals Mapping
| Metric | Most relevant categories |
|---|---|
| **LCP** (Largest Contentful Paint) | Waterfalls, Bundle Size, Resource Hints |
| **INP** (Interaction to Next Paint) | Re-render, Rendering, JavaScript |
| **CLS** (Cumulative Layout Shift) | Rendering (Suspense placement, image dimensions) |
| **TBT** (Total Blocking Time) | Bundle Size, JavaScript, Defer Third-Party |
| **FID** (legacy) | Bundle Size, Hydration |
## Related
- Skills: [react-patterns](../react-patterns/SKILL.md), [react-testing](../react-testing/SKILL.md), [frontend-patterns](../frontend-patterns/SKILL.md), [accessibility](../accessibility/SKILL.md), [nextjs-turbopack](../nextjs-turbopack/SKILL.md)
- Rules: [rules/react/](../../rules/react/)
- Agents: `react-reviewer` enforces these rules in code review; `react-build-resolver` handles related build failures
- Commands: `/react-review`, `/react-build`, `/react-test`
## Attribution
Adapted from Vercel Labs `react-best-practices` skill (MIT License, copyright Vercel Engineering, v1.0.0 January 2026). Source: [https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices).
This skill restructures and adapts the original 70-rule catalog into a single navigable reference. For the full original ruleset with extended examples, see the upstream repository.