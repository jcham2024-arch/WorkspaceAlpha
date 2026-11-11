---
tier: experimental
last_reviewed: 2026-11-10
content_hash: ddb8a1b4df1026f3a3fe1635cb50b0360e9277454c8b05577ff148c6a72d7c2f
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: Conner K Ward
date_added: 2026-06-16
description: macOS screen recorder that captures the main display PLUS system audio via ScreenCaptureKit — no BlackHole/loopback driver, no sudo, just the standard Screen Recording permission. CLI-driven; fills the headless-screen-recording-with-system-sound gap QuickTime and `screencapture -v` can't.
docs: SKILL.md
license: MIT
name: macos-screen-recorder
risk: critical
source: community
source_repo: connerkward/macos-screen-recorder-system-audio
source_type: community
  - macos
  - screen-recording
  - system-audio
  - screencapturekit
  - cli
  - swift
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
---plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "Screen/audio/input capture requires sensitive macOS permissions; keep out of plugin-safe bundles."
---
## When to Use
Use when you need to script a screen recording WITH system sound on macOS from the CLI (demos, captures, voice-demo recording) — the case QuickTime and `screencapture -v` can't cover without a virtual audio device.
_Source: [connerkward/macos-screen-recorder-system-audio](https://github.com/connerkward/macos-screen-recorder-system-audio) (MIT)._
# macos-screen-recorder (sck-record)
`sck-record.swift` → compiled `sck-record` (binary gitignored; built by `setup-machine`, or
`swiftc -O sck-record.swift -o sck-record`). Records the main display + system audio via
ScreenCaptureKit.
```
./sck-record <out.mp4> <seconds>
```
**Intended use:** system audio from the CLI after a reviewed local build — no
BlackHole / loopback virtual device, no sudo; only the standard Screen Recording permission
(granted once to whatever app shells out). It is *not* a general "better than OBS/Screen
Studio" tool — it fills exactly the headless-CLI-with-system-audio gap.
`sck-record` is the raw capture primitive — it records, nothing more. To polish a
recording afterward (idle speed-up, auto-zoom, keystroke chips, smoothed cursor,
vertical export), pair it with
[screenstudio-alternative-skill](https://github.com/connerkward/screenstudio-alternative-skill):
record with `sck-record --no-cursor <out.mp4> <seconds>`, then run its post-production
pass on the resulting mp4. (Auto-zoom and keystroke overlays additionally need an
input-event log captured *during* recording, which that skill supplies; `sck-record`'s
pixels alone cover idle speed-up, cursor smoothing, and vertical export.)
## Availability and capture scope
This AAS tree contains the guide only: `sck-record.swift`, the compiled binary and `setup-machine` are not bundled. Obtain the exact reviewed upstream source/license and confirm OS/Swift/CLI support before compiling or claiming a recording. Existing permission alone does not authorize capturing the user's screen or system audio: confirm display/window, duration, destination and privacy scope. Use a new private output, hide unrelated sensitive surfaces, stop on schedule and inspect actual video/audio tracks before reporting success. Do not record input-event logs or upload the capture without the corresponding authorization.
## Limitations
- macOS only; it depends on ScreenCaptureKit and the user's Screen Recording permission.
- The recorder captures raw display and system audio but does not provide editing, auto-zoom, captions, or social-format polish by itself.
- Input-event overlays require a separate event log captured during recording; pixels alone cannot reconstruct keystrokes or precise click metadata.
## Platform variants
OS-specific companions for this skill:
- [Mac](platforms/mac.md)