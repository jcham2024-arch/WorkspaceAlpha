# Common Workflows

Scope: common-workflows (github-actions-templates).
Load when: you need the common-workflows (github-actions-templates) detail described in SKILL.md.

## Contents

- Common Workflows

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Choosing a workflow boundary

## Inputs

Inspect the target repository scripts, runtime support, protected branches and artifact publication policy.

## Procedure and verification

Use unprivileged pull-request jobs for tests and builds. Put publication in a separate trusted path with its own credentials and explicit protected environment where required. Bind the artifact to the tested commit and reject missing or mismatched provenance. Check that a failing test prevents the publishing job from running.

## Limitations

A template must be adapted to actual commands. Do not give fork code production secrets, persistent runner access or a write token. See the inline workflow patterns in the skill for the starting structure.
