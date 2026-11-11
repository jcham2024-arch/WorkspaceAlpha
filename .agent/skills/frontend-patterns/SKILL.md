---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 63317cd173a80a7ddb707d9cb39e9d00050f19ddae5226697b78ce64f26a73ce
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. Use when building or reviewing React or Next.js components, state, or render performance.
license: MIT
name: frontend-patterns
---
# Frontend Development Patterns
Modern frontend patterns for React, Next.js, and performant user interfaces.
## When to Activate
- Building React components (composition, props, rendering)
- Managing state (useState, useReducer, Zustand, Context)
- Implementing data fetching (SWR, React Query, server components)
- Optimizing performance (memoization, virtualization, code splitting)
- Working with forms (validation, controlled inputs, Zod schemas)
- Handling client-side routing and navigation
- Building accessible, responsive UI patterns
## Privacy and Data Boundaries
Frontend examples should use synthetic or domain-generic data. Do not collect, log, persist, or display credentials, access tokens, SSNs, health data, payment details, private emails, phone numbers, or other sensitive personal data unless the user explicitly requests a scoped implementation with appropriate validation, redaction, and access controls.
Avoid adding analytics, tracking pixels, third-party scripts, or external data sinks without explicit approval. When handling user data, prefer least-privilege APIs, client-side redaction before logging, and server-side validation for every boundary.
## Component Patterns
### Composition Over Inheritance
### Compound Components
### Render Props Pattern
## Custom Hooks Patterns
### State Management Hook
### Async Data Fetching Hook
### Debounce Hook
## State Management Patterns
### Context + Reducer Pattern
## Performance Optimization
### Memoization
### Code Splitting & Lazy Loading
### Virtualization for Long Lists
## Form Handling Patterns
### Controlled Form with Validation
## Error Boundary Pattern
## Animation Patterns
### Framer Motion Animations
## Accessibility Patterns
### Keyboard Navigation
### Focus Management
**Remember**: Modern frontend patterns enable maintainable, performant user interfaces. Choose patterns that fit your project complexity.