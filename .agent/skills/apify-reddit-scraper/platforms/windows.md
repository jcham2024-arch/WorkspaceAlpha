# apify-reddit-scraper — Windows

Scope: Windows variant of the `apify-reddit-scraper` skill.
Load when: you are doing `apify-reddit-scraper` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: Scrape Reddit posts, comments, subreddits and users with the harshmaur/reddit-scraper Apify Actor. No Reddit API key. Keyword search, date windows, full threads.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
