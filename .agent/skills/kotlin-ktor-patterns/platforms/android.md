# kotlin-ktor-patterns — Android

Scope: Android variant of the `kotlin-ktor-patterns` skill.
Load when: you are doing `kotlin-ktor-patterns` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing. Use when building a Ktor server — routing, plugins, auth, DI, serialization, or tests.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
