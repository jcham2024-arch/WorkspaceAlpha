# appium-skill — Android

Scope: Android variant of the `appium-skill` skill.
Load when: you are doing `appium-skill` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Generates production-grade Appium mobile automation scripts for Android and iOS in Java, Python, or JavaScript. Supports real device and emulator testing locally and on TestMu AI cloud with 100+ real devices.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
