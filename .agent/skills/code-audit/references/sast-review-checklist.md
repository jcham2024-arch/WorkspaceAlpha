# Sast Review Checklist

Scope: sast-review-checklist (code-audit).
Load when: you need the sast-review-checklist (code-audit) detail described in SKILL.md.

## Contents

- Sast Review Checklist

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# 代码审计清单（精简）

- [ ] 所有外部输入入口列表
- [ ] 鉴权/鉴权中间件覆盖
- [ ] 多租户 ID 是否绑定会话
- [ ] 反序列化 / pickle / YAML load
- [ ] SSRF 出网与协议限制
- [ ] 密钥与 token 存储
- [ ] 文件上传路径与类型
- [ ] 危险 exec/system/Runtime