# Features Vs Dockerfile

Scope: features-vs-dockerfile (devcontainer-setup).
Load when: you need the features-vs-dockerfile (devcontainer-setup) detail described in SKILL.md.

## Contents

- Features Vs Dockerfile

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
> Modified 2026-10-23: qualified Python installation claim. CC-BY-SA-4.0 retained under the bundled upstream notice.

# Features vs Dockerfile

## Use devcontainer features when:

- Installing standard development tools (GitHub CLI, languages, etc.)
- The feature does what you need out of the box
- You want automatic updates with feature version bumps

## Use Dockerfile when:

- Installing specific versions of tools
- Custom configuration is needed
- Combining multiple tools in optimized layers
- The feature doesn't exist or is poorly maintained

## Example: Python

For Python, we use Dockerfile + uv instead of the Python feature because:

1. uv can download compatible prebuilt Python distributions when available; some platforms require another installation path
2. We get uv for dependency management
3. More control over the installation
