# matematico-tao — Android

Scope: Android variant of the `matematico-tao` skill.
Load when: you are doing `matematico-tao` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Analyze code complexity, dependency graphs, concurrency and invariants using explicit mathematical assumptions. Use for algorithm or architecture reviews; bundled Kotlin scanners produce advisory estimates, not formal proofs.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
