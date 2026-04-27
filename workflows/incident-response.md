# Workflow: Incident Response

*From signal to resolution. The incident-response workflow is invoked when any of the cadre's monitoring surfaces (A12 audit findings, A14 cost spikes, A11 eval regressions, operator-reported issues, regulator inquiries) produces a Sev-1 or Sev-2 signal. A13 (incident responder) owns the workflow; the orchestrator coordinates resources.*

---

## Severity classification

- **Sev-1.** Active integrity failure, regulator inquiry, data exposure, audit-chain corruption, unauthorized memory write, runaway cost. Response begins immediately; no SLA other than "as fast as humanly possible." Tier 3 review.
- **Sev-2.** Control failure with bounded scope, eval regression below threshold, repeated SLO breaches, MCP server compromise indicator, single-engagement cadre failure. Response begins within 4 hours of detection. Tier 2 review.
- **Sev-3.** Anomaly worth investigating, single-trace failure, unexpected metric drift, single SLO breach. Response begins within 1 business day. Tier 1 review.

Severity is assigned by A13 at intake. Severity may be raised during response based on findings; severity is rarely lowered (a downgrade requires Tier 2 review and a documented basis).

---

## Phase 1 — Detection and triage

Detection sources:

- A12 audit-cycle findings
- A14 cost-meter alerts
- A11 eval regressions (real-time, not just weekly cadence)
- Direct operator report
- Regulator or third-party report
- Internal review trigger (a reviewer escalating during a Tier 2/3 review)

A13 acknowledges within the SLA, performs initial triage (severity assignment, scope assessment, immediate-containment decision), and opens the incident chain entry. The entry includes:

- Detection source and timestamp
- Initial severity
- Scope (engagement-bounded, multi-engagement, framework-level)
- Initial containment actions taken (e.g., cadre paused, MCP server disconnected, deliverable held)
- Reviewer roster engaged

For Sev-1 incidents, containment is immediate and over-broad; scope is narrowed during investigation. Pausing too much is preferable to pausing too little.

---

## Phase 2 — Containment

Containment ends or bounds the incident's active impact. Common containment actions:

- **Pause cadre.** Halt new actions in the affected engagement. Existing in-flight actions complete or are explicitly aborted.
- **Disconnect upstream.** Drop a compromised or non-conformant MCP server from the active allowlist.
- **Hold deliverable.** Block a Tier 2 deliverable from external release until investigation completes.
- **Memory rollback.** Targeted or time-based rollback per `governance/memory-policy.md` discipline. Always Tier 3 for cross-engagement, Tier 2 for per-engagement.
- **Reviewer disengagement.** When a reviewer's action is implicated, they are removed from active routing pending review.

Every containment action is itself a chain entry. Containment that proves over-broad in retrospect is unwound through the same authorized channels; the cadre does not silently un-pause.

---

## Phase 3 — Investigation

Investigation reconstructs the incident from the audit chain. The reconstruction follows the chain backward from the detection point, identifying:

- The triggering event(s)
- The propagation path through the cadre
- The control surfaces that did or did not fire
- The data, decisions, or external effects affected
- The blast radius (what additional engagements, deliverables, or systems could have been affected, even if not actually affected)

A12 supports investigation by re-running targeted audits over the affected window. A04 (source archivist) supports investigation by surfacing the source materials available at the time of the triggering event. A20 (compliance mapper) is engaged when the investigation suggests regulatory implications.

The investigation produces a draft post-mortem (per `templates/incident-postmortem-template.md`) which is reviewed by the engagement lead and, for Sev-1 and many Sev-2 incidents, by the operator's compliance and legal functions.

---

## Phase 4 — Remediation

Remediation falls into immediate and structural categories.

**Immediate remediation** addresses the specific incident:
- Correct affected outputs (e.g., re-redact a release that was insufficiently sanitized; reissue a corrected dossier)
- Notify affected parties when notification is required by policy or regulation
- Restore the cadre to a known-good state with the post-incident configuration

**Structural remediation** addresses the root cause:
- Add eval coverage for the failure mode (regression test)
- Tighten an allowlist or trust tier
- Update a handoff contract (with full schema-evolution discipline)
- Update the reviewer roster, training, or load model
- Add a known limitation (`governance/known-limitations.md`) when the issue surfaces a gap the framework cannot fully close
- Update prompts, agent specs, or workflows when the issue reveals a procedural gap

Structural remediation is implemented through the framework's normal change discipline (Conventional Commits, CI gates, release notes), not through ad-hoc edits during incident response. The post-mortem identifies the structural changes; the changes themselves are made through the standard development flow.

---

## Phase 5 — Post-mortem and closure

The post-mortem is the canonical record. Sections:

- Summary (one paragraph, blame-free)
- Timeline (chain-derived; not narrative reconstruction from memory)
- Root cause(s) — distinguish triggering event from underlying conditions
- Contributing factors
- What worked (controls that fired correctly are part of the record)
- What did not work
- Immediate remediation (taken)
- Structural remediation (committed, with owners and dates)
- Follow-up review schedule

Post-mortems are reviewed at the appropriate tier. Sev-1 post-mortems are Tier 3 reviewed and (typically) shared with the operator's board-level oversight where one exists. Sev-2 post-mortems are Tier 2 reviewed.

The incident is closed only when:

- Containment is unwound or made permanent
- Immediate remediation is complete
- Structural remediation has commit-tracked plans with owners
- The post-mortem is signed off
- The audit chain entry recording closure is emitted

Closure does not mean the structural remediation is complete; it means the response is complete and the structural items are in the operator's commit-tracked backlog.

---

## Failure modes

- **A13 unavailable.** Backup responders are pre-named in the engagement charter. Failover is itself logged.
- **Investigation stalls.** When chain reconstruction is incomplete (gaps, integrity failures), the investigation cannot proceed past the gap. The gap itself is the finding; reconstruction depends on operator-side records or external anchoring.
- **Remediation conflict.** When immediate remediation conflicts with operator policy (e.g., notification timing constraints), the conflict is escalated to operator counsel rather than resolved by the cadre.
- **Repeat incidents.** A second incident of the same root cause indicates structural remediation failed. The post-mortem for the second incident treats the first incident's remediation gap as the primary root cause.

---

## Audit emissions

- Incident open (severity-tier-appropriate)
- Containment actions (severity-tier-appropriate)
- Investigation findings (Tier 2 minimum)
- Remediation actions (Tier 2 or 3 per scope)
- Post-mortem signoff (severity-tier-appropriate)
- Incident closure (severity-tier-appropriate)

---

## Cross-references

- `cadre/squad-keel-operations/A13-incident-responder.md` — the owning agent
- `cadre/squad-keel-operations/A12-trace-auditor.md` — investigation support
- `cadre/squad-vanta-research/A04-source-archivist.md` — source-side support
- `cadre/squad-pulse-governance/A20-compliance-mapper.md` — regulatory implications
- `templates/incident-postmortem-template.md` — post-mortem skeleton
- `governance/audit-chain-spec.md` — chain reconstruction substrate
- `governance/memory-policy.md` — rollback discipline invoked here
