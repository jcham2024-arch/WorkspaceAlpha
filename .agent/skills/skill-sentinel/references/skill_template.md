# Skill Template

Scope: skill_template (skill-sentinel).
Load when: you need the skill_template (skill-sentinel) detail described in SKILL.md.

## Contents

- Skill Template

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Template para Novas Skills

Recomendacoes sao hipoteses; confirmar escopo, necessidade e ausencia de alternativa existente antes de criar uma skill. Usar o template oficial do catalogo como contrato. Nao criar banco, scripts, dependencias, tracking ou rate limiting quando a tarefa nao precisa deles.

## Exemplo minimo

````markdown
---
name: nome-da-skill
description: "O que faz e quando usar, sem keywords redundantes."
risk: safe
source: self
date_added: "YYYY-MM-DD"
---

# Nome da skill

## When to Use

Descrever tarefas concretas e limites de escopo.

## Workflow

1. Identificar entradas e autorizacoes existentes.
2. Executar somente a tarefa solicitada.
3. Validar o resultado por evidencias apropriadas.

## Examples

Incluir um exemplo concreto com entradas sinteticas.

## Limitations

Declarar pressupostos, dependencias, custos e limites reais.
````

Datas, risco e proveniencia devem ser preenchidos honestamente. Para scripts opcionais, manter imports sem efeitos colaterais; ler fontes como dados inertes; criar estado privado fora do pacote apenas numa operacao explicita. Fechar conexoes SQLite em finally e usar parametros SQL. Nao registrar secrets nem codigo-fonte integral em logs.
