---
id: CADRE-SP-10
title: "SP-10 — Companion Bundle"
version: "1.0"
type: sub-prompt
sequence: 10
input_artifacts: ["diagnostic-report.md", "cadre-blueprint.md"]
output_artifact: "bundle-recommendation.md"
hitl_tier: 1
sku_tier_minimum: "tier-3"
---

# SP-10 — Companion Bundle

*Recommends the BHIL companion frameworks (PATHFINDER, AXIOM, VERDICT, NEXUS, PRD/MVP) that compound CADRE's value for a specific client. Outputs `bundle-recommendation.md`. Routinely run as part of Tier-3 (Sprint), Tier-4 (Cadre Operator), and Tier-5 (Enterprise) engagements; optional add-on to Tier-2 (Diagnostic).*

---

## Purpose

CADRE is the anchor framework, but it does not solve every problem a client has. The other BHIL frameworks address adjacent problems — AI literacy in the humans who supervise agents, governance overlay for regulatory exposure, research integrity discipline applied beyond the cadre, the data substrate the cadre reads from, and the product delivery cadence the cadre feeds. SP-10 is the synthesis prompt that maps the client's diagnostic findings onto the companion framework portfolio and produces a tailored multi-framework retainer recommendation.

The economic argument: a single-framework retainer is replaceable. A three- or four-framework retainer is not. Bundled engagements are stickier, deliver more compound value per dollar, and produce the kind of multi-year relationships that justify BHIL's positioning.

---

## Inputs

- **`engagements/<id>/diagnostic-report.md`** — the SP-09 output (or equivalent for non-Diagnostic engagements)
- **`engagements/<id>/cadre-blueprint.md`** — the cadre design from SP-01
- **`integration/companion-pathfinder.md`** through **`integration/companion-prd-mvp.md`** — the companion framework specs
- **`workflows/`** — pricing for each framework

---

## Output

**`engagements/<id>/bundle-recommendation.md`** — the canonical bundle recommendation. Contents:

1. **Bundle thesis** (1 paragraph) — why this client gets compound value from a multi-framework engagement
2. **Recommended frameworks** — which companions, ranked by leverage
3. **Per-framework rationale** — for each recommended framework, the specific dimension scores or risk register items it addresses
4. **Sequencing plan** — which framework leads, which follow, on what cadence
5. **Combined retainer pricing** — all-in monthly cost vs. à-la-carte
6. **Anti-recommendations** — frameworks explicitly NOT recommended for this client and why
7. **Decision criteria** — what would change the recommendation (if D2 improves, drop PATHFINDER; if a new regulator enters scope, add AXIOM)

---

## The five companion frameworks (canonical reference)

### PATHFINDER — AI Literacy

**What it is**: A structured curriculum that brings the humans who supervise AI agents up to the literacy level required to do that supervision well. Solves the Prosci ADKAR "Awareness" and "Desire" barriers (the two largest barriers to organizational change per the Prosci n=679 study).

**Pair with CADRE when**: D2 (Team AI Literacy) scores ≤ 3.0 on the 7-dimension rubric. Without PATHFINDER, the named HITL reviewers can't perform Tier 2+ reviews competently — they're either rubber-stamping or over-rejecting, both of which defeat the gate.

**Typical bundle position**: PATHFINDER runs first or in parallel with CADRE Sprint. The cadre cannot go to full production without trained reviewers.

**Rough pricing**: $8K–$25K depending on cohort size and depth.

---

### AXIOM — AI Governance Overlay

**What it is**: Operationalizes EU AI Act, NIST AI RMF, ISO 42001, and sector-specific obligations into a working governance program. Document templates, audit cadences, named-role assignments, and the cross-walk between regulator-facing reporting and engineering practice.

**Pair with CADRE when**: D4 (Compliance Posture) scores ≤ 3.0, OR client operates in a high-risk sector (healthcare, finance, hiring, biometric, EU deployment), OR the client has a stated compliance milestone (ISO 42001 certification, EU AI Act conformity, internal audit readiness).

**Typical bundle position**: AXIOM runs concurrent with CADRE deployment. AXIOM produces the governance documentation that CADRE's PULSE squad enforces at runtime.

**Rough pricing**: $15K–$40K per quarter; ongoing retainer typical.

---

### VERDICT — Research Integrity

**What it is**: Evidence classification discipline (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE) applied to the client's research, content, and analysis workflows. Trains analysts on primary-source weighting, source archival, and inference flagging. The discipline that drives A02 (Evidence Classifier) inside the cadre, extended outward to the rest of the organization.

**Pair with CADRE when**: Client produces a lot of research-driven content (analyst reports, market intelligence, competitive briefs, due diligence), OR client has been burned by hallucination or unsourced AI output, OR client is in a fiduciary or regulated communication context (investment research, journalism, legal opinion).

**Typical bundle position**: VERDICT runs in parallel with the VANTA squad of the cadre — they reinforce each other. Cadre artifacts are VERDICT-classified; VERDICT-trained analysts review cadre output more competently.

**Rough pricing**: $10K–$30K initial training plus retainer for ongoing review.

---

### NEXUS — Data Universe

**What it is**: A single-source-of-truth substrate that feeds both human analytics and agent retrieval layers. Data classification, lineage tracking, residency mapping, and the API surface that MCP servers and human dashboards both consume.

**Pair with CADRE when**: D1 (Data Infrastructure) scores ≤ 2.5, OR the client has multiple parallel data systems with no canonical truth, OR the cadre's MCP integration (SP-04) cannot be configured cleanly because the underlying data is fragmented.

**Typical bundle position**: NEXUS runs **before** CADRE. The cadre cannot deploy effectively against a fragmented data substrate. NEXUS often pulls in PRD/MVP for the API design.

**Rough pricing**: $30K–$150K depending on data complexity; long-tail engagement.

---

### PRD/MVP — Product Delivery Cadence

**What it is**: RICE prioritization, Opportunity Solution Trees, North Star Metric, and a working cadence for moving from research to spec to ship. Feeds directly into the ATLAS squad of the cadre.

**Pair with CADRE when**: D3 (Process Maturity) scores ≤ 3.0 AND the client wants ATLAS in scope, OR the client has a stated product delivery problem (slow-to-ship, low spec quality, weak prioritization), OR the client is a startup or scale-up where product cadence is foundational.

**Typical bundle position**: PRD/MVP runs in parallel with ATLAS deployment. The cadre's PRD Author (A06), Spec Decomposer (A07), and Roadmap Mapper (A09) all assume PRD/MVP-grade input.

**Rough pricing**: $8K–$30K initial install plus retainer for product reviews.

---

## Step-by-step

### Step 1 — Read the diagnostic findings

Pull the dimension scores and risk register from `diagnostic-report.md`. Map each low score (≤ 3.0) to the relevant companion framework using the rubric above.

### Step 2 — Identify hard pre-requisites

Some bundles have pre-requisite ordering:

- If D1 < 2.5, NEXUS must run before CADRE (or before any cadre subagent that reads the data)
- If D2 < 2.5, PATHFINDER must run before any Tier 2+ HITL gate goes live
- If D4 < 2.5 in a high-risk sector, AXIOM must run before any external-facing cadre action

Hard pre-requisites become "Phase 1" of the recommendation. Other recommendations are "Phase 2" or run in parallel.

### Step 3 — Identify high-leverage parallels

Some bundles compound when run together:

- VANTA + VERDICT — research squad benefits massively from organization-wide evidence classification discipline
- ATLAS + PRD/MVP — product squad benefits from upstream product-cadence improvements
- PULSE + AXIOM — governance squad enforces what AXIOM documents

Recommend these as parallel engagements when the diagnostic supports them.

### Step 4 — Identify anti-recommendations

Some clients should explicitly NOT bundle. Cases:

- Client at composite readiness > 4.0 — usually doesn't need PATHFINDER (D2 is already high)
- Client with mature ISO 27001/SOC 2 program but no AI-specific exposure — AXIOM may be overkill; lighter-touch governance review might suffice
- Client without any product delivery in scope (pure analytics shop) — PRD/MVP is irrelevant; recommend deferring it
- Client in shadow-mode evaluation only (Tier-2 Diagnostic only, no Sprint) — companion bundle recommendations are advisory but not actionable until the Sprint

Document the anti-recommendations so the client sees the framework was applied with discrimination, not as a sales pitch for everything.

### Step 5 — Compute combined retainer pricing

Single-framework retainer pricing applies. Combined retainers get a coherence discount (typically 10–15%) reflecting reduced cross-framework overhead. Document both:

- Per-framework à-la-carte pricing
- Bundle pricing with discount applied
- Net difference

### Step 6 — Define decision criteria

What would change the recommendation? Document the conditions:

- "If D2 score improves to ≥ 4 within 6 months, PATHFINDER can be ramped down to maintenance mode"
- "If a new regulator (e.g., FDA premarket clearance for clinical AI) enters scope, AXIOM expands"
- "If a new product line enters scope, PRD/MVP expands"

The decision criteria turn the recommendation into a living document.

### Step 7 — Write `bundle-recommendation.md`

Use `templates/bundle-recommendation-template.md` as the scaffold. Persist to `engagements/<id>/bundle-recommendation.md`.

---

## Quality criteria

- [ ] Every recommended framework has a specific dimension score or risk register item driving it
- [ ] Hard pre-requisites are sequenced explicitly (Phase 1 / Phase 2 / parallel)
- [ ] At least one anti-recommendation (or explicit "all five frameworks are warranted" with justification)
- [ ] Combined pricing shown alongside à-la-carte
- [ ] Decision criteria document what would change the recommendation
- [ ] Bundle thesis is one paragraph (not a sales pitch; an analytical conclusion)

---

## Common failure modes

- **"All five frameworks for everyone."** This is a sales pitch, not a recommendation. Most clients warrant 2–3 companions, not all 5.
- **Sequencing recommendations without pre-requisites.** "Do PATHFINDER and CADRE in parallel" is fine; "do NEXUS and CADRE in parallel when D1 < 2.5" is wrong because the cadre will fail without the data substrate.
- **Pricing without justification.** "$30K–$80K bundle" without showing how that breaks down is opaque. Show the math.
- **No anti-recommendations.** A recommendation that recommends everything has demonstrated nothing. Discrimination is the proof of judgment.
- **No decision criteria.** Recommendations without decision criteria are time-locked. Document what would change them.

---

## Companion-bundle case study patterns

**The healthtech startup pattern** (D1=2, D2=2, D4=2, sector=healthcare):
NEXUS → PATHFINDER → AXIOM → CADRE (smaller cadre, VANTA + minimal PULSE). Heavy front-loading; CADRE comes last because the foundations aren't ready.

**The regulated-finance pattern** (D1=4, D2=3, D4=3, sector=finance):
AXIOM (concurrent) + CADRE (full) + VERDICT (concurrent). Already has data; needs governance overlay and research integrity discipline running alongside cadre deployment.

**The mid-market scale-up pattern** (D1=3, D2=3, D3=2, D4=3):
PRD/MVP → CADRE (with ATLAS) + PATHFINDER (concurrent). Product cadence is the bottleneck; cadre amplifies once cadence is in place.

**The mature enterprise pattern** (D1=4, D2=4, D3=4, D4=4):
CADRE (full 20-agent) + AXIOM (lighter-touch ongoing) only. Already mature; doesn't need PATHFINDER or VERDICT remediation.

**The sole-founder pattern** (D1=2, D2=4, D3=2, D4=2):
Light NEXUS + minimal CADRE (VANTA + PULSE only). Founder is AI-literate (D2 high); needs data substrate and tight cadre, no broader org-change frameworks.

---

## Citations

- BHIL framework portfolio documentation (PATHFINDER, AXIOM, VERDICT, NEXUS, PRD/MVP).
- Prosci ADKAR research, n=679 organizations.
- Reichheld, F. *The Loyalty Effect.* Harvard Business Press, 1996. (Customer-tenure economics; source of the multi-framework retainer thesis.)
- BHIL internal: `integration/` folder for per-framework pairing details.

---

*BHIL CADRE Framework — SP-10 — v1.0.0 — Bundle Synthesis*
