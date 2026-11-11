# Extension Analysis

Scope: extension-analysis (browser-extension-reverse).
Load when: you need the extension-analysis (browser-extension-reverse) detail described in SKILL.md.

## Contents

- Extension Analysis

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# 扩展分析要点

| 字段 | 风险信号 |
|------|----------|
| host_permissions `<all_urls>` | 可读写任意站 |
| webRequestBlocking | 中间人式改写 |
| nativeMessaging | 出浏览器到本机 |
| externally_connectable | 网页驱动扩展 |

MV3：关注 service_worker 生命周期与 declarativeNetRequest。