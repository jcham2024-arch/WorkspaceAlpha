# hexagonal-architecture — Android

Scope: Android variant of the `hexagonal-architecture` skill.
Load when: you are doing `hexagonal-architecture` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services. Use when introducing or refactoring toward Ports and Adapters, or when domain logic has become entangled with I/O.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
