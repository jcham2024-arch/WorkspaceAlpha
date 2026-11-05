# Preservation Rules

The following components are the reason this repair exists. They will be extracted into a separate product. After your repair their public APIs must be unchanged and their tests must pass.

## P1 — SecurityInterlock, RiskLevel, and audit chain

- Location: `security-interface/` and its app-side adapter.
- Public surface: `ToolExecutorPort`, `RiskLevel`, `SecurityInterlock.evaluate/execute`, `ToolRiskRegistry`, `AuditLogManager`, `FileAuditStore`.
- Must not: change method signatures, weaken fail-closed behavior, remove audit fields, or change the chain hash algorithm.
- Tests that must pass: null-call fail-closed, thrown-exception fail-closed, mismatched approval request id, budget exhaustion, audit chain tamper detection.

## P2 — WorkspacePathGuard

- Location: `app/src/main/java/.../workspace/WorkspacePathGuard.kt` (find it by class name; the exact path may differ).
- Must not: weaken containment rules (reject absolute paths, empty paths, `..`, canonical escapes, sibling-prefix bypasses like `$sandbox-evil`), or change the rejection exception type.
- Tests that must pass: all containment cases including the sibling-prefix case.

## P3 — AndroidKeyStoreManager

- Location: `app/src/main/java/.../security/AndroidKeyStoreManager.kt`.
- Must not: change the cipher (AES-256/GCM), change the key-alias scheme, or expose plaintext through a getter.
- Tests that must pass: round-trip encryption, no plaintext recoverable from DataStore bytes.

## P4 — core-engine

- Location: `core-engine/`.
- Must not: import Android, change port method signatures, or add runtime dependencies.
- Tests that must pass: all engine unit tests.

## What may be repaired freely

- `ChatScreen.kt`, `AppNavigation.kt`, `ChatViewModel.kt`, `WorkspaceScreen.kt` — Compose UI. Fix imports, replace non-existent Material 3 color roles with existing ones, resolve `@Composable` context errors. Do not redesign.
- `AgentOrchestrator.kt`, `ChatRepositoryImpl.kt` — align method signatures with their interfaces. Do not add methods unless the call site cannot be fixed otherwise.
- `FileGovernanceEngine.kt` — align types (pick `File` or `String` for paths and propagate).
- `SearchMemoryToolWorker.kt` — fix tokenizer-level syntax errors (unclosed braces, mismatched parens). If the file is structurally broken, quarantine it.
- `AndroidApprovalPort.kt` — align with SecurityInterlock's approval port.

## Quarantine protocol

If a file cannot be repaired without a rewrite (for example, a file that depends on `OfflineSyncManager`, which does not exist and is out of scope for extraction):

1. Move the file to `quarantine/` at the repo root, preserving its package path inside that directory.
2. Add the quarantine directory to the module's `sourceSets` exclusion in `build.gradle.kts`. This is the ONLY allowed build-file change.
3. Add an entry to `docs/repair-report.md` §Quarantined with the file path, the reason, and the unresolved dependency.
4. Do not delete the file.

## Do not

- Do not change `fallbackToDestructiveMigration()`. It is a known defect, scheduled for replacement during extraction. Changing it now is out of scope.
- Do not rename packages.
- Do not add Firebase, WorkManager, Hilt, Koin, or any dependency not already present, unless a compiler error explicitly requires it AND no existing dependency provides the symbol.
- Do not `@Suppress` a compiler error.
- Do not comment out code to make the build pass. Quarantine instead.