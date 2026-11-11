---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "7e4deba44a6007e7ca0b27a2095a90f9bd0cbc3635c81a9ad551a48ef41c118e"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: dart-flutter-patterns
description: Production-ready Dart and Flutter patterns covering null safety, immutable state with Freezed, async composition, widget architecture, state management (BLoC, Riverpod, Provider), GoRouter navigation with auth guards, Dio networking, error handling, and testing. Use when writing or reviewing Dart and Flutter code — state, widgets, navigation, networking, or architecture.
tier: "experimental"
metadata:
  origin: ECC
---


# Dart/Flutter Patterns

## When to Use

Use this skill when:
- Starting a new Flutter feature and need idiomatic patterns for state management, navigation, or data access
- Reviewing or writing Dart code and need guidance on null safety, sealed types, or async composition
- Setting up a new Flutter project and choosing between BLoC, Riverpod, or Provider
- Implementing secure HTTP clients, WebView integration, or local storage
- Writing tests for Flutter widgets, Cubits, or Riverpod providers
- Wiring up GoRouter with authentication guards

## How It Works

This skill provides copy-paste-ready Dart/Flutter code patterns organized by concern:
1. **Null safety** — avoid `!`, prefer `?.`/`??`/pattern matching
2. **Immutable state** — sealed classes, `freezed`, `copyWith`
3. **Async composition** — concurrent `Future.wait`, safe `BuildContext` after `await`
4. **Widget architecture** — extract to classes (not methods), `const` propagation, scoped rebuilds
5. **State management** — BLoC/Cubit events, Riverpod notifiers and derived providers
6. **Navigation** — GoRouter with reactive auth guards via `refreshListenable`
7. **Networking** — Dio with interceptors, token refresh with one-time retry guard
8. **Error handling** — global capture, `ErrorWidget.builder`, crashlytics wiring
9. **Testing** — unit (BLoC test), widget (ProviderScope overrides), fakes over mocks

## Examples


---

Practical, production-ready patterns for Dart and Flutter applications. Library-agnostic where possible, with explicit coverage of the most common ecosystem packages.

---

## 1. Null Safety Fundamentals

### Prefer Patterns Over Bang Operator


### Avoid `late` Overuse


---

## 2. Immutable State

### Sealed Classes for State Hierarchies


### Freezed for Boilerplate-Free Immutability


---

## 3. Async Composition

### Structured Concurrency with Future.wait


### Stream Patterns


### BuildContext After Await


---

## 4. Widget Architecture

### Extract to Classes, Not Methods


### const Propagation


### Scoped Rebuilds


---

## 5. State Management: BLoC/Cubit


---

## 6. State Management: Riverpod


---

## 7. Navigation with GoRouter


---

## 8. HTTP with Dio


---

## 9. Error Handling Architecture


---

## 10. Testing Quick Reference


---

## References

- [Effective Dart: Design](https://dart.dev/effective-dart/design)
- [Flutter Performance Best Practices](https://docs.flutter.dev/perf/best-practices)
- [Riverpod Documentation](https://riverpod.dev/)
- [BLoC Library](https://bloclibrary.dev/)
- [GoRouter](https://pub.dev/packages/go_router)
- [Freezed](https://pub.dev/packages/freezed)
- Skill: `flutter-dart-code-review` — comprehensive review checklist
- Rules: `rules/dart/` — coding style, patterns, security, testing, hooks
