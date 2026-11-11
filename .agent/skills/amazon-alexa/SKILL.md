---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 6d552c561982d22af2b85c07e0e4ef70c54321fa5253c3f84fe7bba4bb6da98d
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: renat
date_added: 2026-03-06
description: Integracao completa com Amazon Alexa para criar skills de voz inteligentes, transformar Alexa em assistente com Claude como cerebro (projeto Auri) e integrar com AWS ecosystem (Lambda, DynamoDB, Polly, Transcribe, Lex, Smart Home).
name: amazon-alexa
risk: critical
source: community
  - voice
  - alexa
  - aws
  - smart-home
  - iot
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
------
# AMAZON ALEXA — Voz Inteligente com Claude
## Detailed Guide
Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.
## When to Use This Skill
- When you need specialized assistance with this domain
## Do Not Use This Skill When
- The task is unrelated to amazon alexa
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
## Example
Prototype a read-only `ChatIntent` for one authorized test account. Verify the
interaction model and timeout in the ASK simulator before deploying; keep smart
home control disabled until account linking and device ownership checks pass.