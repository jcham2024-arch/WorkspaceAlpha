# Reference

Scope: moved detail from SKILL.md.
Load when: needed by the operation described in SKILL.md.

## Contents

- Reference

## Checklist

- [ ] (see SKILL.md)

## Commands

| Fallback | Command |
|---|---|
| see body | — |

## Notes

- Original code preserved verbatim from SKILL.md.

```
```text
MyApp/
├── lib/
│   └── MyApp/
│       ├── App.pm           # Main module
│       ├── Config.pm        # Configuration
│       ├── DB.pm            # Database layer
│       └── Util.pm          # Utilities
├── bin/
│   └── myapp                # Entry-point script
├── t/
│   ├── 00-load.t            # Compilation tests
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── cpanfile                 # Dependencies
├── Makefile.PL              # Build system
└── .perlcriticrc            # Linting config
```

```
