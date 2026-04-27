# Workflow: Promote Learnings

*The cross-engagement memory boundary crossing. Promotion takes a learning observed in one engagement and makes it available across the operator's portfolio. The workflow is deliberately friction-laden because the boundary is consequential: client-identifying content must never cross, and stale learnings must not accumulate.*

---

## Owner and reviewers

- **Proposer:** Any agent or human in the source engagement (often surfaced by A05 Synthesizer at engagement closeout, A12 Trace Auditor during weekly cadence, or operator-side reviewers)
- **Sanitizer:** Engagement lead (operator-side) — owns the rewrite for engagement-agnostic statement
- **Approver (Tier 2 reviewer):** Compliance officer or designated learnings-review reviewer per the operator's roster
- **Operational follow-up:** A20 Compliance Mapper (sunset reviews); A19 Audit Logger (chain emissions)

---

## What promotion is for

Cross-engagement memory exists to capture genuine learnings that apply across engagements. Examples of appropriate promotions:

- Pattern: a redaction failure mode in one healthcare engagement that other healthcare engagements should inherit prevention for
- Calibration: an observed eval threshold for a class of decisions that should be the cadre's default starting point
- Policy refinement: a HITL tier assignment that proved correct in practice for a category of action
- Exemplar: a handoff schema fragment that handled a tricky case well
- Limitation: an MCP-server quirk that affected handling and should be noted in the framework's known-limitations file

Examples that should not be promoted:

- Anything client-identifying (operator name acceptable; downstream-client name not)
- Specific deal sizes or commercial terms
- Specific personnel or contact details
- Engagement-specific operational details that don't generalize
- Speculative learnings that have not yet been validated through application

---

## Phase 1 — Proposal

A proposal artifact is written to `engagements/<id>/promotions/proposed/<slug>.md`. The proposal includes:

- **Title.** Engagement-agnostic statement of the learning
- **Rationale.** Why this generalizes; what other engagements would benefit
- **Source engagement reference.** Engagement ID; specific traces, deliverables, or incidents that produced the observation
- **Sanitization checklist.** Explicit identification of any client-identifying content present in the source artifacts that must not appear in the promoted version
- **Proposed sunset condition.** When this learning should be re-reviewed (default: 12 months; specific learnings may have shorter or longer sunsets per the rationale)
- **Proposed location.** Where in `cadre/memory/learnings/` this would live (typically organized by category: redaction, eval, policy, exemplars, limitations)

The proposal is itself a Tier 1 chain entry. Multiple proposals can batch through closeout; each is treated as a separate decision.

---

## Phase 2 — Review

The Tier 2 reviewer evaluates each proposal:

- **Generalizability.** Does the learning apply beyond the source engagement?
- **Sanitization completeness.** Has every client-identifying element been identified and removed in the proposed promoted text?
- **Necessity.** Does this learning require cross-engagement memory, or could it be captured in framework documentation, prompts, or agent specs instead?
- **Sunset appropriateness.** Is the proposed sunset reasonable given the learning's nature?
- **Conflict.** Does this conflict with existing learnings? If so, which prevails and why?

Decisions:

- **Approve.** Proceed to sanitization and publication.
- **Approve with revisions.** Specific edits required; back to proposer for revision and re-review.
- **Reject for sanitization gap.** The proposed text contains client-identifying content; rewrite required.
- **Reject for non-generalization.** The learning is engagement-specific; no promotion. The learning may still be valuable; it stays in engagement memory and the engagement's lessons-learned record.
- **Defer.** Insufficient information to decide; specific evidence or experience needed before approval is appropriate.
- **Redirect.** The learning should be captured in framework documentation (prompts, agent specs, governance docs) instead of cross-engagement memory; route through the framework change discipline.

The decision and rationale are recorded in the chain.

---

## Phase 3 — Sanitization

Approved proposals are rewritten as engagement-agnostic statements. The sanitizer (typically the engagement lead) produces the final text. The reviewer verifies the sanitized text before publication; sanitization without re-verification is not permitted.

The sanitization checklist from the proposal is the basis for verification. Any item on the checklist must be confirmed absent from the final text. Reviewers should test by attempting to identify the source engagement from the promoted text alone; if identification is possible, sanitization is incomplete.

---

## Phase 4 — Publication

The sanitized learning is written to `cadre/memory/learnings/<category>/<slug>.md` with structured frontmatter:

```yaml
---
id: learning-2026-04-26-redact-name-suffix-pattern
category: redaction
title: <engagement-agnostic title>
proposed_at: <ISO timestamp>
approved_at: <ISO timestamp>
reviewer: <reviewer handle>
source_engagement_hash: <one-way hash of source engagement ID>
sunset_date: <ISO date>
status: active
related_limitations: [<refs to known-limitations entries>]
related_prompts: [<refs to SP-XX prompts>]
related_agents: [<refs to A0X agent specs>]
---
```

The body is the engagement-agnostic statement plus the rationale-without-identifiers plus any examples (which themselves must be sanitized or synthetic).

The publication is a Tier 2 chain entry under the `cadre-system` engagement ID. Future cross-engagement reads of the learning are auditable.

The source-engagement hash is one-way; readers cannot reverse it to identify the source engagement. Operators who need the link (e.g., during audit) maintain the mapping in operator-side records, not in the cadre.

---

## Phase 5 — Periodic review

A20 (compliance mapper) sweeps `cadre/memory/learnings/` at the operator-defined cadence (default: quarterly):

- Learnings approaching their sunset date are flagged for re-review
- Learnings whose related context has changed (e.g., a referenced agent spec has been substantially revised) are flagged
- Learnings that have not been read in the recent window are flagged as candidates for deprecation (a learning no one consults is not earning its place)

Re-review uses the same Tier 2 process as initial review. Outcomes:

- **Renew.** Learning remains active with a new sunset date.
- **Revise.** Specific edits and re-publication.
- **Deprecate.** Move to `cadre/memory/learnings/_deprecated/` with the deprecation rationale. The chain preserves the original entry and records the deprecation.

Deprecated learnings are not deleted. They remain auditable and may inform future learnings, but they are not surfaced in active retrieval.

---

## Failure modes

- **Sanitization gap discovered after publication.** Sev-1 if client-identifying content reached the cross-engagement scope. The learning is unpublished; rollback follows the rollback discipline (`governance/memory-policy.md`); operator's privacy/compliance function reviews potential exposure scope; an incident is opened.
- **Approval without proposal.** Treated as a Tier 3 control failure. The publication is unpublished; the original control failure is itself a chain entry; the approver's authority is reviewed.
- **Sunset missed without review.** A20's responsibility; itself a control finding. The learning is suspended pending review.
- **Promoted learning conflicts with later evidence.** The conflict is itself a learning candidate. The original learning is revised or deprecated; the new learning is proposed. The chain preserves both.

---

## Audit emissions

- Proposal (Tier 1)
- Review decision (Tier 2)
- Sanitization (Tier 1, performed by sanitizer; reviewed by approver)
- Publication (Tier 2)
- Renewal / revision / deprecation (Tier 2)

---

## Cross-references

- `architecture/memory-architecture.md` — three-scope architecture
- `governance/memory-policy.md` — policy controls including this workflow
- `governance/audit-chain-spec.md` — chain entries that record the workflow
- `governance/known-limitations.md` — destination for limitation-class learnings
- `cadre/squad-pulse-governance/A20-compliance-mapper.md` — periodic-review owner
- `cadre/squad-pulse-governance/A19-audit-logger.md` — chain emission
- `workflows/engagement-closeout.md` — typical batch trigger for proposals
