# Stage 04 — Verify

Run the checks the task demands: build, validation script, tests.
Report doc gaps explicitly (doc_gap_detected) instead of inventing
rules. Write `verification.md` (per-step output contract).
Then log the session to the knowledge system:
`python3 .agent/tools/knowledge.py add --kind work ...` (and
`error`/`lesson`/`decision` as applicable) and update
memory/learnings.md with what you learned before finishing.

Outputs: verified result + updated learnings.
