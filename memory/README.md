# Memory — Knowledge System

Persistent knowledge for this workspace: what was done, what broke,
what was learned, what was decided. All files are append-only and
git-tracked; a SQLite FTS database (`.context/knowledge.db`) plus a
slim `index.json` make them searchable.

## Files

| File | Kind | Write when | Read when |
|---|---|---|---|
| `JOURNAL.md` | work | A task finishes (stage 04) | New session, before planning |
| `ERRORS.md` | error | A failure is diagnosed | A repeating symptom appears |
| `LESSONS.md` | lesson | A durable principle emerges | Before choosing an approach |
| `DECISIONS.md` | decision | A hard trade-off is settled | Before revisiting a settled area |
| `learnings.md` | session bullets | Session ends | Session start (existing, kept) |
| `checkpoints/` | resume points | Session dies / hands off | Resuming a task |

Format (append only — never rewrite history; corrections are new
entries with a new date):

```
- YYYY-MM-DD | <kind>: <title> | tags: <a,b,c>
  <continuation lines indented two spaces>
```

## Procedure

At stage 04 (verify), after work completes:
```bash
python3 .agent/tools/knowledge.py add --kind work \
  --title "built X" --tags build,validate \
  --body "what changed; what was verified"
python3 .agent/tools/knowledge.py add --kind error ...   # if errors were found
python3 .agent/tools/knowledge.py add --kind lesson ...  # if a principle emerged
python3 .agent/tools/knowledge.py add --kind decision ... # if a trade-off was settled
```
The `add` command appends AND syncs the DB + index automatically.
For bulk existing content, `python3 .agent/tools/knowledge.py sync`
rebuilds from the files. Search any time: `search <words>` /
`last --kind work -n 5`.

Query discipline: before planning (stage 01) search this memory
first; cite the file + date when applying a stored lesson.
