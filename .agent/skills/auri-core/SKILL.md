---
tier: experimental
last_reviewed: 2026-11-10
content_hash: fb17f8db2039727513baaf8605640e7541d9fd3f6b05fe20dbafc30cd69c05c7
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: renat
date_added: 2026-03-06
description: ""Auri: assistente de voz inteligente (Alexa + modelo Claude configurado e verificado). Visao do produto, persona Vitoria Neural, stack AWS, modelo Free/Pro/Business/Enterprise, roadmap 4 fases, GTM, north star WAC e analise competitiva.""
name: auri-core
risk: critical
source: community
  - voice-assistant
  - product-vision
  - alexa
  - aws
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
------
# Auri - Core Product Skill
## Detailed Guide
Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.
## When to Use This Skill
- Ao revisar a visão de produto, hipóteses de GTM, métricas ou arquitetura proposta do Auri; não como prova de um serviço já implementado.
## Do Not Use This Skill When
- The task is unrelated to auri core
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise
## Example
**User request:**
> Review this product request with the Auri workflow and return the documented product deliverable.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
## Limites do produto e implementação
Este pacote é uma visão/planejamento de produto, não um backend implantado: não contém Lambda, modelos SAM, testes, chaves, alarmes nem implementações dos comandos `/Auri-*`. Não invente status OK, receita ou métricas. Preços, metas, margens, população Echo, comparações e cronogramas são cenários sem validação; inclua consumo de IA, voz, impostos, suporte, taxas e limites de uso antes de prometer “ilimitado”. Um skill Alexa não ganha automaticamente acesso a compras, calendário, música ou smart home; cada integração exige API/capacidade, permissão e política verificadas. Confirme modelo disponível, versões de SDK, voz/região/motor e subconjunto SSML suportado; os esboços não são código Python/XML executável. DynamoDB TTL é assíncrono, usa timestamp de expiração por item e não implementa sozinho retenção imediata de 90/365 dias. Não misture memórias de membros da família sem autorização e isolamento. Separe métricas e transcrições minimizadas, autentique pedidos de exclusão e trate conteúdo de voz como dado não confiável. Deploy SAM, IAM, publicação Alexa, cobrança e mensagens exigem autorização do usuário para conta, região, alvo e custos; preserve credenciais em Secret Manager e valide assinatura/replay de requisições Alexa no backend.