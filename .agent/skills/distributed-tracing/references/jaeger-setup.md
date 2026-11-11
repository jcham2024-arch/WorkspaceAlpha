# Jaeger Setup

Scope: jaeger-setup (distributed-tracing).
Load when: you need the jaeger-setup (distributed-tracing) detail described in SKILL.md.

## Contents

- Jaeger Setup

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Jaeger integration checklist

## Inputs

Record the installed Jaeger version, storage backend, retention, query access and OTLP transport. Use that version's deployment guide; the collector endpoint and query UI are different services.

## Procedure and verification

Prepare configuration in a disposable environment. Restrict listeners and query access, use transport protection appropriate to the network, and verify storage credentials without exposing them in manifests. Send a synthetic trace and locate it through the query interface. Restart the disposable instance to check the chosen persistence behavior.

## Limitations

An in-memory demonstration is not durable production storage. A healthy UI does not prove ingestion, retention or authorization. Record the exact tested configuration and rollback path.
