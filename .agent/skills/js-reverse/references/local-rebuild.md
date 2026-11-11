# Local Rebuild

Scope: local-rebuild (js-reverse).
Load when: you need the local-rebuild (js-reverse) detail described in SKILL.md.

## Contents

- Local Rebuild

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# 本地复现

页面侧确认以下内容后再回到 Node：

- 真实入口函数
- 调用顺序
- 参数来源
- 依赖的浏览器对象
- 是否依赖时间、随机数、storage、cookie、UA、canvas、crypto

先最小复现，再逐步补环境，不要一次性模拟整浏览器。
