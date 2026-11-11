---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 74a70e12e44a3dc04b0eb0b29508aaae6431c9cf4fc56771bcf232821c0dddf4
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Generate structured changelogs from git history. Use when user asks \"what changed recently\", \"generate a changelog\", \"summarize commits\" or user wants to understand recent development activity.
name: wiki-changelog
risk: safe
source: community
---
# Wiki Changelog
Generate structured changelogs from git history.
## When to Use
- User asks "what changed recently", "generate a changelog", "summarize commits"
- User wants to understand recent development activity
## Procedure
1. Examine git log (commits, dates, authors, messages)
2. Group by time period: daily (last 7 days), weekly (older)
3. Classify each commit: Features (🆕), Fixes (🐛), Refactoring (🔄), Docs (📝), Config (🔧), Dependencies (📦), Breaking (⚠️)
4. Generate concise user-facing descriptions using project terminology
## Example
**User request:**
> Generate a changelog from the recent git history, grouping user-visible changes and linking each claim to its commit.
## Constraints
- Focus on user-facing changes
- Merge related commits into coherent descriptions
- Use project terminology from README
- Highlight breaking changes prominently with migration notes
### When to Use
This skill is applicable to execute the workflow or actions described in the overview.