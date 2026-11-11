---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 8a1cc81fbbcb22b955839e840865edaa7bd14e441e352c904c251de328f40dcc
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-09-21
description: Transcribing, displaying and animating captions
name: remotion-captions
risk: critical
source: remotion-dev
source_repo: remotion-dev/skills
source_type: official
version: 4.0.526
---
## When to Use
- Use when this upstream workflow matches the user's stated goal.
- Use when the task requires the procedures documented in this skill.
All captions must be processed in JSON. The captions must use the [`Caption`](https://www.remotion.dev/docs/captions/caption.md) type which is the following:
```ts
import type { Caption } from "@remotion/captions";
```
This is the definition:
```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
  pageBreakAfter?: boolean;
};
```
## Generating captions
To transcribe video and audio files to generate captions, load the [transcribe-captions.md](transcribe-captions.md) file for more instructions.
## Displaying captions
To display captions in your video, load the [display-captions.md](display-captions.md) file for more instructions.
## Importing captions
To import captions from a .srt file, load the [import-srt-captions.md](import-srt-captions.md) file for more instructions.
## Examples
```text
User: Apply this skill to my current task.
Assistant: Follow the workflow in this skill, cite limitations, and ask before risky steps.
```
## Limitations
- Imported upstream skill; verify credentials, permissions, and safety boundaries before execution.
- Does not replace environment-specific validation, testing, or maintainer review.