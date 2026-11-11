# Platform Variant — Android

For skills that diverge on Android. Context + scripting notes, one level deep.

## Pattern

Variant lives either inline (frontmatter `os: android` + body OS
section) or as `platforms/android.md` inside the skill folder.

## Context

- Kotlin/Compose-first; Android lifecycle (Activity, Service,
  WorkManager) differs from desktop apps.
- Paths: internal storage, cache, external storage, scoped storage.

## Scripting

- Shell: user shell + `adb` for devices/emulators; Gradle wrapper.
- Builds: `./gradlew assembleDebug`, `adb install`, `logcat`,
  `adb shell dumpsys` for inspection.
- Pitfalls: background restrictions (Doze/App Standby), permission
  models, emulator vs device drift.

## Top matching skills

- android-jetpack-compose-expert — Jetpack Compose (OS-native UI)
- android-cli — Android CLI (Gradle/ADB scaffolding)
- android-ui-journey-testing — UI journeys on Android

Routing: provision by `os=android` within coding/research roles.
