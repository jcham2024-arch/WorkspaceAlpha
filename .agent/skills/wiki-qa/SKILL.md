---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 4e969fa982b5b13687accdb7400fb7fa0880159df05b25d9036b2f1112720cd3
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Answer repository questions grounded entirely in source code evidence. Use when user asks a question about the codebase, user wants to understand a specific file, function, or component, or user asks \"how does X work\" or \"where is Y defined\".
name: wiki-qa
risk: safe
source: community
---
# Wiki Q&A
Answer repository questions grounded entirely in source code evidence.
## When to Use
- User asks a question about the codebase
- User wants to understand a specific file, function, or component
- User asks "how does X work" or "where is Y defined"
## Procedure
1. Detect the language of the question; respond in the same language
2. Search the codebase for relevant files
3. Read those files to gather evidence
4. Synthesize an answer with inline citations
## Response Format
- Use `##` headings, code blocks with language tags, tables, bullet lists
- Cite sources inline: `(src/path/file.ts:42)`
- Include a "Key Files" table mapping files to their roles
- If information is insufficient, say so and suggest files to examine
## Rules
- ONLY use information from actual source files
- NEVER invent, guess, or use external knowledge
- Think step by step before answering
### When to Use
This skill is applicable to execute the workflow or actions described in the overview.
## Example
**User request:**
> Answer this repository question using only source-code evidence, with direct file and line references.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.