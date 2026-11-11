# code-reviewer — Android

Scope: Android variant of the `code-reviewer` skill.
Load when: you are doing `code-reviewer` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Use for any code review: a pull request, a diff, a commit, or a pasted function, handler or file in TypeScript, JavaScript, Python, Go, Swift, Kotlin, C#/.NET, Java, C, C++, Rust, Ruby, PHP or Dart/Flutter. Applies per-language rule packs (security such as SQL injection and missing auth, async and resource handling, error handling, performance) and scripts that score a PR's

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
