# Workflow: Weekly Cadence

*The steady-state operational rhythm. Every active engagement runs one weekly cadence cycle. The cycle compresses eval, audit, cost review, governance scan, and reviewer-roster check into a predictable, auditable sequence that surfaces drift before it compounds.*

---

## Owner and reviewers

- **Owner:** Engagement lead (operator-side)
- **Coordinator:** Orchestrator agent
- **Tier 2 reviewers:** Engagement lead reviews the cadence findings dossier; compliance officer reviews when findings include governance items
- **Tier 3 reviewers:** Required only when findings include sector-triggered escalations

---

## Cadence

Weekly. Operator's calendar week boundary. Late or skipped cycles are themselves a control finding; A12 records skipped cycles as anomalies.

A weekly cycle is roughly 4 hours of cadre work and 1–2 hours of operator review. SKU envelopes accommodate weekly cadence; the cost lives in the steady-state operating budget, not the deliverable budget.

---

## Step 1 — Eval cycle (A11)

A11 (eval runner) executes the engagement's eval suite against the most recent week of production traffic (or a representative sample for high-volume engagements). The output:

- Per-eval metric results
- Comparison to baseline (per-engagement baseline established at startup)
- Comparison to prior week
- Flagged regressions (any eval below its declared threshold)
- Flagged improvements worth investigating (an unexplained jump can indicate a measurement bug)

Results are written to `engagements/<id>/cadence/<week>/evals.json` and `engagements/<id>/cadence/<week>/evals-summary.md`.

---

## Step 2 — Audit cycle (A12)

A12 (trace auditor) samples production traces from the week. The sampling rate is engagement-specific (typically 1–10% of traces, with 100% sampling for Tier 2 and Tier 3 actions). For each sampled trace:

- Verify handoff schemas validated cleanly (cross-check with A15 records)
- Verify HITL tier assignments are consistent with policy
- Verify evidence classifications match source structure
- Verify memory writes were path-validated and that the validator emitted the expected entries
- Verify audit chain integrity (full chain re-verification for any week where new chain entries crossed an external anchor; sample verification otherwise)

Findings are classified Sev-3 (anomaly worth investigating), Sev-2 (control failure requiring response), or Sev-1 (active integrity failure requiring incident response). Sev-1 findings invoke the incident-response workflow rather than waiting for the cadence dossier.

---

## Step 3 — Cost review (A14)

A14 (cost meter) compiles the week's spend per agent, per action class, and per deliverable. The output:

- Spend versus budget (engagement-level ceiling and per-deliverable envelopes)
- Token-usage trends (Opus orchestration tokens vs Sonnet subagent tokens vs Haiku utility tokens)
- Cost per accepted deliverable (the operator-relevant unit cost)
- Anomalies: agents whose spend is anomalous compared to their declared parallelism class and historical pattern

Cost spikes that crossed the engagement's ceiling during the week have already triggered A13 escalation; the cost review confirms the response was executed and proposes structural fixes for recurring spikes.

---

## Step 4 — Governance scan (A20)

A20 (compliance mapper) sweeps the per-engagement risk register against the week's activity:

- New regulatory developments in the engagement's jurisdictions/sectors that may require operator response
- Items in `governance/known-limitations.md` whose scope extended to engagement actions in the week
- Memory items approaching sunset or retention boundaries
- Reviewer roster coverage relative to the week's actual decision distribution (e.g., did the engagement need a Tier 3 reviewer for a use case the roster did not cover?)

A20's output feeds the cadence dossier and surfaces items requiring operator follow-up. A20 does not modify operator policy unilaterally; it surfaces and recommends.

---

## Step 5 — Reviewer roster check

The orchestrator confirms that the week's HITL decisions were made by reviewers meeting roster discipline (jurisdiction match, sector match, role match, load match). Anomalies:

- Tier 2 or 3 decisions made by reviewers outside their declared scope
- Load imbalance (a single reviewer carrying disproportionate decision volume)
- SLO breaches (decisions made past the tier's SLO)

Anomalies are surfaced; remediation is operator-side (roster expansion, load redistribution, additional training).

---

## Step 6 — Cadence dossier

The cadre produces a single dossier compiling the week's findings. Structure:

- Executive summary (one page)
- Eval cycle results
- Audit cycle findings
- Cost review
- Governance scan
- Reviewer roster check
- Action items (with owners, due dates, and tier-appropriate review requirements)
- Comparison to prior week (deltas, trends, persistent items)

The dossier is written to `engagements/<id>/cadence/<week>/dossier.md` and presented to the engagement lead. The lead reviews and either accepts the dossier (closing the cycle) or routes specific items for additional review.

The cadence dossier is itself a Tier 1 audit chain entry; specific findings within it may carry their own tier classifications.

---

## Failure modes

- **Eval suite drift.** When the eval suite no longer reflects the engagement's actual use cases, eval results stop being meaningful. A12 surfaces this as a control finding; the eval suite is updated through SP-07's evolution discipline.
- **Audit-trace gaps.** When sampling reveals gaps in the chain (entries that should exist but do not), the cycle escalates immediately to incident response. The cycle does not proceed past chain integrity verification.
- **Cost ceiling crossed mid-week.** Already handled by A13 escalation in real time; the cadence cycle confirms post-hoc and proposes prevention.
- **Reviewer SLO breaches.** Surfaced in step 5; cadence does not retroactively fix breaches but does require operator response (typically a documented rationale plus a remediation commitment).
- **Cycle delayed past week boundary.** Itself a control finding. Cadence cycles do not skip; a delayed cycle is run as soon as feasible and the delay is logged.

---

## Audit emissions

- Cycle initiation (Tier 1)
- Eval results (Tier 1)
- Audit findings (Tier 1 for Sev-3, Tier 2 for Sev-2; Sev-1 invokes incident response)
- Cost review (Tier 1)
- Governance scan results (Tier 1; Tier 2 if items require operator response)
- Cadence dossier acceptance (Tier 2)

---

## Cross-references

- `cadre/squad-keel-operations/A11-eval-runner.md`
- `cadre/squad-keel-operations/A12-trace-auditor.md`
- `cadre/squad-keel-operations/A14-cost-meter.md`
- `cadre/squad-pulse-governance/A20-compliance-mapper.md`
- `prompts/SP-07-eval-harness.md` — eval suite evolution discipline
- `workflows/incident-response.md` — invoked by Sev-1 findings
- `governance/audit-chain-spec.md` — verification cadence
