# expo-ui-jetpack-compose — Android

Scope: Android variant of the `expo-ui-jetpack-compose` skill.
Load when: you are doing `expo-ui-jetpack-compose` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Build Android-native Expo SDK 55 UI with Jetpack Compose views/modifiers, Host sizing and platform-specific integration.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
