# Third-Party Notices

This project bundles a master skill library (`.agent/skills/`) containing 3,520 skills from various upstream sources. This file documents the licenses of third-party skills that are **not** licensed under the project's root MIT License.

## License Compatibility Summary

| License | Count | MIT-Compatible | Notes |
|---------|-------|----------------|-------|
| MIT | ~86 | Yes | Project default |
| Apache 2.0 | 12 | Yes | Standard Apache 2.0 |
| Apache 2.0 + Additional Terms | 7 | **No** | Hosted service restriction (see below) |
| BSD-3-Clause | 1 | Yes | Weaviate skill |
| CC BY 4.0 | 2 | Yes | Attribution required |
| CC0 1.0 | 1 | Yes | Public domain dedication |

---

## Non-MIT-Compatible Skills (Require Attention)

### "tools-registry License" — Apache 2.0 with Additional Terms (7 skills)

**Skills affected:**
- `jev-memory`
- `lead-signals`
- `make-ugc`
- `rea-growth`
- `recruit`
- `treg`
- `web-access`

**License text:** Apache License 2.0 with Additional Terms:
1. **Hosted service restriction** — Cannot use the software to provide a hosted, managed, or embedded service to third parties (SaaS, managed registry, commercial distribution) without explicit written authorization from `jason@superdesign.dev`
2. **Contributor terms** — Contributions licensed under same terms; licensor may use commercially
3. Otherwise governed by Apache 2.0

**Impact:** These skills cannot be used to build a commercial hosted service without permission. For internal/private use, they are acceptable.

**Action required:** If this workspace is used to build a commercial SaaS offering, either:
- Obtain written authorization from the licensor, OR
- Remove these 7 skills from the active profile / master library

---

## MIT-Compatible Third-Party Licenses

### Apache License 2.0 (12 skills)

Standard Apache 2.0 — compatible with MIT. Includes patent grant.
- Skills: (various, identified by "Apache License" header)

### BSD-3-Clause (1 skill)

**weaviate** — Weaviate B.V. copyright 2020-2026. Standard 3-clause BSD, compatible with MIT.

### Creative Commons Attribution 4.0 International (2 skills)

**unslop-ui**, **requirements-writing** — CC BY 4.0 requires attribution when sharing/distributing. Compatible with MIT for code combination; attribution must be preserved.

### Creative Commons CC0 1.0 Universal (1 skill)

**sfxmint** — Public domain dedication. No restrictions, fully compatible.

---

## Recommendation

For the **7 skills with hosted service restrictions**, if this project remains internal/private (no commercial SaaS distribution), no action is needed. If commercial distribution is planned, evaluate whether to:
1. Seek authorization from `jason@superdesign.dev`
2. Replace with alternative skills
3. Accept the restriction and document compliance

All other third-party licenses are compatible with the project's MIT License.
