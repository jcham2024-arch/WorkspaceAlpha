# Work Journal

Summaries of completed work. Append-only; sync after each entry
(`python3 .agent/tools/knowledge.py sync`).

## Entries

- 2026-11-07 | decision: knowledge system introduced | tags: knowledge
  Markdown files (JOURNAL/ERRORS/LESSONS/DECISIONS) are the truth; a
  SQLite FTS DB (.context/knowledge.db) + index.json are generated
  views, rebuilt by .agent/tools/knowledge.py sync.
