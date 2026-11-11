# Beats

Scope: beats (hyperframes-cli).
Load when: you need the beats (hyperframes-cli) detail described in SKILL.md.

## Contents

- Beats

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Generate a project beat grid

Use `hyperframes beats` when an existing HyperFrames project needs the Studio-compatible beat file for its music track. This is a CLI utility, not a complete video workflow.

```bash
npx hyperframes beats
npx hyperframes beats ./my-video
npx hyperframes beats ./my-video --json
```

Given an audio or video file instead of a folder (`npx hyperframes beats music.mp3 --json`), `beats` analyses that file and prints `{ ok, file, count, bpm, beatTimes }`; it writes nothing.

The project must contain a local music `<audio>` source. Mark it with `data-timeline-role="music"`; an id containing `music`, `bgm`, or `soundtrack` is also recognized. The command decodes that file with ffmpeg, tracks its beats, and writes `beats/<audio-relative-path>.json`.

If the track has no steady beat, the command fails and writes nothing. If ffmpeg is missing, run `npx hyperframes doctor`.

For a whole video cut to a music track, see `/hyperframes` → `references/film.md`.
