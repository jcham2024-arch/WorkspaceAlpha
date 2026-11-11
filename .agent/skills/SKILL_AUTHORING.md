# Skill Authoring — Master Guidance

Canonical source: Anthropic, [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
[Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview),
plus the Agent Skills open standard (agentskills/agentskills,
Apache-2.0) and this workspace's REFERENCE_FORMAT.md. Applies to
every skill in .agent/skills/ (master library).

## 1. The schema (hard spec)

- `SKILL.md` frontmatter: `name` (≤ 64 chars) and `description`
  (≤ 1024 chars). No other frontmatter fields are required.
- Folder name MUST match frontmatter `name` after Unicode NFKC
  normalization. Ours: suffixed imports (`<source>__<name>`) are
  indexed in INDEX.csv; profile wiring uses folder name.
- Structure: `SKILL.md` (required) + optional `scripts/`,
  `references/`, `assets/`.
- Progressive disclosure (3 tiers): metadata always loaded
  (~50–100 tokens/skill), body on trigger, references on demand.
  This is what makes a 3,520-skill library affordable.

## 2. Size tiers (this workspace's numbers)

| Tier | Budget | Rule |
|---|---|---|
| Frontmatter | description ≤ 60 words, third person | Not just what it does, but WHEN to use it (trigger terms) |
| Body (SKILL.md) | < 500 lines (< ~5K tokens) | Workflow + checklists + pointers only |
| references/ | unbounded, one level deep from SKILL.md | Deeper nesting gets partial-read (`head -100`) — avoid |
| Reference files > 100 lines | table of contents on top | Agent can jump to sections |
| Scripts | executed, not loaded | Prefer over long instructions; must handle errors (solve, don't punt) |

Rule of thumb (Anthropic): content beyond 500 lines splits into
files. Body is the trigger-serving index, references are chapters.

## 3. Wording & language rules

- Assume the agent is smart. Write the minimum it hasn't got.
  Test each sentence: "Does the agent know this already?"
  Cut: filler, hedging (just, really, basically), pleasantries,
  narration, banners. Keep numbers, API names, file paths verbatim.
- Descriptions: third person, specific, both WHAT and WHEN. E.g.
  pdf-processing: "Extract text and tables from PDF files, fill
  forms, merge documents. Use when working with PDF files or when
  the user mentions PDFs, forms, or document extraction."
- Naming: gerund form ("Processing PDFs"), consistent across the
  collection; avoid Helper/Utils/Data.
- One term per concept ("field", not field/box/element). No
  Windows backslashes (always forward slashes).
- Offering choices: one default + escape hatch, never a menu.
- High/medium/low freedom matches task fragility: free-form for
  reviews; templates for report shapes; exact scripts for fragile
  ops. Narrow bridge → guardrails; open field → direction.
- No time-sensitive data inline ("before Aug 2025…") — move to an
  "old patterns" block.

## 4. Body structure patterns

- **Single-file**: metadata + quick-start + one example. Best for
  simple skills.
- **High-level + references (Pattern 1)**: quick start in body,
  FORMS.md / REFERENCE.md / EXAMPLES.md linked by name.
- **Domain split (Pattern 2)**: reference/<domain>.md per domain;
  grep to find the domain fast (bigquery example). Fits our
  categorized master: CATEGORIZATION.csv routes to category first.
- **Conditional details (Pattern 3)**: basic inline, advanced in
  linked files ("For tracked changes: See REDLINING.md").
- Workflows: step checklists the agent copies and ticks off.
  Feedback loops where errors crash: validate → fix → repeat.
- Templates: strict (exact structure) vs flexible ("sensible
  default — adapt"). Examples: input/output pairs.

## 5. Scripts, code, MCP and runtime

- Scripts solve, don't punt: handle FileNotFoundError etc.;
  document timeouts/retries (no magic numbers); run, don't paste.
- Utility scripts > inline generation (reliable, token-cheap,
  consistent). State execute-vs-read intent explicitly.
- Plan-validate-execute for batch/destructive work (create plan
  file → validate → execute → verify).
- MCP tools: always `ServerName:tool_name` fully qualified.
- Declared dependencies: name the pip/npm install; never assume
  tools are installed. Runtime here is Python 3 stdlib + this
  harness's PATH — see scripts in .agent/tools/.

## 6. Evaluation & writing process (TDD for skills)

1. Build evaluations FIRST (≥ 3 scenarios covering real failures).
2. Baseline without the skill; write minimal instructions to close
   the gap; iterate.
3. Agent A authors / refines; Agent B tests in real tasks. Observe
   navigation; tune description wording until selection is reliable.
4. Test across model tiers (Haiku needs more detail; Opus needs
   less): our profiles' smallest-model rule leans on this.
5. Team feedback: does it fire when expected; what's missing.

Our eval harness: .agent/skills/README.md (one eval per profile).

## 7. Reference format (this workspace's standard)

Every references/*.md: `# Title` → `Scope:` → `Load when:` →
`## Contents` → `## Checklist` → `## Commands` table → `## Notes`.
One level deep. See REFERENCE_FORMAT.md in this folder.

## 8. Platforms (cross-platform vs OS-specific)

- Cross-platform default: most skills are `os=cross` (OS-agnostic).
- OS tags: `android | windows | linux | mac` (whole-word match in
  CATEGORIZATION.csv's `os` column).
- Two attachment patterns (PLATFORMS.md): inline `os:` frontmatter
  tag + OS section, or `skills/<name>/platforms/<os>.md` companions.
- An OS variant contains context (semantics/paths/APIs) + scripting
  (best shell + commands + pitfalls) for THAT OS only.
- Provision by `task_type + level + os`, never all 4 variants unless
  the task spans them.

## Checklist (merge of Anthropic + workspace)

Core:
- [ ] Description: third person, ≤60 words, what + when, trigger terms
- [ ] Body: < 500 lines, workflow/checklists only, one level refs
- [ ] Terms consistent; forward slashes; no time-sensitive content
- [ ] Freedom level matches task fragility
- [ ] Examples concrete; templates strict-or-flexible as needed

Code:
- [ ] Scripts handle errors; no magic numbers; packages declared
- [ ] Plan-validate-execute where it matters
- [ ] MCP names fully qualified (ServerName:tool)

Process:
- [ ] ≥ 3 evals; tested on real tasks + multiple model tiers
- [ ] Agent A/B loop used; selection tune checked
- [ ] Team feedback incorporated
