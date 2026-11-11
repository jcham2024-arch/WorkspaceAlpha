# Debug Interface Triage

Scope: debug-interface-triage (hardware-security).
Load when: you need the debug-interface-triage (hardware-security) detail described in SKILL.md.

## Contents

- Debug Interface Triage

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# 调试接口分诊

1. 找丝印：TX RX GND VCC TDI TDO TCK TMS  
2. 电压匹配再连接  
3. 先只读串口日志  
4. 记录 U-Boot 中断键与环境变量（不随意 saveenv）  
5. 镜像提取后 SHA256  