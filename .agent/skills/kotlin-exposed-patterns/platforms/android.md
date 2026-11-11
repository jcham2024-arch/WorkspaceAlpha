# kotlin-exposed-patterns — Android

Scope: Android variant of the `kotlin-exposed-patterns` skill.
Load when: you are doing `kotlin-exposed-patterns` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern. Use when working with the Exposed ORM — DSL or DAO queries, transactions, pooling, or migrations.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
