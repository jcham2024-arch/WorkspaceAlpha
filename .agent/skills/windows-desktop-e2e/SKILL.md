---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 0722e8ad2e9ccaa73ea2f34310f5c2d69b7eaf43af8469cfda2275807dd57459
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: E2E testing for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) using pywinauto and Windows UI Automation. Use when writing E2E tests for a Windows native desktop app with pywinauto or UI Automation.
name: windows-desktop-e2e
origin: ECC
---
# Windows Desktop E2E Testing
End-to-end testing for Windows native desktop applications using **pywinauto** backed by Windows UI Automation (UIA). Covers WPF, WinForms, Win32/MFC, and Qt (5.x / 6.x) — with Qt-specific guidance as a dedicated section.
## When to Activate
- Writing or running E2E tests for a Windows native desktop application
- Setting up a desktop GUI test suite from scratch
- Diagnosing flaky or failing desktop automation tests
- Adding testability (AutomationId, accessible names) to an existing app
- Integrating desktop E2E into a CI/CD pipeline (GitHub Actions `windows-latest`)
### When NOT to Use
- Web applications → use `e2e-testing` skill (Playwright)
- Electron / CEF / WebView2 apps → the HTML layer needs browser automation, not UIA
- Mobile apps → use platform-specific tools (UIAutomator, XCUITest)
- Pure unit or integration tests that don't need a running GUI
## Core Concepts
All Windows desktop automation relies on **UI Automation (UIA)**, a Windows-built-in accessibility API. Every supported framework exposes a tree of UIA elements with properties Claude can read and act on:
```
Your test (Python)
    └── pywinauto (UIA backend)
        └── Windows UI Automation API   ← built into Windows, framework-agnostic
            └── App's UIA provider      ← each framework ships its own
                └── Running .exe
```
**UIA quality by framework:**
| Framework | AutomationId | Reliability | Notes |
|-----------|-------------|-------------|-------|
| WPF | 5/5 | Excellent | `x:Name` maps directly to AutomationId |
| WinForms | 4/5 | Good | `AccessibleName` = AutomationId |
| UWP / WinUI 3 | 5/5 | Excellent | Full Microsoft support |
| Qt 6.x | 5/5 | Excellent | Accessibility enabled by default; class names change to `Qt6*` |
| Qt 5.15+ | 4/5 | Good | Improved Accessibility module |
| Qt 5.7–5.14 | 3/5 | Fair | Needs `QT_ACCESSIBILITY=1`; objectName manual |
| Win32 / MFC | 3/5 | Fair | Control IDs accessible; text matching common |
## Setup & Prerequisites
Verify UIA is reachable:
Install **Accessibility Insights for Windows** (free, from Microsoft) — your DevTools equivalent for inspecting the UIA element tree before writing any test.
## Testability Setup (by Framework)
The single most impactful thing you can do is **give every interactive control a stable AutomationId** before writing tests.
### WPF
### WinForms
### Win32 / MFC
### Qt — see dedicated section below
---
## Page Object Model
```
tests/
├── conftest.py          # app launch fixture, failure screenshot
├── pytest.ini
├── config.py
├── pages/
│   ├── __init__.py      # required for imports
│   ├── base_page.py     # locators, wait, screenshot helpers
│   ├── login_page.py
│   └── main_page.py
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   └── test_main_flow.py
└── artifacts/           # screenshots, videos, logs
```
### base_page.py
### login_page.py
### conftest.py
> For new projects prefer the **Tier 1 sandbox fixture** (see below) — it adds filesystem isolation at zero extra cost. This basic fixture is for minimal/legacy setups only.
### config.py
### pytest.ini
## Locator Strategy
```
AutomationId  >  Name (text)  >  ClassName + index  >  XPath
  (stable)         (readable)       (fragile)           (last resort)
```
Inspect with Accessibility Insights → **Properties** pane → look for `AutomationId` first.
## Wait Patterns
**Never use `time.sleep()` as primary synchronization** — use `wait()` or `wait_until()`.
## Artifact Management
## Per-Step Trace (opt-in)
The default failure screenshot is often too thin for diagnosing flaky tests. The step-level trace below is **off by default** — enable it only when reproducing a flaky case.
### Enable
### Patch into BasePage
### Caveats
- **PII / credentials**: `type_text` content is `<redacted>` by default. Never set `E2E_TRACE_INCLUDE_TEXT=1` on login or payment flows.
- **Overhead**: ~50–200ms per action + one PNG per step on disk. Don't enable on the default CI matrix — only on a dedicated flake-repro job.
- **Artifact bloat**: a long flow produces tens of MB; tune `retention-days` accordingly.
- **Parallel/rerun hygiene**: this simple example appends to `trace.jsonl` and uses a class-level counter. Clear the artifact directory before reruns, and use per-worker artifact dirs for parallel tests.
- **Coverage gap**: actions performed outside `BasePage` (raw `pywinauto` calls in test code) are not traced.
## Flaky Test Handling
Common causes and fixes:
| Cause | Fix |
|-------|-----|
| Control not ready | Replace `time.sleep` with `wait_visible` |
| Window not focused | Add `win.set_focus()` before interactions |
| Animation in progress | `wait_until(lambda: not loading_indicator.exists())` |
| Dialog timing | `wait_window(title, timeout=15)` |
| CI display not ready | Set `DISPLAY` or use virtual desktop in CI |
| `set_edit_text` raises NotImplementedError | UIA ValuePattern missing (common on Qt 5.x) — `BasePage.type_text` already falls back to `keyboard.send_keys` |
| Control exists but `wait_visible` times out | Window minimised or off-screen — call `win.restore()` + `win.set_focus()` before waiting |
## Test Isolation & Sandbox
Three tiers of isolation — use the lightest tier that satisfies your needs.
### Tier 1 — Filesystem Isolation (default, always use)
Each test gets its own `APPDATA` / `LOCALAPPDATA` / `TEMP` via `subprocess.Popen` and `Application.connect()`. pytest's `tmp_path` fixture handles cleanup automatically.
### Tier 2 — Windows Job Object (optional: process-lifetime containment)
Attach the process to a Job Object so it is **automatically terminated** when
the test fixture's job handle is GC'd. Also prevents the app from spawning
child processes that escape fixture cleanup.
> **Scope of isolation:** Job Objects do NOT virtualize filesystem access or
> block network traffic. File-write and network isolation require AppContainer,
> Windows Firewall rules, or Tier 3 (Windows Sandbox). Use Tier 2 only for
> process-lifetime and child-process containment.
Requires no extra dependencies.
### Tier 3 — Windows Sandbox (CI full-OS isolation)
When you need a clean Windows image per run (no leftover registry keys, no
shared GPU state, true isolation), run the **entire test suite** inside
[Windows Sandbox](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-overview).
**Requirement:** Windows 10/11 Pro or Enterprise, Virtualization enabled.
Create `e2e-sandbox.wsb` in your project root:
Launch: `WindowsSandbox.exe e2e-sandbox.wsb`
> pywinauto and the app both run **inside** the sandbox (same session required).
> Artifacts are written back to the host via the mapped folder.
### Tier comparison
| Tier | Isolation | Setup cost | Works on CI | Use when |
|------|-----------|-----------|-------------|----------|
| 1 — `tmp_path` env redirect | Filesystem | Zero | Always | Default for all tests |
| 2 — Job Object | Process tree | Low | Always | Prevent child-process escape |
| 3 — Windows Sandbox | Full OS | Medium | Needs Pro/Enterprise image | Nightly clean-room runs |
### Prevent hanging tests
Add `pytest-timeout` to cap any single test. In `pytest.ini` set `timeout = 60` and `timeout_method = thread`. Note: `thread` method cannot kill Qt app subprocesses on Windows — add `atexit.register(lambda: [p.kill() for p in psutil.Process().children(recursive=True)])` in `conftest.py` to reap orphans.
## CI/CD Integration
## Qt Specific
### Enable UIA in Qt 5.x
Qt 5.x accessibility is disabled by default in some builds (especially 5.7–5.14). Set the environment variable **before** launching. Qt 6.x enables accessibility by default — skip this step for Qt 6.
Or export it in CI:
### Add Stable Identifiers to Qt Widgets
Centralise all IDs in a header to avoid typos:
### Qt-Specific Quirks
**QComboBox** — the dropdown is a separate top-level window:
**QMessageBox / QDialog** — also separate top-level windows:
**QTableWidget / QTableView** — row/cell access:
**Self-drawn controls** (`paintEvent`-only, `QGraphicsView`, `QOpenGLWidget`) — UIA cannot see their internals. Use the Fallback section below.
## Fallback: Screenshot Mode
When a control is not reachable via UIA (self-drawn, third-party, game engine):
### DPI / Scaling Rules (screenshot mode only)
Screenshot matching is brutally sensitive to Windows display scaling (100% / 125% / 150%). Three hard rules:
1. **Capture templates at the same scale as the target machine.** Don't try to rescue a mismatch with `PIL.Image.resize` — `cv2.matchTemplate` is very fragile against resampling artefacts.
2. **Pin the CI display scaling.** On `windows-latest` add a step like `Set-DisplayResolution 1920 1080 -Force` and disable per-monitor DPI scaling, so screenshot dimensions are reproducible.
3. **Record the scale alongside each artefact.** On capture, write `GetDpiForWindow(hwnd) / 96` to `artifacts/<test>/metadata.json` — postmortems become obvious instead of guess-work.
> Process-level DPI awareness (`SetProcessDpiAwarenessContext`) **can conflict with Qt's own DPI handling** when the app under test is Qt-based. Prefer "same-scale templates + CI pin" over flipping process-wide DPI mode in fixtures.
### Debugging Match Confidence
When tuning the `confidence` threshold, the only sane workflow is to **see** where the match landed. The helper below is diagnosis-only — do not call it from test code.
**Use sparingly** — image matching breaks on DPI changes, theme switches, and partial occlusion.
Always try UIA first; fall back to screenshots only for genuinely unreachable controls.
## Anti-Patterns
## Running Tests
## Related Skills
- `e2e-testing` — Playwright E2E for web applications
- `cpp-testing` — C++ unit/integration testing with GoogleTest
- `cpp-coding-standards` — C++ code style and patterns
## Platform variants
OS-specific companions for this skill:
- [Windows](platforms/windows.md)