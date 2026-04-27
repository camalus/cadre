# Workflow: New Engagement Startup

*From signed engagement letter to operating cadre. The workflow takes a confirmed engagement and produces the engagement directory, the charter, the cadre composition, and the readiness baseline. Start condition: signed agreement. Exit condition: cadre operational on first deliverable scope.*

---

## Owner and reviewers

- **Owner:** Engagement lead (operator-side); orchestrator agent (cadre-side)
- **Tier 2 reviewers:** Operator's compliance officer (sign-off on charter, allowlists, reviewer roster); operator's engagement sponsor (scope confirmation)
- **Tier 3 reviewers:** Required when sector triggers (healthcare PHI, banking model risk, EU high-risk AI Act categorization) apply

---

## Phase 1 — Intake (Day 0 to Day 1)

The engagement-letter scope is converted into a structured intake artifact. The intake captures:

- Operator identity, deployment target, and sector classification
- Use-case description, including consequential decisions in scope
- Data inventory at the level of class (e.g., "customer support tickets," "loan-application records") and sensitivity classification
- Jurisdiction footprint (EU, US states, UK, etc.)
- Regulatory triggers identified by intake (HIPAA, GDPR, EU AI Act category, NYC LL 144, Colorado SB24-205, sector-specific)
- Existing AI governance posture, including any pre-existing risk registers or policies the cadre must integrate with
- Reviewer roster availability across required jurisdiction/sector/role/load attributes

The intake artifact is written to `engagements/<id>/intake/` and is the first audit chain entry under the engagement ID. The engagement ID is assigned by the operator's engagement-management system and is opaque to the cadre.

If the readiness diagnostic (SP-09) has been performed for this operator, its dossier is referenced here. If not, the intake captures whether a diagnostic is in scope or whether the engagement is proceeding without one (and if so, the rationale and the heightened review posture).

---

## Phase 2 — Scoping and charter (Day 1 to Day 3)

The intake feeds the charter. The charter is the authoritative document that defines what the cadre will do, what it will not do, and how decisions get made. It is reviewed at Tier 2 minimum.

Charter sections:

- **Scope.** What deliverables, what cadence, what success criteria
- **Out of scope.** Explicit exclusions to prevent scope creep
- **Cadre composition.** Which of A01–A20 are activated for this engagement; which are deactivated; which are augmented with operator-supplied custom agents
- **HITL configuration.** Tier defaults per action class; reviewer roster mapped to engagement; SLO commitments
- **Memory configuration.** Per-engagement memory location (always `engagements/<id>/memory/`); cross-engagement learnings access policy; sanitization policy for any future promotions
- **Allowlists.** MCP servers (with trust tier per server); model variants (Opus/Sonnet/Haiku assignments per agent); external tools beyond MCP
- **Audit configuration.** Chain storage location; retention horizon; verification cadence; external anchoring (if any)
- **Cost ceiling.** Operator-set ceiling triggering A14 escalation; emergency-stop authority
- **Termination conditions.** Exit triggers, both planned (engagement complete) and unplanned (operator decision, regulatory finding, cadre incident)

The template for the charter lives in `templates/engagement-charter-template.md`. The completed charter is signed by the engagement lead, the compliance officer, and (where applicable) the Tier 3 reviewers, and stored at `engagements/<id>/charter.md`.

---

## Phase 3 — Cadre composition (Day 3 to Day 5)

Per the charter, the orchestrator activates the agent set, configures allowlists, instantiates handoff contracts, and connects to the approved MCP servers. The composition step produces:

- An `engagements/<id>/cadre/` directory mirroring the relevant subset of `cadre/`
- An `engagements/<id>/contracts/` directory with the engagement-specific handoff schemas (which may extend the framework defaults but never relax them)
- An `engagements/<id>/allowlists/` directory with MCP-server, tool, and model allowlists
- A connection-test report verifying every MCP server in the allowlist is reachable, RFC 8707 conformance is verified (or the documented opt-in is in place), and authentication flows complete cleanly

Composition concludes with an end-to-end smoke test: a synthetic input flows through the cadre's full handoff chain, producing a synthetic deliverable. The smoke test exercises the eval harness (SP-07) on the engagement's specific inputs and confirms that A11 and A12 produce expected outputs.

---

## Phase 4 — Readiness baseline (Day 5 to Day 7)

Before live operation, the cadre establishes a readiness baseline that future cycles can be measured against:

- A11 runs the full eval suite and records baseline metrics
- A12 performs a baseline audit of the smoke-test traces
- A14 records baseline cost-per-deliverable for SKU verification
- A20 performs a baseline regulatory-mapping pass against the engagement's jurisdiction/sector configuration and produces the per-engagement risk register

The baseline artifacts are stored at `engagements/<id>/baseline/` and are referenced by every subsequent weekly cadence cycle. Drift from baseline beyond declared thresholds is itself a signal that A12 surfaces.

---

## Phase 5 — Go-live and handoff to weekly cadence

The engagement transitions to live operation. The orchestrator emits a chain entry recording the go-live event, the charter signatures, the baseline metrics, and the SLO commitments. Subsequent operation is governed by the weekly cadence workflow.

The first weekly cadence cycle (see `workflows/weekly-cadence.md`) begins on the operator's calendar week boundary following go-live, regardless of where in the week go-live occurred.

---

## Failure modes

- **Charter ambiguity.** When intake does not produce a clean scope, the engagement does not proceed to composition. The fix is more intake, not more charter.
- **Reviewer roster gap.** When required roster coverage is missing, the engagement does not go live. The fix is roster augmentation (operator hires or engages external reviewers); the cadre does not paper over the gap.
- **MCP server non-conformance discovered at composition.** Either the operator opts into the documented compensating controls (per `governance/known-limitations.md`) or the server is removed from the allowlist. The cadre does not silently proceed with non-conformant servers.
- **Smoke test failure.** Composition does not exit until smoke tests pass. The fix is to address the underlying issue (typically a contract mismatch or a misconfigured allowlist), not to bypass the test.

---

## Audit emissions

Every phase produces audit chain entries:

- Intake artifact creation (Tier 1)
- Charter signatures (Tier 2 or Tier 3 per sector)
- Allowlist publications (Tier 2)
- Smoke test outcomes (Tier 1)
- Baseline metrics (Tier 1)
- Go-live (Tier 2)

The full startup chain is reconstructable from the engagement's chain segment.

---

## Cross-references

- `prompts/SP-09-readiness-diagnostic.md` — input when a diagnostic was performed
- `prompts/SP-08-deployment-runbook.md` — covers the deployment mechanics within this workflow
- `templates/engagement-charter-template.md` — the charter skeleton
- `governance/hitl-policy.md` — tier model invoked here
- `workflows/weekly-cadence.md` — the workflow that takes over at go-live
