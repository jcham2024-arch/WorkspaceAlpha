# A2A Mapping — Envelope to Agent-to-Agent Semantics

This document maps WorkspaceAlpha delegation envelope fields to A2A (Agent-to-Agent)
v1.0 semantics. The JWS envelope is the A2A message; its fields correspond to
A2A task fields as shown below.

## Envelope → A2A Mapping

| Envelope Field | A2A Semantic | Description |
|----------------|--------------|-------------|
| `delegation_id` | Task ID | Unique identifier for the delegation/task |
| `from_agent` | Caller identity | The agent initiating the delegation |
| `to_agent` | Callee identity | The agent receiving the delegation |
| `delegation_type` | Task type | Type of delegation (MISSION/EXECUTION) |
| `objective` | Task description | What the delegatee should accomplish |
| `acceptance_criteria` | Task success conditions | Criteria that must be met for completion |
| `return_schema` | Artifact contract | Schema for return values |
| `authority` | Delegated capability scope | What the delegatee is authorized to do |
| `allowed_targets` | Permitted targets | Systems/resources the delegatee may access |
| `forbidden_targets` | Forbidden targets | Systems/resources the delegatee must not access |
| `max_steps` | Max execution steps | Maximum number of steps the delegatee may take |
| `termination_signal` | Termination condition | Signal that ends the delegation |

## Identity Block → A2A Identity

| Identity Field | A2A Semantic | Description |
|----------------|--------------|-------------|
| `agent_id` | Caller agent ID | Unique identifier for the calling agent |
| `agent_version` | Agent version | Version of the calling agent software |
| `issuer` | Identity issuer | Authority that issued the agent identity |
| `key_id` | Key ID | Key identifier for signature verification |
| `signature` | Signature | Cryptographic signature over the envelope body |

## Signature Verification

The `signature` field in the identity block is a detached signature over the
envelope body (excluding the `signature` field itself). The receiving agent
must:

1. Extract the signature from the envelope
2. Remove the `signature` field from the envelope
3. Canonicalize the remaining envelope (sorted keys, deterministic format)
4. Verify the signature using the public key associated with `key_id`
5. Reject the delegation if signature verification fails

## A2A Message Flow

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Caller    │────▶│   Callee     │────▶│   Caller     │
│ (Orchestrator│     │  (Manager)   │     │ (Orchestrator)│
└─────────────┘     └──────────────┘     └──────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   DELEGATION      ACCEPTANCE     RESULT
   ENVELOPE           ENVELOPE      ENVELOPE
   (MISSION)          (PLAN)        (RETURN)
```

## Example Envelope

```yaml
envelope_version: "1.0"
delegation_id: "del-abc123"
from_agent: "orchestrator-alpha"
to_agent: "taskmaster-beta"
delegation_type: "MISSION"
target_tier: "thinking"
authority: "PLAN"
allowed_targets: ["docs/README.md", "docs/specs/"]
forbidden_targets: [".agent/.env", ".context/manifest.json"]
max_steps: 12
termination_signal: "MISSION_COMPLETE"
return_schema: "schemas/return-envelope.schema.json"
return_format: "json"
identity:
  agent_id: "orchestrator-alpha"
  agent_version: "1.4.2"
  issuer: "workspace-alpha"
  key_id: "sha256:abc123..."
  signature: "..."
objective: "Review the audit persistence module for security compliance"
acceptance_criteria:
  - "All audit entries must include tenant_id"
  - "No secrets may be logged in plaintext"
  - "All tool invocations must be recorded in provenance"
non_goals:
  - "Do not modify production data"
  - "Do not access external networks"
context_evidence:
  - kid: "docs/contracts/decisions/Q3-key-rotation.md"
    bytes: [1024, 2048]
failure_trace: null
return_schema: "schemas/return-envelope.schema.json"
```

## Related

- `envelope/handoff-envelope.schema.json` — JSON Schema for delegation envelope
- `envelope/return-envelope.schema.json` — JSON Schema for return envelope
- `envelope/mission-envelope.yaml` — MISSION delegation template
- `envelope/execution-envelope.yaml` — EXECUTION delegation template
