---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 76fb3462a2916d605215e9d49b18399fc12a2741b7487b4390ad4c4effe96c78
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Create Zustand stores following established patterns with proper TypeScript types and middleware.
name: zustand-store-ts
risk: critical
source: community
---
# Zustand Store
Create Zustand stores following established patterns with proper TypeScript types and middleware.
## Quick Start
No assets/template.ts is bundled. Adapt the inline examples to the installed Zustand version and actual project types; these are fragments, not a complete application.
## Use subscribeWithSelector for selector subscriptions
```typescript
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
export const useMyStore = create<MyStore>()(
  subscribeWithSelector((set, get) => ({
    // state and actions
  }))
);
```
## Separate State and Actions
```typescript
export interface MyState {
  items: Item[];
  isLoading: boolean;
}
export interface MyActions {
  addItem: (item: Item) => void;
  loadItems: () => Promise<void>;
}
export type MyStore = MyState & MyActions;
```
## Use Individual Selectors
```typescript
// Good - only re-renders when `items` changes
const items = useMyStore((state) => state.items);
// Avoid - re-renders on any state change
const { items, isLoading } = useMyStore();
```
## Subscribe Outside React
```typescript
useMyStore.subscribe(
  (state) => state.selectedId,
  (selectedId) => console.log('Selected:', selectedId)
);
```
## Integration Steps
1. Create store in `src/frontend/src/store/`
2. Export from `src/frontend/src/store/index.ts`
3. Add tests in `src/frontend/src/store/*.test.ts`
## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.