# Ad Attack Paths

Scope: ad-attack-paths (windows-ad).
Load when: you need the ad-attack-paths (windows-ad) detail described in SKILL.md.

## Contents

- Ad Attack Paths

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# AD 攻击路径速查

| 路径 | 前提 | 工具线索 |
|------|------|----------|
| Kerberoast | SPN 账户 | GetUserSPNs / Rubeus |
| AS-REP Roast | 不要求预认证 | GetNPUsers |
| ESC1 | 可注册模板 + 可伪造SAN | Certipy |
| ESC8 | HTTP enrollment + 中继 | ntlmrelayx |
| ACL → DA | GenericAll on user/group | BloodHound |
| NTLM Relay | 签名未强制 | Responder + relay |

始终：授权 → 枚举 → 路径评分 → 最小验证 → 清理。