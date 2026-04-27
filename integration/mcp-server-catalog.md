# MCP Server Catalog

*Framework-level catalog of MCP servers that have been vetted at least once for use under CADRE. Catalog entries are engagement-agnostic and informational; they do not constitute approval for any specific engagement. Each engagement's actual allowlist is built fresh from the onboarding workflow (`integration/mcp-server-onboarding.md`).*

---

## Catalog status as of v1.0

The catalog is intentionally lean at framework launch. The MCP ecosystem (specification revision 2025-11-25) is maturing, conformance varies, and operators' specific deployments will determine which servers actually warrant onboarding. The catalog grows by use, not by speculation.

The following categories are documented as classes; specific servers within each class must complete onboarding per engagement.

---

## Class A — Operator-owned servers

Servers built and operated by the operator's own engineering team (or by trusted contractors under operator control). Default framework-level trust tier: I (highest), subject to engagement-specific verification.

Common cases:

- Internal documentation and knowledge-base servers
- Operator-side data lake or warehouse exposure
- Operator-side ticket and case-management systems

Conformance posture: the operator commits to RFC 8707 conformance during server construction; conformance is verified per engagement in any case.

---

## Class B — Productivity SaaS connectors

Servers from vendors offering productivity, collaboration, or knowledge-work tools. Default framework-level trust tier: II, subject to attestation review and conformance verification per engagement.

Common cases:

- Email, calendar, document collaboration
- Issue tracking, project management
- Internal chat and communication
- Knowledge-base and wiki platforms

Conformance posture: most reputable vendors in this class are progressing toward RFC 8707 conformance during 2026; verification is per-version, not vendor-wide. [INFERENCE — based on the vendor maturity trajectory observable in the public MCP server lists; specific vendor conformance must be confirmed at onboarding time]

---

## Class C — Sector-specific data services

Servers specific to regulated sectors: healthcare data exchanges, financial-data providers, legal research platforms, regulatory-data services. Default framework-level trust tier: III, requiring sector-specific attestation review.

Conformance posture: variable. Some sector vendors prioritize protocol conformance; others lag because their primary regulatory frame is not protocol security. Onboarding for sector servers should expect Tier IV (compensated trust) more often than other classes. [INFERENCE]

---

## Class D — Infrastructure and dev tooling

Servers exposing infrastructure (cloud APIs, database admin), CI/CD systems, monitoring, observability, security tooling. Default framework-level trust tier: II for read access; III for any side-effect-producing capability.

Side-effect-producing capabilities (deploying, mutating cloud resources, scaling, terminating) require Tier 3 HITL discipline regardless of server trust tier. The trust-tier classification governs server-side concerns; HITL discipline governs cadre-side action.

---

## Class E — Public-data and OSINT services

Servers exposing public information: government data, public regulatory databases, public business directories, open-data lakes. Default framework-level trust tier: II.

The principal risk in this class is freshness and accuracy, not data exposure. Conformance posture: variable. Audit emissions emphasize source-archiving (A04) so that data drift after retrieval can be reconstructed.

---

## Class F — Generative tooling

Servers offering generative capabilities: code generation, image generation, text augmentation. CADRE generally avoids this class because the cadre already has model access through the orchestrator's primary provider; bringing additional generative capability through an MCP server typically expands the model attack surface without proportional benefit.

When a Class F server is required (specialized capability not available via the primary provider), default tier is III, with explicit compensating controls covering output verification.

---

## What the catalog does not establish

The catalog does not constitute a standing approval for any specific server. Onboarding per engagement is required regardless of whether the class or specific vendor is catalogued. The catalog informs the onboarding process; it does not bypass it.

The catalog is also not exhaustive. New servers are catalogued when first onboarded. Servers no operator has onboarded under CADRE simply do not appear; their absence is not a judgment.

---

## Maintenance

The catalog is maintained as part of the framework's normal documentation discipline. New entries follow the framework change procedure (Conventional Commits with `cadre(integration)` scope, peer review, CI). Removals (a server has been deprecated by its vendor or has had its conformance posture invalidated) follow the same discipline.

A20 (compliance mapper) flags catalog entries when relevant regulatory or vendor changes occur; the framework maintainer (currently Barry Hurd Intelligence Lab) processes those flags and updates the catalog.

---

## Cross-references

- `integration/mcp-server-onboarding.md` — the per-engagement process
- `integration/external-tool-allowlist.md` — non-MCP equivalent
- `architecture/mcp-integration.md` — protocol-level posture
- `governance/known-limitations.md` — limitations relevant to onboarding decisions
