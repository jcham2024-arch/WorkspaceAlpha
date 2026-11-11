# mobile-reverse — Android

Scope: Android variant of the `mobile-reverse` skill.
Load when: you are doing `mobile-reverse` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Authorized Android/iOS application reverse engineering and security testing: APK/IPA analysis, runtime instrumentation (Frida/Objection), SSL-pinning and jailbreak/root-detection bypass, per OWASP MASTG.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
