# Fallbacks

Scope: fallbacks (js-reverse).
Load when: you need the fallbacks (js-reverse) detail described in SKILL.md.

## Contents

- Fallbacks

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# 回退策略

当当前路径无进展时按顺序回退：

1. 从断点回退到请求观察
2. 从源码猜测回退到运行时证据
3. 从 Node 补环境回退到页面取证
4. 从深度去混淆回退到最小可复现链路
