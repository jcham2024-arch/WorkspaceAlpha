# expo-ui — Android

Scope: Android variant of the `expo-ui` skill.
Load when: you are doing `expo-ui` on Android.

## Context

Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.
Topic: Build native UI with the @expo/ui package: real SwiftUI on iOS and Jetpack Compose on Android rendered from React in an Expo or React Native app.

## Scripting

Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
