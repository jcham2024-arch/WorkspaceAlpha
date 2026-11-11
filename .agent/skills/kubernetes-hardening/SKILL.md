---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 60c5026d8905d79f75aba25e488c69863c7028420023cc7e67017db3ef6c72b3
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: devops-skills
category: security
compatibility: Requires the relevant security tooling (scanners, vault CLIs) and an
date_added: 2026-09-20
description: Implement Kubernetes security contexts, Pod Security Standards, and network
license: MIT
license_source: "https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE"
name: app-reader
risk: critical
source: "https://github.com/BagelHole/DevOps-Security-Agent-Skills"
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
version: 1.0
---  policies.
  authorized scope for any active assessment. Docs-only; helper scripts and templates
  not bundled.
---
# Kubernetes Hardening
Secure Kubernetes clusters and workloads.
## When to Use This Skill
Use this skill when:
- Hardening Kubernetes clusters
- Implementing Pod Security Standards
- Configuring network policies
- Meeting security compliance
## Scope and validation
Confirm the exact cluster/namespace/version and authorized writes before applying policies. Examples are fragments: validate the reviewed image, namespace, service accounts, labels and required runtime storage. Pin the policy version to the target Kubernetes release where supported. Restricted admission controls new/updated pods; it does not retroactively fix running workloads or establish compliance.
## Pod Security Standards
```yaml
# Namespace with restricted policy
apiVersion: v1
kind: Namespace
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```
## Security Context
```yaml
apiVersion: v1
kind: Pod
  labels:
    app: web
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: registry.example.invalid/myapp:REVIEWED_IMMUTABLE_TAG
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
```
## Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
spec:
  podSelector:
    matchLabels:
      app: web
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```
## RBAC
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
subjects:
- kind: ServiceAccount
roleRef:
  kind: Role
  apiGroup: rbac.authorization.k8s.io
```
## Best Practices
- Enable Pod Security Standards
- Implement network policies
- Use RBAC with least privilege
- Enable audit logging
- Secure etcd with encryption
- Use service mesh for mTLS
- Regular security scanning
## Related Skills
- kubernetes-ops (`kubernetes-ops`) - K8s operations
- container-hardening (`container-hardening`) - Container security
## Limitations
- Apply guidance only within authorized scope; test destructive steps in non-production first.
- Docs-only import: upstream scripts and templates not bundled.
### Example
```bash
# Read-only first: inventory before any active step.
which <tool> && <tool> --help | head -n 20
```
> Adapted from [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills) (MIT); frontmatter, When to Use/Limitations, and safety boundaries added for upstream compliance. Docs-only import: helper scripts and templates not bundled.
NetworkPolicy enforcement requires a supporting CNI. The default-deny example also blocks DNS and dependencies until narrowly scoped rules are added; same-namespace pod selectors do not authorize arbitrary namespaces. Test allowed and denied flows from the real source identities and preserve recovery access. `readOnlyRootFilesystem` may require bounded writable temporary volumes; do not disable it blindly after a startup error. [Kubernetes NetworkPolicy behavior](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
## Platform variants
OS-specific companions for this skill:
- [Linux](platforms/linux.md)