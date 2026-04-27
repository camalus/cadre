---
id: CADRE-SP-09
title: "SP-09 — Readiness Diagnostic (Commercial Wedge)"
version: "1.0"
type: sub-prompt
sequence: 9
input_artifacts: ["engagement-brief.yaml", "readiness/methodology.md"]
output_artifact: "diagnostic-report.md"
hitl_tier: 2
sku_tier: "tier-2"
price_range_usd: [4500, 7500]
duration: "1 day (8 working hours)"
---

# SP-09 — Readiness Diagnostic (Commercial Wedge)

*The single most commercially important prompt in the CADRE sequence. SP-09 is the $4,500–$7,500 one-day diagnostic that opens the engagement door and converts into a $5K–$30K/month Cadre Operator retainer. It defeats both the "free envisioning workshop" commodity trap and the Big-4 $75K–$250K ISO pre-cert gate.*

---

## Purpose

SP-09 produces a **Readiness Diagnostic Report** for a prospective client. The report scores the client on the 7-dimension CADRE readiness rubric, recommends a tailored cadre blueprint sized to the client's maturity and budget, identifies the highest-leverage near-term interventions, and quotes a specific Sprint engagement (Tier 3) with 100% diagnostic credit applied.

The diagnostic is paid ($4,500–$7,500), one-day, and stands alone as a deliverable. The client may walk away with the report and never engage further; that is acceptable. The conversion target is ~30% diagnostic-to-Sprint based on benchmarks for analogous fractional-CDO engagements.

---

## Inputs

- **Client intake form** completed pre-engagement
- **2-hour discovery interview** with named client stakeholder (CEO, CTO, COO, or Chief AI Officer)
- **Document review** of any client-supplied materials (org charts, current AI initiatives, governance docs, prior assessments)
- **`readiness/methodology.md`** — the 7-dimension scoring methodology
- **`readiness/d1-data-infrastructure.md`** through **`readiness/d7-hitl-governance.md`** — per-dimension rubrics
- **`workflows/tier-2-readiness-diagnostic.md`** — the operational workflow

---

## Output

**`engagements/<id>/diagnostic-report.md`** — the deliverable, branded per `bhil-docx` skill if delivered as a Word document. Standard sections:

1. **Executive summary** (1 page) — overall readiness verdict, top 3 findings, recommended next step
2. **7-dimension readiness scorecard** — score and rationale per dimension, with composite
3. **Recommended cadre blueprint** — which agents and squads to deploy, sized to maturity
4. **Critical-path interventions** — top 3–5 highest-leverage moves the client should make in the next 90 days
5. **Risk register** — material risks (regulatory, operational, reputational) and mitigations
6. **Sprint quote** — specific Tier-3 Readiness Sprint engagement with deliverables, timeline, price, and 100% diagnostic credit applied
7. **Companion framework recommendations** — which BHIL companion frameworks (PATHFINDER, AXIOM, VERDICT, NEXUS, PRD/MVP) would compound value
8. **Methodology and citations** — how the assessment was conducted; primary sources

---

## The 7 readiness dimensions (canonical reference)

| # | Dimension | Question it answers |
|---|---|---|
| **D1** | Data infrastructure | Does the client have data the cadre can actually read? |
| **D2** | Team AI literacy | Can the humans approve, oversee, and override agent output? |
| **D3** | Process maturity | Are the workflows the cadre would touch documented and stable? |
| **D4** | Compliance posture | Where does the client sit on EU AI Act / NIST / ISO 42001 / sector regs? |
| **D5** | Tooling stack | Does the client have the runtime (Anthropic, MCP, observability) provisioned? |
| **D6** | Integration readiness | Can the cadre talk to the client's existing systems via MCP or APIs? |
| **D7** | HITL governance | Are reviewers named, trained, and resourced for Tier 1+ gates? |

Each dimension scores 1–5:

- **1 — Absent**: dimension is missing entirely; cadre cannot deploy without remediation
- **2 — Nascent**: foundations exist but inconsistent or undocumented
- **3 — Developing**: documented in some areas; gaps present but addressable
- **4 — Mature**: well-documented, consistently applied, gaps are minor
- **5 — Excellent**: industry-leading; ready for advanced cadre patterns

Composite score is the weighted average; weights vary by SKU tier and client size (see `readiness/scoring-rubric.md`).

---

## Step-by-step (one-day delivery)

### Hour 0 — Pre-arrival (asynchronous)

Before the on-site or video day, the client completes the intake form and supplies:

- Org chart (executives + AI/data team)
- Current AI/automation initiatives list
- Any existing governance documents (AI policy, data classification, security policies)
- Recent compliance assessments (if any)
- A representative process flow the client wants the cadre to touch

The BHIL operator reviews these materials and pre-populates draft scores for the dimensions where the documentation answers the question.

### Hour 1–2 — Discovery interview

90-minute structured interview with the named stakeholder. Topics:

- Strategic intent: what business outcome justifies the cadre?
- Risk tolerance: what's the worst-case outcome the client can tolerate?
- Reviewer availability: who can play the Tier 1, 2, 3 roles?
- Current pain: which decisions are bottlenecking today?
- Data: what does the client actually have, where, in what shape?
- Compliance: which regulatory regimes apply?
- Timeline: when does the client need value?

### Hour 3–4 — Score the 7 dimensions

Working from the discovery interview and the supplied materials, score each dimension. For each score, capture:

- Score (1–5)
- Evidence — what the client said or what the documents show
- Rationale — why this score and not the adjacent ones
- Critical gap — the single most important thing missing at this score

### Hour 5 — Recommend cadre blueprint

From the dimension scores, compute the recommended cadre blueprint:

- **If composite score < 2.5**: recommend deferring cadre deployment; client needs foundational work first (typically PATHFINDER for D2, NEXUS for D1, AXIOM for D4)
- **If composite score 2.5–3.0**: recommend a minimal 5–7 agent cadre focused on VANTA + minimal KEEL/PULSE; defer ATLAS until D3 improves
- **If composite score 3.0–4.0**: recommend a tailored 10–15 agent cadre; full VANTA + ATLAS + appropriate KEEL/PULSE
- **If composite score > 4.0**: recommend the full 20-agent cadre with advanced patterns (cross-engagement memory, async Tasks, Cynefin-keyed autonomy presets)

### Hour 6 — Identify critical-path interventions

The 3–5 highest-leverage moves the client should make in the next 90 days. These are the actionable findings that justify the diagnostic price. Each intervention includes:

- The dimension it addresses
- The specific action
- Estimated effort (person-weeks or dollars)
- Expected impact on dimension score

### Hour 7 — Risk register

Material risks discovered during the assessment, especially:

- **Regulatory risk** — gaps to EU AI Act / NIST / ISO 42001 / sector regs
- **Operational risk** — single points of failure, missing reviewers, unmonitored systems
- **Reputational risk** — patterns that resemble Air Canada / iTutor / Klarna failures
- **Vendor risk** — dependence on vendors with weak ROI evidence (flag UNCORROBORATED metrics)

For each risk, name an owner and a mitigation timeframe.

### Hour 8 — Sprint quote and report assembly

Quote a specific **Tier-3 Readiness Sprint** engagement. Standard Sprint:

- 2–4 weeks
- Addresses the top 3 critical-path interventions
- Produces a deployment-ready cadre blueprint and pilot
- Price: $25,000–$60,000 (varies by intervention scope)
- **100% of the diagnostic price ($4,500–$7,500) is credited toward the Sprint price** — this is the wedge that converts.

Assemble all sections into `diagnostic-report.md`. If the client requested a Word deliverable, render through the `bhil-docx` skill with BHIL branding (cobalt blue `#1B4FD8` / dark navy `#1C1C2E`).

---

## Pricing logic

Why $4,500–$7,500 and not $0 (free) or $25,000+ (Big-4 territory)?

- **$0 (free workshop)** — competes against every ISV's lead-gen workshop. Commoditizes the diagnostic. Selects for clients who don't value the work.
- **$25K+ (Big-4 ISO pre-cert)** — too high for a one-day deliverable; clients expect multi-week scope at that price. Doesn't fit the "fast paid validation" entry pattern.
- **$4,500–$7,500** — high enough that the client must commit, low enough that it's a non-friction decision for any company that's serious about AI deployment. Equivalent to one BHIL day-rate. Defensible.

The 100% credit toward Sprint is the conversion mechanism. Clients who walk away keep the report; clients who continue lose nothing in net cost. Estimated 30% conversion on available benchmarks.

---

## Quality criteria

- [ ] All 7 dimensions are scored with evidence and rationale
- [ ] Composite score is calculated per the rubric
- [ ] Recommended cadre blueprint matches the composite score range
- [ ] At least 3 critical-path interventions, each with effort and expected impact
- [ ] Risk register includes regulatory, operational, reputational, vendor risk categories
- [ ] Sprint quote is specific: scope, deliverables, timeline, price, credit applied
- [ ] Companion framework recommendations are tailored (not generic "consider PATHFINDER")
- [ ] Methodology section cites the 7-dimension rubric and primary sources
- [ ] Total document length: 12–20 pages (long enough to defend, short enough to read)

---

## Common failure modes

- **Score inflation to flatter the prospect.** A client at composite 2.0 deserves to hear it. Don't score them at 3.5 to make them feel ready. The Klarna pattern — declaring readiness and reversing within a year — is what happens when diagnostics are flattering instead of accurate.
- **Generic recommendations.** "Consider improving your data infrastructure" is not a recommendation. "Migrate the X dataset from Y to Z within 6 weeks; estimated effort $40K; D1 score moves from 2 to 3.5" is.
- **No Sprint quote.** Half the value is the conversion path. The Sprint quote is mandatory.
- **No critical-path interventions tied to dimension scores.** Each intervention must explicitly improve one or more dimensions.
- **Risk register that lists everything.** If everything is a risk, nothing is. Top 5–10 material risks.
- **Vendor-published ROI metrics presented as VERIFIED.** Rakuten, Decagon, Glean, Klarna — all UNCORROBORATED. Cite with vendor attribution.

---

## What good looks like

A finished SP-09 deliverable should be the kind of document a CFO would forward to a CEO with the line "this is the most useful AI assessment I've seen." Specific, evidence-backed, with named numbers and named next steps. Not flattering, not catastrophizing — calibrated.

The example engagement in `examples/sample-engagement/` is a reference implementation. Read it before you deliver your first diagnostic.

---

## Citations

- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025.
- BHIL framework portfolio: PATHFINDER, AXIOM, VERDICT, NEXUS, PRD/MVP, LOCUS, MERIDIAN, SENTINEL, VANTAGE, CODEX.
- Prosci ADKAR research, n=679 organizations (Awareness and Desire as primary change-management barriers).
- Snowden, D. & Boone, M. *A Leader's Framework for Decision Making.* HBR, November 2007.
- Moffatt v. Air Canada, 2024 BCCRT 149 (operator liability for agent output).
- iTutor Group EEOC settlement, 2023 (~$365,000).
- Klarna AI deployment reversal, 2025 (CEO Bloomberg interview May 2025; CMSWire reframing May 20, 2025).

---

*BHIL CADRE Framework — SP-09 — v1.0.0 — The Commercial Wedge*
