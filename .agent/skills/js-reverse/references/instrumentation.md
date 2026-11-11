# Instrumentation

Scope: instrumentation (js-reverse).
Load when: you need the instrumentation (js-reverse) detail described in SKILL.md.

## Contents

- Instrumentation

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# 插桩

优先轻量观察：

- XHR/Fetch 断点
- 函数文本断点
- 暂停后读调用栈与局部变量

只有在轻量观察不够时，才升级为更重的源码改写或本地插桩。
