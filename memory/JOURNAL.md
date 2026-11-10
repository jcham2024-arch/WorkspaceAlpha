# Work Journal

Summaries of completed work. Append-only; sync after each entry
(`python3 .agent/tools/knowledge.py sync`).

## Entries

- 2026-11-07 | decision: knowledge system introduced | tags: knowledge
  Markdown files (JOURNAL/ERRORS/LESSONS/DECISIONS) are the truth; a
  SQLite FTS DB (.context/knowledge.db) + index.json are generated
  views, rebuilt by .agent/tools/knowledge.py sync.
- 2026-11-10 | work: Bootstrap project specs, decisions, and open questions | tags: spec,decision,bootstrap
  Created audit-persistence-spec.md, open-questions.md, 3 decision notes (Q1 RPO/RTO, Q2 SQLite sync, Q3 key rotation), replaced docs/README.md with full project documentation. Rebuilt manifest, wiki, skill index. validate.py passes.
