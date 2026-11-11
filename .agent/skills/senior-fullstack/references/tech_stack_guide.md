# Tech Stack Guide

Scope: tech_stack_guide (senior-fullstack).
Load when: you need the tech_stack_guide (senior-fullstack) detail described in SKILL.md.

## Contents

- Tech Stack Guide

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Stack inspection checklist

Read the project's dependency manifests, lockfiles, entrypoints and build configuration. Record the frontend framework, backend runtime, persistence layer, authentication boundary and deployment target without replacing them merely to match an example stack.

Identify the commands the project actually declares for type checking, tests, linting and build. Check installed versions before selecting an API or adding a dependency. Preserve environment files and keep credentials out of logs and source control.

For a proposed feature, state which layers must change and which contract each layer owns. Prefer an existing component, service or repository abstraction when its behavior fits. Record unsupported environments and missing provider access as limitations.
