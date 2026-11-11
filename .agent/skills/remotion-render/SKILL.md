---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "21cebe87a36459b0c364557646158848b7d059eb9f065651b19a603dd5fc1b4f"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: remotion-render
description: Export a Remotion video
tier: "experimental"
version: 4.0.526
source_repo: remotion-dev/skills
source_type: official
source: remotion-dev
date_added: '2026-09-21'
risk: unknown
---

## When to Use
- Use when this upstream workflow matches the user's stated goal.
- Use when the task requires the procedures documented in this skill.

## General rendering strategy

Render a video using:

```
npx remotion render
```

Full list of options: https://www.remotion.dev/docs/cli/render.md

Render a still using:

```
npx remotion still
```

Full list of options: https://www.remotion.dev/docs/cli/still.md

## Transparent videos

See [Transparent videos](transparent-videos.md) for alpha-compatible codec/pixel-format settings. Confirm composition ID, frame range, output path and installed CLI version before rendering. Use a new output and inspect actual frames, duration, audio and alpha on a contrasting background; the command exiting successfully alone does not establish visual correctness.


## Examples

```text
User: Apply this skill to my current task.
Assistant: Follow the workflow in this skill, cite limitations, and ask before risky steps.
```

## Limitations

- Imported upstream skill; verify credentials, permissions, and safety boundaries before execution.
- Does not replace environment-specific validation, testing, or maintainer review.
