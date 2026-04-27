# MCP Server Onboarding

*The process for taking an MCP server from "candidate for connection" to "in the engagement's active allowlist." Onboarding is intentionally rigorous; the cost of insufficiently vetted server connections is paid in incidents.*

---

## When this process applies

Apply this process when:

- A new MCP server is proposed for an engagement that does not currently use it
- An existing engagement's MCP server is being upgraded to a major version
- An MCP server's authentication, scope, or trust posture changes materially
- A server was previously connected at one trust tier and is being considered for a higher tier

The process does not apply to routine version updates that do not change the security posture; those follow the operator's standard change-management procedure.

---

## Step 1 — Candidate intake

The proposer (engagement lead or designated technical owner) prepares an intake artifact at `engagements/<id>/integration/mcp-candidates/<server-slug>.md` covering:

- **Server identity.** Vendor, server name, version, deployment model (SaaS, self-hosted, hybrid)
- **Capabilities being requested.** Which specific tools or resources will be used; this is the basis for the per-tool allowlist
- **Authentication.** OAuth 2.1 conformance status; supported scopes
- **RFC 8707 conformance.** Whether the server correctly implements Resource Indicators
- **Data flow.** What data the cadre would send to the server; what data the cadre would receive; whether the server stores data
- **Vendor security posture.** Any third-party security attestations (SOC 2, ISO 27001, sector-specific certifications)
- **Operator's existing relationship.** Whether the operator already uses the vendor for non-cadre purposes; existing contractual posture

The intake artifact is the basis for trust-tier assignment and is itself an audit chain entry.

---

## Step 2 — Trust-tier assignment

Trust tiers map to the architecture document (`architecture/mcp-integration.md`). The candidate is provisionally assigned a tier:

- **Tier I (highest trust):** Operator-owned servers, or servers from vendors with a current BAA/DPA and a strong attestation record, with full RFC 8707 conformance
- **Tier II (standard trust):** Vendors with adequate attestation and full RFC 8707 conformance, no special operator relationship
- **Tier III (limited trust):** Vendors with full RFC 8707 conformance but limited attestation, or strong attestation but limited operational track record
- **Tier IV (compensated trust):** Servers without RFC 8707 conformance, requiring documented compensating controls per `governance/known-limitations.md`

Tier assignment is provisional until the conformance verification (Step 3) and trial operation (Step 5) are complete.

---

## Step 3 — Conformance verification

The cadre runs an automated conformance check:

- **OAuth 2.1.** Authorization Code with PKCE flow completes; refresh tokens behave per spec; scope downgrade is honored
- **RFC 8707.** Resource indicator presence is enforced server-side; tokens issued for one resource are rejected when presented to another resource
- **MCP protocol revision.** Server speaks revision 2025-11-25 (or operator-approved alternative); async Tasks behave per spec; URL Mode Elicitation behaves per spec where used [VERIFIED — MCP specification revision 2025-11-25]
- **TLS posture.** Modern TLS configuration; certificate chain validates; HSTS or equivalent

Failures at this step block onboarding at the assigned tier. The candidate may be reconsidered at a lower tier (Tier IV with compensating controls) if the failure can be compensated and the operator accepts the residual risk.

The conformance verification produces a structured report stored at `engagements/<id>/integration/mcp-candidates/<server-slug>-conformance.json`.

---

## Step 4 — Allowlist construction

The per-tool allowlist is constructed from the intake's "capabilities being requested" section. The principle: explicit allowlists, no broad allowlists. Each entry specifies:

- The tool name (server-side)
- The permitted operation (read, write, side-effect-producing)
- The agent(s) authorized to invoke
- The HITL tier required (per `governance/hitl-policy.md`)
- The audit emission requirement (per `governance/audit-chain-spec.md`)

Allowlists are reviewed at Tier 2 minimum. Allowlists that authorize side-effect-producing tools are reviewed at Tier 3.

---

## Step 5 — Trial operation

Before full onboarding, the server runs in a constrained trial mode:

- A non-production engagement (or a sandboxed slice of a production engagement) uses the server
- A12 audits every interaction with elevated sampling (effectively 100% during trial)
- A14 records cost behavior; anomalous spend triggers escalation
- A13 monitors for incident indicators

Trial duration is operator-determined; defaults are 1–2 weeks for Tier II, 2–4 weeks for Tier III, 4+ weeks for Tier IV.

Trial completion produces a trial report covering:

- Operational behavior (latency, error rate, scope compliance)
- Cost behavior (per-call cost, total trial spend)
- Audit findings during trial
- Any incidents or near-misses
- Recommendation: proceed at provisional tier, downgrade tier, or block onboarding

---

## Step 6 — Onboarding decision

The onboarding decision is a Tier 2 decision (Tier 3 for Tier IV servers). The decision is recorded in the chain and references the intake, the conformance report, the allowlist, and the trial report.

Approved onboarding adds the server to the engagement's active allowlist. The chain entry is the canonical record; subsequent operator-side configuration (credential storage, network rules) follows operator IT procedures.

Approved onboarding includes:

- The trust tier (final, post-trial)
- The allowlist
- The HITL tier defaults per allowed action
- The audit emission requirements
- The reauthorization cadence (when the onboarding decision must be revisited; default 12 months)

---

## Step 7 — Catalog update

The framework-level catalog (`integration/mcp-server-catalog.md`) is updated when the onboarded server is one not previously catalogued. This update goes through the framework's standard change discipline, not through the engagement's own audit chain.

Catalog entries record only engagement-agnostic information: the server's identity, the protocol conformance status, and the framework-default trust tier. Operator-specific configuration stays in the operator's records.

---

## Failure modes

- **Conformance verification fails.** The candidate is rejected at the requested tier. Either re-propose at a lower tier with compensating controls, or do not onboard. Do not paper over conformance gaps with ad-hoc workarounds.
- **Trial reveals incidents.** The trial report records the incidents; onboarding decision considers whether the incidents are blocking. Persistent or severity-1 incidents during trial are blocking.
- **Allowlist creep.** Capabilities requested expand beyond intake during trial. The onboarding decision must reflect the actual allowlist; any expansion is a new intake.
- **Reauthorization missed.** An onboarded server whose reauthorization date passes without review is automatically suspended from the active allowlist; further use requires a fresh decision.

---

## Audit emissions

- Intake artifact (Tier 1)
- Conformance report (Tier 1)
- Allowlist publication (Tier 2)
- Trial start (Tier 1)
- Trial conclusion and report (Tier 2)
- Onboarding decision (Tier 2 or Tier 3)
- Catalog update (Tier 2, framework scope)

---

## Cross-references

- `architecture/mcp-integration.md` — protocol-level architecture
- `integration/mcp-server-catalog.md` — framework-level catalog
- `integration/external-tool-allowlist.md` — non-MCP equivalent
- `governance/known-limitations.md` — RFC 8707 absent operators, compensating controls
- `governance/hitl-policy.md` — tier model invoked here
- `governance/audit-chain-spec.md` — chain emissions
