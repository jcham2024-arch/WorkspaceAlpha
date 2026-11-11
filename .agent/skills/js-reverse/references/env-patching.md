# Env Patching

Scope: env-patching (js-reverse).
Load when: you need the env-patching (js-reverse) detail described in SKILL.md.

## Contents

- Env Patching

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# 补环境规则

- 只补页面证据已经证明需要的对象
- 一次补一个最小因果单元
- 先补值，再补函数壳，再补返回对象契约
- 每次补丁都要重新执行并记录 first divergence 是否前移
