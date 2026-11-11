# Direct Connect

Scope: direct-connect (hybrid-cloud-networking).
Load when: you need the direct-connect (hybrid-cloud-networking) detail described in SKILL.md.

## Contents

- Direct Connect

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Dedicated Connectivity Comparison

## Private Connectivity Options

| Provider | Service | Typical Use |
| -------- | ------- | ----------- |
| AWS | Direct Connect | Private connectivity into VPCs and Transit Gateway domains |
| Azure | ExpressRoute | Dedicated enterprise connectivity into VNets and Microsoft services |
| GCP | Cloud Interconnect | Dedicated or partner connectivity into VPCs |
| OCI | FastConnect | Private connectivity into VCNs through DRG attachments |

## Design Guidance

1. Prefer redundant circuits in separate facilities for production workloads.
2. Terminate private links into central transit or hub networking layers.
3. Use VPN as backup even when dedicated links are primary.
4. Validate BGP advertisements, failover behavior, and MTU assumptions during testing.
