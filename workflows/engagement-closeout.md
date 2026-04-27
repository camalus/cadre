# Workflow: Engagement Closeout

*From last deliverable to archived record. The closeout workflow finalizes deliverables, archives the engagement, extracts lessons, and ensures every retention obligation is met. Closeout is not "shutdown"; it is the structured handoff from active operation to long-term records management.*

---

## Owner and reviewers

- **Owner:** Engagement lead (operator-side)
- **Coordinator:** Orchestrator agent
- **Tier 2 reviewers:** Engagement lead and compliance officer
- **Tier 3 reviewers:** Required when sector-triggered records obligations apply (HIPAA, SR 11-7, EU AI Act Article 18) or when the closeout includes an unusual condition (early termination, cadre incident, regulator inquiry)

---

## Triggering conditions

Closeout is triggered by:

- Planned engagement end per the charter's termination conditions
- Operator decision to end the engagement
- Renewal that materially changes scope (the prior engagement is closed; a new engagement starts)
- Regulatory or contractual mandate

A closeout invoked by an active incident requires the incident to be at closure phase before closeout proceeds; closeout cannot bypass open incident remediation.

---

## Phase 1 — Final deliverables

The cadre completes all in-flight work:

- Outstanding deliverables are produced through the standard handoff and tier-appropriate review chain
- Drafts in flight that will not be completed are explicitly aborted and recorded as such (not silently abandoned)
- Open eval-cycle and audit-cycle items are completed; the final cadence dossier covers the partial week through closeout
- Any pending HITL decisions are routed to closure (decided or explicitly withdrawn)

Final deliverables receive the same review discipline as ordinary deliverables; closeout is not a justification for relaxed review.

---

## Phase 2 — Final reconciliation

The orchestrator runs end-of-engagement reconciliations:

- A14 produces a final cost report (full engagement spend, per-deliverable unit costs, variance from budgeted SKU, recurring spike sources)
- A11 produces a final eval summary (baseline-to-final delta, regressions and improvements, eval-suite drift if any)
- A12 performs a full-chain integrity verification of the engagement's audit chain
- A15 confirms all handoff schemas validated; any unresolved handoff items are resolved or explicitly aborted
- A20 performs a final compliance scan against the engagement's jurisdiction/sector configuration; any items remaining open feed the operator's records-management backlog

The reconciliation artifacts are stored at `engagements/<id>/closeout/reconciliation/`.

---

## Phase 3 — Lessons-learned extraction

Closeout is the principal moment for lessons-learned. The orchestrator and engagement lead jointly review:

- Successful patterns worth capturing as cross-engagement learnings (candidates for the promote-learnings workflow)
- Recurring incidents or near-misses (candidates for structural remediation in the framework)
- Reviewer-roster gaps that surfaced during the engagement
- Cost surprises that the SKU envelope did not accommodate
- Tooling or MCP-server gaps the engagement worked around
- Operator-side process gaps the cadre cannot close

Lessons-learned are documented at `engagements/<id>/closeout/lessons.md` and routed:

- Cross-engagement learnings (after sanitization) to the promote-learnings workflow
- Framework changes to the cadre's structural remediation backlog
- Operator-side items to the operator's process-improvement backlog

The lessons-learned document is reviewed at Tier 2.

---

## Phase 4 — Promotions

Approved cross-engagement promotions follow the promote-learnings workflow (`workflows/promote-learnings.md`). Closeout does not bypass the workflow; it batches candidate promotions for efficient review. Each promotion is its own Tier 2 decision.

If no promotions are appropriate, the lessons-learned document records that explicitly. Empty promotion sets are normal; many engagements produce engagement-specific knowledge that does not generalize.

---

## Phase 5 — Archive

The engagement directory is archived. Archive structure:

- All artifacts under `engagements/<id>/` are preserved
- The audit chain segment for the engagement is sealed (a final entry records the closeout, the integrity hash of the chain, and the archival storage location)
- Memory contents (per-engagement) are preserved per the retention schedule (`governance/memory-policy.md`)
- External-facing deliverables and their underlying artifacts are linked through the chain so that future verification can reconstruct what was delivered and what supported it

Archival storage location is operator-determined and recorded in the closeout artifact. Archives are immutable; modifications to archived content are themselves recorded incidents requiring Tier 3 review.

---

## Phase 6 — Decommission

Active resources are decommissioned:

- MCP server connections specific to the engagement are dropped from active allowlists
- Reviewer roster entries unique to the engagement are stood down
- Cost-tracking continues only for the residual archival storage cost; active cost meters are zeroed out
- The orchestrator emits the final chain entry for the engagement

Cross-engagement resources (shared MCP servers, framework-level reviewers, framework prompts and agents) are unaffected. The engagement-specific configuration is removed; the framework continues.

---

## Phase 7 — Closeout dossier

The closeout dossier is the artifact the operator retains to demonstrate the engagement was concluded properly. Sections:

- Summary
- Final deliverables (with references)
- Reconciliation artifacts (cost, evals, audit, compliance)
- Lessons learned
- Promotions decided (approved, rejected, deferred)
- Archive location and integrity hash
- Decommission record
- Signatures: engagement lead, compliance officer, Tier 3 signatories where applicable

The closeout dossier itself is archived alongside the engagement artifacts.

---

## Failure modes

- **In-flight work not completable.** Either the engagement extends to complete the work, or the work is explicitly aborted with documented rationale. Silent abandonment is not permitted.
- **Reconciliation surfaces an unaddressed incident.** The closeout pauses; the incident proceeds through incident-response workflow; closeout resumes after incident closure.
- **Audit chain integrity failure surfaced at closeout.** Sev-1 incident; closeout halts; integrity is re-established or the gap is bounded and documented before closeout completes.
- **Promotion rejected at closeout that should have been approved earlier.** The promotion can be reopened in a future engagement's promote-learnings workflow; closeout does not retroactively change prior decisions.
- **Operator decommission timeline conflicts with retention obligation.** Compliance officer arbitrates; the cadre cannot decommission resources that hold artifacts under active retention obligation.

---

## Audit emissions

- Closeout open (Tier 2)
- Each final deliverable (per its own tier)
- Reconciliation artifacts (Tier 1)
- Lessons-learned signoff (Tier 2)
- Each promotion decision (Tier 2)
- Archive sealing (Tier 2)
- Decommission (Tier 2)
- Closeout signoff (Tier 2 or Tier 3 per sector triggers)

---

## Cross-references

- `workflows/promote-learnings.md` — invoked for any cross-engagement promotion
- `workflows/incident-response.md` — invoked when reconciliation surfaces issues
- `governance/audit-chain-spec.md` — chain sealing substrate
- `governance/memory-policy.md` — retention and rollback discipline
- `templates/engagement-charter-template.md` — termination conditions originally specified
- `cadre/squad-keel-operations/A14-cost-meter.md`
- `cadre/squad-keel-operations/A12-trace-auditor.md`
