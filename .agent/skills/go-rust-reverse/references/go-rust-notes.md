# Go Rust Notes

Scope: go-rust-notes (go-rust-reverse).
Load when: you need the go-rust-notes (go-rust-reverse) detail described in SKILL.md.

## Contents

- Go Rust Notes

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Go/Rust 提示

Go：先找 `runtime.main` / `main.main`，用 pclntab 恢复。  
Rust：先收集 `src/` 路径字符串与 `Option`/`Result` 处理块。  
两者均：优先字符串驱动，避免在运行时库中迷路。