# Reference

Scope: moved detail from SKILL.md.
Load when: needed by the operation described in SKILL.md.

## Contents

- Reference

## Checklist

- [ ] (see SKILL.md)

## Commands

| Fallback | Command |
|---|---|
| see body | — |

## Notes

- Original code preserved verbatim from SKILL.md.

```
```bash
# 1. 安装 32 位 Python（和 64 位可以共存）
# 下载地址：https://www.python.org/downloads/windows/

# 2. 用 32 位 Python 安装依赖
py -3.12-32 -m pip install -r requirements.txt

# 3. 用 32 位 Python 编译
py -3.12-32 -m nuitka --standalone ...你的参数
```

```
