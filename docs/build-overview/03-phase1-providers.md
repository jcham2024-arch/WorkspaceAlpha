> **ChatWorkspace Build Task Overview** — Part 3 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`02-phase0-foundation.md`](02-phase0-foundation.md) · Next: [`04-phase2-chat-creation-git.md`](04-phase2-chat-creation-git.md)

## 4. Phase 1 — Providers (Week 2)

Goal: provider CRUD, encrypted key storage, default promotion, delete guards.

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-020 | Port D6 `ProviderPresets` (7 presets) | WS-P | T-012 | Presets seed base URL + model id, not API key |
| T-021 | Port D7 `ProviderConfigurationManager` (DataStore) | WS-P | T-020 | CRUD + default promotion on delete pass |
| T-022 | Port D8 `AndroidKeyStoreManager` (AES-256/GCM) | WS-P | T-012 | Round-trip test passes; no plaintext in DataStore bytes |
| T-023 | Define `ProviderConfig` Room entity + DAO | WS-S | T-015 | Schema migration test passes |
| T-024 | `ProviderRepository` in `:data` bridging donor manager to ChatWorkspace | WS-I | T-021, T-023 | Repository contract test passes |
| T-025 [P] | Providers list screen | WS-N | T-014, T-024 | List, empty state, default badge |
| T-026 [P] | Add/Edit provider screen | WS-N | T-024 | Validation on save; key masked after save |
| T-027 | Delete provider guard (blocked if referenced by active chat) | WS-N | T-024 | A12 passes |
| T-028 | Donor checklist D6–D8 complete | WS-P | T-020–T-022 | All checklist items checked in supplement §4 |
| T-029 | Integration test: full provider lifecycle | WS-H | T-025–T-027 | Test in CI, A1 and A10 (partial) pass |

### Phase 1 exit gate — M1

- A1 (multiple providers, one default) passes.
- A12 (delete guard) passes.
- No plaintext key in DataStore, logs, workspace.
- D6–D8 checklists complete.

---
