# Known Issues — Harness Branch

Baseline: 286 Kotlin errors across 18 files (per `docs/status.md`). This file is the triage map. Use it to fix root causes, not symptoms.

## Root cause A — Missing DI factories (blocks everything)

### A1 — `ChatRepository.getInstance(...)` does not exist

`ChatRepository` is an interface with no companion object. Callers such as `AgentTaskWorker` invoke `ChatRepository.getInstance(context)`.

Fix — add to `ChatRepository`:

```kotlin
companion object {
    @Volatile private var instance: ChatRepository? = null
    fun getInstance(context: Context): ChatRepository =
        instance ?: synchronized(this) {
            instance ?: ChatRepositoryImpl(context.applicationContext)
                .also { instance = it }
        }
}
```

Do not add Hilt, Koin, or Firebase. The manual singleton matches the branch's existing style.

### A2 — `ChatRepository.getAgentOrchestrator()` does not exist

Called by `AgentTaskWorker`. Not declared on the interface or the impl.

Fix — inspect `ChatRepositoryImpl` first. If it already constructs an `AgentOrchestrator`, add `fun getAgentOrchestrator(): AgentOrchestrator` to the interface and implementation. If it does not, do not add the method; instead quarantine `AgentTaskWorker` (see A3).

### A3 — `OfflineSyncManager.getInstance(...)` does not exist

Referenced by `AgentTaskWorker`. There is no such class anywhere in the repo.

Fix — this is out of scope for extraction. Quarantine `AgentTaskWorker.kt` per preservation-rules.md §Quarantine. Do not stub `OfflineSyncManager`.

### A4 — `AgentOrchestrator.executeToolCall` signature mismatch

`ChatRepositoryImpl.executeTool` calls `agentOrchestrator.executeToolCall(toolCall)` (single argument). `AgentOrchestrator.executeToolCall` is declared as `(String, String, Map<String, Any?>)`.

Fix — fix the call site in `ChatRepositoryImpl.executeTool` to decompose `toolCall` into `(serverName, toolName, args)`. Do not add an overload.

## Root cause B — Compose and Material 3 errors

### B1 — `ChatScreen.kt` (79 errors)

- `Icons.Default.PlayArrow` used without `import androidx.compose.material.icons.filled.PlayArrow`.
- Non-existent Material 3 color roles referenced: `warning`, `onSurfaceContainerHighest`, `onSurfaceContainer`.
  - Fix — map to existing roles: `warning` → `MaterialTheme.colorScheme.errorContainer` (or a local `Color` constant in the theme); `onSurfaceContainerHighest` → `onSurface`; `onSurfaceContainer` → `surfaceVariant`. Do not invent new `ColorScheme` fields.
- `@Composable` context violations — a composable state read occurs outside a `@Composable` function. Move the read inside `remember { }`, `LaunchedEffect { }`, or `derivedStateOf { }`.
- `'return' is prohibited here` inside a `@Composable` — a bare `return` in a composable body. Restructure with conditional branches. If you need an early-exit, wrap the early portion in an `if` and place the rest in an `else`.

### B2 — `AppNavigation.kt` (22 errors)

- `import androidx.navigation.compose.navArgument` is wrong. `navArgument` lives in `androidx.navigation`.
  - Fix — `import androidx.navigation.navArgument`.
- Verify every `NavType` import matches the version in the version catalog. Do not guess; check `gradle/libs.versions.toml` (or wherever versions are declared).

### B3 — `WorkspaceScreen.kt` (23 errors)

Same class of errors as B1: missing imports, non-existent roles, `@Composable` context.

### B4 — `ChatViewModel.kt` (21 errors)

Likely cascading from B1. Fix B1 first, re-run the build, and only fix what remains.

## Root cause C — Type and syntax errors

### C1 — `FileGovernanceEngine.kt` (40 errors)

Type inference failures. Align argument and return types with the `WorkspacePathGuard` and `SecurityInterlock` ports. If the file mixes `File` and `String` for paths, pick one and propagate it through call sites rather than casting.

### C2 — `SearchMemoryToolWorker.kt` (24 errors)

Tokenizer-level syntax errors — unclosed braces, mismatched parens, malformed lambdas. These are structural, not type issues. Open the file and inspect the regions flagged in the build log. If a single region is broken, fix it in place. If the file is structurally broken end to end, quarantine it.

### C3 — `AndroidApprovalPort.kt` (15 errors)

Align with `SecurityInterlock`'s approval port. Likely a method signature mismatch or a missing return.

### C4 — `AgentTaskWorker.kt` (9 errors)

Cascading from A1–A3. Quarantine per A3.

### C5 — `ChatRepositoryImpl.kt` (4 errors)

Cascading from A4. Fix A4 first.

### C6 — `AgentOrchestrator.kt` (3 errors)

Cascading from A4. Fix A4 first.

## Root cause D — Error-class summary (for progress tracking)

| Error class | Approx count | Primary files |
|---|---|---|
| `'return' is prohibited here` | 25 | ChatScreen, WorkspaceScreen |
| Type inference failures | 24 | FileGovernanceEngine, SearchMemoryToolWorker |
| `@Composable` context violations | 18 | ChatScreen, WorkspaceScreen |
| Missing imports | ~30 | ChatScreen, AppNavigation |
| Unresolved references (DI) | ~15 | AgentTaskWorker, ChatRepositoryImpl |
| Signature mismatches | ~10 | ChatRepositoryImpl, AgentOrchestrator, AndroidApprovalPort |
| Tokenizer / syntax | ~30 | SearchMemoryToolWorker and cascade |
| Remainder (files not listed above) | ~46 | various |

After each wave, run `sh gradlew assembleDebug 2>&1 | tee /tmp/build.log` and update `docs/repair-progress.md` with the new total.