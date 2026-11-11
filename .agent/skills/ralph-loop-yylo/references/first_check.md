# First Check

Scope: first_check (ralph-loop-yylo).
Load when: you need the first_check (ralph-loop-yylo) detail described in SKILL.md.

## Contents

- First Check

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
### Check once

Before editing, verify the task worktree, clean starting state, and frozen admitted
path scope. Inspect ignore files only when the assigned task requires an ignore
rule or the task's validation would otherwise produce untracked generated output.

Modify an ignore file only when all of the following are true:

- the change is necessary for the assigned task;
- the exact file is included in the task's admitted paths;
- existing project conventions support the rule; and
- the change is included in focused validation and the task commit.

Do not create or expand `.gitignore`, `.dockerignore`, `.eslintignore`,
`.prettierignore`, `.npmignore`, `.terraformignore`, or `.helmignore` merely
because a related tool is present. If a useful ignore-file change is outside the
assigned scope, record a bounded related follow-up and continue only when the
current task remains valid without it.
