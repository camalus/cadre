---
id: CADRE-SP-01
title: "SP-01 — Cadre Design"
version: "1.0"
type: sub-prompt
sequence: 1
input_artifacts: ["engagement-brief.yaml"]
output_artifact: "cadre-blueprint.md"
hitl_tier: 2
---

# SP-01 — Cadre Design

*Designs the agent cadre for a specific engagement. Determines which of the 20 agents are in scope, how they're configured, and which Cynefin domains each capability falls into. Output drives every subsequent prompt in the sequence.*

---

## Purpose

Most engagements do not need all 20 agents. A solo founder running a market-research-only engagement might use just VANTA (5 agents) plus minimal KEEL/PULSE (2 agents) for a 7-agent cadre. A Fortune 500 line-of-business deploying customer-facing automation might use the full 20. SP-01 produces a tailored cadre blueprint sized to the engagement scope, budget, and risk profile.

---

## Inputs

- **`engagement-brief.yaml`** — the structured intake from the operator (see P00 for required fields)
- **`workflows/tier-N.md`** — the SKU tier that defines budget and timeline envelopes
- **`readiness/methodology.md`** — for sizing decisions tied to client maturity

---

## Output

**`engagements/<id>/cadre-blueprint.md`** — the canonical cadre design document for this engagement. Contains:

1. Engagement summary (1 paragraph)
2. **Cadre roster table** — which of the 20 agents are in scope, with rationale for each
3. **Cynefin domain mapping** — for each in-scope capability, which Cynefin domain it falls into and the corresponding autonomy level
4. **HITL tier assignments** — preliminary tier-0/1/2/3 assignments per agent action (refined in SP-06)
5. **Parallelism plan** — which agents fan out, which serialize, expected concurrency
6. **Cost envelope** — projected token spend and Managed Agents session-hours by squad
7. **Out-of-scope flags** — agents explicitly NOT used and why
8. **Open questions** — items that need operator input before SP-02 can run

---

## Step-by-step

### Step 1 — Parse the engagement brief

Confirm all required fields are present. If `jurisdiction`, `sector`, or `human_reviewers` is missing, halt and request from operator. These three fields drive HITL routing and cannot be inferred safely.

### Step 2 — Determine cadre scope

Map the engagement's in-scope capabilities to squads:

- **Market research, competitive analysis, evidence synthesis** → VANTA (some or all of A01–A05)
- **Product specification, PRD, roadmap** → ATLAS (some or all of A06–A10)
- **Runtime ops, eval, incident response, cost tracking** → KEEL (some or all of A11–A15)
- **Governance, compliance, HITL routing, audit** → PULSE (some or all of A16–A20)

Some agents are non-optional regardless of scope:

- **A02 Evidence Classifier** — required for any engagement that produces external-facing claims
- **A15 Handoff Validator** — required for any multi-agent engagement
- **A17 HITL Router** — required for any engagement with external-facing actions
- **A19 Audit Logger** — required for any engagement subject to regulatory reporting

If the engagement scope excludes any of these, escalate. The exclusion may be defensible (purely internal idempotent reads) but must be documented.

### Step 3 — Map capabilities to Cynefin domains

For each in-scope capability, classify the Cynefin domain (see `architecture/cynefin-autonomy-dial.md`):

- **Clear** — best practice, single right answer (e.g., FAQ routing, structured data extraction)
- **Complicated** — good practice, range of right answers (e.g., legal analysis, financial modeling)
- **Complex** — emergent practice, retrospectively coherent (e.g., R&D, novel market entry)
- **Chaotic** — novel practice, stop-the-bleeding (e.g., crisis response, security incident)

The Cynefin domain drives autonomy level:

| Cynefin | Autonomy | Default HITL Tier |
|---|---|---|
| Clear | Full automation | 0 |
| Complicated | Expert-augmented (LLM proposes, human validates) | 1 |
| Complex | Human-led with AI probes | 2 |
| Chaotic | AI as sensing layer, human acts | 3 |

A single engagement typically spans multiple domains. Map each capability separately.

### Step 4 — Apply the read/write asymmetry rule

For each in-scope agent, classify its parallelism:

- **Parallel-safe** — pure-function reads, idempotent operations, no shared-state mutation
- **Serialized** — mutating writes, state-dependent decisions, external side effects

Override defaults only with documented justification. The default classifications in `cadre/` are the starting point.

### Step 5 — Estimate cost envelope

Token budget per agent type (from `architecture/orchestrator-worker-pattern.md`):

- VANTA (heavy parallel research) — 30–50% of total spend
- ATLAS (medium spec authoring) — 20–35% of total spend
- KEEL (continuous eval/audit) — 15–25% of total spend
- PULSE (lightweight gating) — 5–10% of total spend
- Orchestrator overhead — 10–20% of total spend

Multiply by SKU tier budget. If the projection exceeds 80% of budget, recommend reducing scope or upgrading SKU tier.

### Step 6 — Identify open questions

List any items that cannot be resolved without operator input:

- Ambiguous scope statements
- Missing human reviewers for required HITL tiers
- Sector-specific compliance obligations not yet declared
- Conflicts between in-scope capabilities and budget envelope

### Step 7 — Write `cadre-blueprint.md`

Use `templates/cadre-blueprint-template.md` as the scaffold. Persist to `engagements/<id>/cadre-blueprint.md`.

---

## Quality criteria

A passing `cadre-blueprint.md` has all of the following:

- [ ] Every in-scope agent has explicit rationale (not just "included by default")
- [ ] Every capability is mapped to exactly one Cynefin domain
- [ ] Every agent has a declared parallelism class
- [ ] Every external-facing action has a preliminary HITL tier
- [ ] Cost envelope projection is within SKU tier budget
- [ ] Out-of-scope agents are listed with justification
- [ ] Open questions are surfaced (or "none" stated explicitly)

---

## Common failure modes

- **Including all 20 agents by default.** Default is to exclude. Each inclusion requires justification.
- **Skipping Cynefin classification on "obvious" tasks.** What looks Clear from outside often turns out to be Complex once you map the actual decisions. Spend the time.
- **Defaulting parallelism class to "parallel-safe" without checking.** A07 Spec Decomposer looks parallel-safe but isn't if multiple specs are being decomposed against the same shared roadmap. Check the task shape, not just the agent.
- **Hand-waving the cost envelope.** Use real per-million-token numbers from `architecture/`. "Roughly $X" is not an envelope.

---

## Citations

- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025. (Token cost ratios; squad sizing)
- Snowden, D. & Boone, M. *A Leader's Framework for Decision Making.* HBR, November 2007. (Cynefin domains)
- Anthropic API pricing (Opus 4.6 $5/$25 per M; Sonnet 4.6 $3/$15 per M; Managed Agents $0.08/session-hour) as of April 2026.

---

*BHIL CADRE Framework — SP-01 — v1.0.0*
