# mobile-design — Android

Scope: Android variant of the `mobile-design` skill.
Load when: you are doing `mobile-design` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Design and review iOS, Android, React Native or Flutter interfaces for touch, accessibility, navigation, offline behavior and measured performance. Use for mobile app UI work; not a mobile compliance certification.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
