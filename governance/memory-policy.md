# Memory Policy

*The policy controls that turn the three-scope memory architecture into an enforceable governance posture. Memory architecture (in `architecture/memory-architecture.md`) describes what memory exists; this document describes what is permitted, who decides, and what happens when discipline fails.*

---

## Policy posture in one sentence

CADRE operates with the smallest memory scope that lets the cadre do its work, with strict path validation on every write, with an explicit promote-learnings workflow for cross-engagement persistence, with retention bounded by sector and policy, and with rollback as a first-class operation.

---

## Three scopes, recapped

CADRE recognizes exactly three memory scopes:

- **None.** The default. The agent has no persistent memory and reads only from explicit inputs. Every research-class agent (A01–A05) defaults to None unless a specific reason justifies escalation.
- **Per-engagement.** Memory scoped to a single client engagement. Path is `engagements/<id>/memory/...`. Lifetime ends with engagement closeout.
- **Cross-engagement.** Persistent memory shared across engagements. Path is `cadre/memory/learnings/...`. Writes require an explicit promote-learnings approval; reads are unconstrained but auditable.

The full architectural rationale lives in `architecture/memory-architecture.md`. This document covers the policy controls.

---

## Path validation enforcement

Every memory write is preceded by path validation. The validator is invoked at the tool layer; agents cannot bypass it because the underlying file-write tool refuses any path that fails validation.

The validator enforces three rules:

1. **Scope match.** The agent's `memory_scope` (declared in its YAML frontmatter) must match the path. A `per-engagement` agent cannot write to `cadre/memory/`; a `none` agent cannot write to either memory tree.
2. **Engagement isolation.** A per-engagement agent operating in engagement `<A>` cannot write to `engagements/<B>/memory/`. The validator verifies the engagement ID embedded in the runtime context matches the path.
3. **Reserved path protection.** Certain paths (e.g., `cadre/memory/learnings/`, `cadre/memory/policies/`) require additional capability checks beyond scope match. The promote-learnings workflow is the only sanctioned writer to `cadre/memory/learnings/`.

The validator emits an audit entry for every accepted write and a denial entry for every rejected write. A12 (trace auditor) reviews denials at every audit cycle; a pattern of denials is treated as a control finding.

A reference Python pattern for the validator appears in `architecture/memory-architecture.md`. Operators may implement equivalent controls in their own runtime, provided the same three rules are enforced and the audit emission is preserved.

---

## Promote-learnings workflow

Cross-engagement memory exists only to capture genuine learnings — patterns, policies, calibration constants, exemplars — that apply across the operator's portfolio. Crossing the per-engagement / cross-engagement boundary is a deliberate decision, not a side effect.

The workflow:

1. **Proposal.** A specific learning is proposed for promotion. The proposal includes the source engagement, the learning text, the rationale for cross-engagement applicability, and a proposed sunset condition (when the learning should be re-reviewed).
2. **Review.** A Tier 2 reviewer (per `governance/hitl-policy.md`) reviews the proposal. If the learning carries any client-identifiable content, the reviewer either rejects the proposal or requires rewriting to remove the identifying content.
3. **Sanitization.** Approved proposals are rewritten as engagement-agnostic statements. Specific client names, deal sizes, contact details, and any other client-identifying material are removed. The provenance is logged in the audit chain but not in the learning itself.
4. **Publication.** The sanitized learning is written to `cadre/memory/learnings/` with a structured frontmatter (proposed-at, approved-at, reviewer, source-engagement-hash, sunset-date).
5. **Audit emission.** A19 records the promotion as a Tier 2 decision with the reviewer's identity and rationale.
6. **Periodic review.** A20 (compliance mapper) sweeps `cadre/memory/learnings/` at the cadence defined in operator policy (default: quarterly) and flags entries past their sunset date for re-review.

Learnings that fail re-review are either renewed or deprecated. Deprecated learnings are moved to `cadre/memory/learnings/_deprecated/` rather than deleted, preserving the audit chain.

---

## Retention bounds

Retention is set per memory scope and may be tightened (never relaxed) by operator policy or sector regulation:

- **None.** N/A.
- **Per-engagement.** Default retention through engagement closeout plus 90 days, then archived to cold storage with operator-defined retention (typically 7 years for client work). Sector-specific overrides:
  - Healthcare engagements touching PHI: minimum 6 years (HIPAA records-retention norms; operator's compliance officer confirms specific obligation)
  - Banking model risk artifacts: minimum 7 years (typical SR 11-7 supervisory examination cycle)
  - EU-deployed high-risk systems: minimum 10 years from system placement (EU AI Act Article 18 obligation flows to the operator; CADRE retains substrate accordingly) [VERIFIED — EU AI Act Article 18]
- **Cross-engagement.** Default retention until the next periodic review or sunset, whichever first. Approved learnings persist until deprecated; deprecated learnings retain the same retention as their original engagement scope.

Retention is enforced by an operator-side scheduled job, not by the cadre itself. The cadre's contribution is the structured frontmatter that makes retention machine-determinable.

---

## Rollback discipline

Rollback is a first-class operation, not an emergency improvisation. The cadre supports two rollback modes:

- **Targeted rollback.** Reverts a specific memory write or learning promotion identified by audit chain ID. Other concurrent writes are preserved. Used when a single decision is later determined to be incorrect.
- **Time-based rollback.** Reverts all memory writes after a specified timestamp. Used during incident response when corruption or contamination is suspected.

Both modes preserve the audit chain. A rollback is itself an entry in the chain; it does not delete prior entries. A12 verifies that the post-rollback state corresponds to a valid prior state and that no entries were elided.

Rollback authorization is Tier 3 for cross-engagement scope and Tier 2 for per-engagement scope. The reviewer is named in the audit entry. A13 (incident responder) is the only agent that proposes rollback; a human reviewer authorizes; the operation is performed at the tool layer with full chain emission.

---

## Failure modes and responses

- **Path validator bypassed.** Treated as a Sev-1 control failure. A13 opens an incident; A12 reconstructs the actual writes against the expected scope; operator's compliance function is notified. Do not paper over with retroactive validation.
- **Learning promoted without sanitization.** Treated as a Tier 3 incident. The learning is unpublished; the audit chain entry is preserved; operator's privacy/compliance function reviews scope of potential exposure. If client-identifying content reached `cadre/memory/learnings/`, the rollback covers all reads of that entry as well.
- **Retention exceeded without policy basis.** Triggers an A20 finding. Operator's records management function determines whether the over-retained data must be purged immediately or whether a documented policy basis exists.
- **Rollback authorized without review.** Treated as a Tier 3 control failure. The unauthorized rollback is itself rolled back where possible; the original state is restored; reviewers are reconvened.

---

## What memory policy does not cover

This document does not cover:

- Vector store contents and retrieval policies; those live in `architecture/memory-architecture.md` because they are architectural choices, not governance choices, in the current design.
- Model-side memory features offered by the model provider (e.g., the Anthropic Managed Agents Memory beta surfaced in `architecture/mcp-integration.md`). When an operator opts into provider-side memory, additional policy controls are required and must be documented per engagement.
- Data minimization at ingest; that is upstream of memory and is handled in the source-archivist (A04) and PII redactor (A18) specs.

---

## Cross-references

- `architecture/memory-architecture.md` — the architectural counterpart
- `governance/hitl-policy.md` — tier definitions invoked by promote-learnings and rollback
- `governance/audit-chain-spec.md` — the chain that holds memory policy decisions
- `governance/known-limitations.md` — gaps and edge cases in current memory enforcement
- `cadre/squad-keel-operations/A12-trace-auditor.md` — verifier of memory policy compliance
- `cadre/squad-pulse-governance/A19-audit-logger.md` — recorder of memory decisions
- `cadre/squad-pulse-governance/A20-compliance-mapper.md` — operational counterpart for retention review
