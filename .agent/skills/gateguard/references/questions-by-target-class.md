# Questions by target class

Scope: classification rules (paths), per-class question sets, public-surface
and data detection rules.
Load when: tuning the gate's questions, adding a language, or
understanding what counts as public surface / data.

## Contents

- Path classification (instruction/test/prose/config/code)
- Public-surface detection
- Data-question rules
- Special cases (every type counts as public; trims)

## Checklist

- [ ] Extension rules: supported JS/TS+Python+Go+Rust+shell list in body §"Questions fit the change"
- [ ] When in doubt (size limits, weird paths) default to the full four questions

## Commands

| Task | Command |
|---|---|
| See supported extensions + public-surface rules | SKILL.md "Questions fit the change" section |

## Notes

- Classification order (first match wins): instruction → test → prose → config → code.
- Code targets: four full questions (importers, public API, data schema, quote instruction); call-sites replace 1+2 when no public surface is touched; data question dropped with no I/O.
- Every class ends with "Quote the user's current instruction verbatim".
- Java, Kotlin, C#, C, C++ and every Write always count as public-surface.
- Public-surface test: any line declaring/exposing a public name on either side (export/declare/def/class/Go caps/Rust pub/shell function/etc.). Supported extensions cover JS/TS/Python/Go/Rust/shell; anything else (size limits, mixed output) gets the full questions word-for-word.
