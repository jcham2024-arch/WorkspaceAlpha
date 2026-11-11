---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "9b3c91e24027cbfb42433e8f31ae8dfe950eef24a50cd8f177f0b9951ffc5d17"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: conductor-manage
description: "Manage track lifecycle: archive, restore, delete, rename, and cleanup"
tier: "experimental"
risk: critical
source: community
date_added: "2026-02-27"
---


# Track Manager

Manage the complete track lifecycle including archiving, restoring, deleting, renaming, and cleaning up orphaned artifacts.

## Use this skill when

- Archiving, restoring, renaming, or deleting Conductor tracks
- Listing track status or cleaning orphaned artifacts
- Managing the track lifecycle across active, completed, and archived states

## Do not use this skill when

- Conductor is not initialized in the repository
- You lack permission to modify track metadata or files
- The task is unrelated to Conductor track management

## Instructions

- Detailed path/transaction safeguards in the playbook apply to every mutation. Preserve prior status and unknown metadata fields; restoration must not falsely complete an abandoned track.
- Preview the exact affected paths and preserve unrelated staged work; do not use broad staging or assume a failed multi-file operation rolled back.

- Verify `conductor/` structure and required files before proceeding.
- Determine the operation mode from arguments or interactive prompts.
- Confirm destructive actions (delete/cleanup) before applying.
- Update `tracks.md` and metadata consistently.
- If detailed steps are required, open `resources/implementation-playbook.md`.

## Safety

- Backup track data before delete operations.
- Avoid removing archived tracks without explicit approval.

## Resources

- `resources/implementation-playbook.md` for detailed modes, prompts, and workflows.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
