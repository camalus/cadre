# Diagnostic Day Runbook

*The hour-by-hour structure of the 8-hour Readiness Diagnostic. This runbook is what the consultant follows on the day. Operators see a summary version in their pre-engagement packet (see `pricing-packaging.md`).*

---

## Pre-day prep (0.5 hour, day before)

The consultant arrives at the diagnostic day already prepared:

- Pre-engagement questionnaire returned by operator (use cases under consideration, known data substrate, current integrations, governance posture, executive sponsor name)
- Operator's recent AI announcements, press, regulatory filings — light VANTA-style scan, ~30 minutes
- Working folder set up at `engagements/<engagement_id>/` with brief.md, intake.md, and the rubric template

This prep is included in the diagnostic fee; it is not billed separately.

---

## Hour 1 — Intake and framing (with stakeholders)

**Attendees:** executive sponsor, technical lead, one representative from a candidate use-case team. Compliance/legal optional but recommended.

**Agenda:**
- Consultant frames the day: "We're going to score 7 dimensions, not pitch a project."
- Operator walks through current AI activity (existing pilots, vendors, internal builds)
- Consultant captures candidate use cases on a working board
- Operator names 1–2 critical-path constraints (e.g., HIPAA, EU residency, board-level skepticism)

**Output:** `intake-notes.md` artifact in the engagement folder. Audit-chain entry through A19.

---

## Hour 2 — Use-case clarity + data substrate (Dimensions 1, 2)

**Attendees:** technical lead, data owner.

**Agenda:**
- For each candidate use case from Hour 1, score Dimension 1 against the rubric
- Walk the data substrate: what data, where, who controls, quality assessment, IP/rights status
- Score Dimension 2

**Output:** dimensions 1 and 2 scored with rationale captured in `scoring-worksheet.md`.

---

## Hour 3 — Integration + governance (Dimensions 3, 4)

**Attendees:** technical lead, security/architecture lead, compliance officer (if available).

**Agenda:**
- Integration walkthrough: API inventory, OAuth posture, MCP servers (if any), enterprise-tier identity provider integration
- Score Dimension 3
- Governance walkthrough: HITL workflows in current AI deployments (if any), audit trail infrastructure, regulatory mapping, named compliance officer status
- Score Dimension 4

**Output:** dimensions 3 and 4 scored.

---

## Hour 4 — Lunch / consultant work block

The consultant takes a working lunch. While the operator's team is at lunch:

- Consultant reviews the morning's findings
- Begins drafting the report scaffold
- Identifies which afternoon sessions need which attendees
- Sends a brief mid-day note to the executive sponsor: "Here's where we are; here's what we're covering this afternoon"

The mid-day note is a small but consequential touch — the sponsor stays informed and can flag concerns before the afternoon proceeds.

---

## Hour 5 — Evaluation + operations (Dimensions 5, 6)

**Attendees:** technical lead, anyone running existing AI deployments.

**Agenda:**
- Eval discipline walkthrough: existing eval suites, CI integration, quality bar enforcement, what gets measured
- Score Dimension 5
- Operational walkthrough: incident response for AI-specific failures, cost monitoring, change management for model upgrades
- Score Dimension 6

**Output:** dimensions 5 and 6 scored.

---

## Hour 6 — Organizational readiness (Dimension 7)

**Attendees:** executive sponsor (mandatory), HR or change-management partner if available.

**Agenda:**
- Sponsorship clarity: who is accountable for the AI deployment's outcomes
- Owner clarity: who runs it day-to-day; what authority they have
- Change-management capacity: history of deployments that required organizational change; lessons learned
- Score Dimension 7

This hour is intentionally with the sponsor because Dimension 7 is the one most often over-scored. Sponsors hear "yes, we're ready"; operators-on-the-ground hear "we have no idea." The consultant's job is to surface the discrepancy.

**Output:** dimension 7 scored.

---

## Hour 7 — Synthesis (consultant solo work)

**Attendees:** consultant only.

**Agenda:**
- Compute composite score
- Identify the 2–3 highest-impact gap-closing actions
- Draft Sprint Quote scope per `pricing-packaging.md` — the right-sized follow-on
- Write the report

The synthesis hour is consultant-solo for a reason: the operator should not be in the room when the consultant decides what the rubric says. Honesty depends on independence at this step.

**Output:** draft report in `engagements/<engagement_id>/diagnostic-report.docx` (using the bhil-docx skill).

---

## Hour 8 — Findings session and Sprint Quote walk-through

**Attendees:** executive sponsor, technical lead, anyone the operator wants present.

**Agenda:**
- Walk the composite score and per-dimension rationale
- Walk the 2–3 highest-impact recommendations
- Walk the Sprint Quote, including the 100% diagnostic-credit policy
- Q&A — typically 20 minutes

**Output:** signed Sprint Quote (or signed walk-away with a documented "not yet" decision). Audit-chain entry of the engagement closure.

The findings session is the moment of truth. Operators who bought into the diagnostic-as-sales-pitch theory are sometimes surprised by honest scoring; consultants must hold the line. Operators who appreciate the honesty are the ones who become long-term clients.

---

## Post-day (within 24 hours)

- Final report delivered as a polished `.docx` (with the bhil-docx skill applied)
- Sprint Quote PDF
- Engagement folder archived per the operator's retention preference
- Follow-up scheduled for 60 days hence to convert or formally close

---

## Common variances

| Variance | Adjustment |
|---|---|
| Operator pushes back on Dimension 4 score (governance underestimated) | Walk the rubric anchors with them; if their evidence supports a higher score, revise. Document the revision. |
| Operator wants additional dimensions scored (e.g., "vendor management") | Out of scope for diagnostic; capture as a Sprint addition |
| Composite score is low and operator wants follow-on engagement anyway | Quote a Foundational Sprint (single dimension closure) before agent work |
| Composite score is high and operator wants Enterprise retainer | Quote Enterprise per `../architecture/cost-economics.md` |
| Mid-day discovery that the operator's situation is materially different from intake | Pause and re-frame; do not power through a misaligned diagnostic |

---

## What the runbook is not

- Not a script. The consultant adapts to the operator. The runbook is structure, not text.
- Not optional. Dimensions cannot be skipped because the schedule is tight. If a dimension can't be scored, the report says so and the score is recorded as N/A with a follow-up action.

---

## Citations

- BHIL LOCUS Framework — diagnostic runbook benchmark, github.com/camalus/BHIL-LOCUS-Framework.
- BHIL ADR Blueprint — engagement-discipline benchmark.

---

*BHIL CADRE Framework — readiness/day-runbook.md — v1.0.0*
