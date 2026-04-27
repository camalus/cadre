---
engagement_id: NL-2026-0341-FULL
artifact_type: handoff-trace
artifact_version: 1.0
trace_window: 2026-04-29T09:15:00-07:00 .. 2026-04-29T11:42:00-07:00
stage: ATLAS-product
---

# Handoff Trace — ATLAS Product Stage, NorthlineCo

This trace captures one stage of the Full SKU engagement: the ATLAS
Product stage that produces the PRD, specs, and acceptance criteria
for the support assistant. It demonstrates the parallel-then-serialized
pattern, schema validation at every boundary, and HITL routing.

The full audit chain entries for this trace live at
`engagements/NL-2026-0341-FULL/audit-chain.jsonl` lines 412–467. This
file is a human-readable summary.

## Stage inputs

- `engagements/NL-2026-0341-FULL/handoffs/charter/charter.json`
  (engagement charter, validated)
- `engagements/NL-2026-0341/01-readiness-diagnostic.md` (parent
  diagnostic, imported)
- `engagements/NL-2026-0341-FULL/handoffs/research/regulatory-confirm.json`
  (VANTA limited output — confirms no sector overlay)

## Sequence

### T+0:00 — Orchestrator dispatch decision

Orchestrator reads each ATLAS agent's YAML frontmatter:

| Agent | parallelism_class | hitl_tier |
|-------|-------------------|-----------|
| A06 PRD Author        | parallel-safe | 2 |
| A07 Spec Decomposer   | parallel-safe | 1 |
| A08 Acceptance Curator| parallel-safe | 2 |
| A09 Roadmap Mapper    | serialized    | 2 |
| A10 Release Notes     | serialized    | 1 |

Decision: dispatch A06, A07, A08 in parallel pool. Hold A09 and A10
for serialized phase after parallel pool reconciles.

### T+0:02 — Parallel pool dispatch

A06, A07, A08 dispatch simultaneously via Task tool. Each receives
the stage inputs.

### T+0:18 — Parallel pool returns

A06 returns first (PRD draft), then A08 (acceptance criteria), then
A07 (spec decomposition). Total wall time: 16 minutes.

### T+0:18 — A15 Handoff Validator runs

A15 validates each output against the ATLAS-stage schema. Result:

| Output           | Schema valid | Notes                         |
|------------------|--------------|--------------------------------|
| A06 PRD          | Yes          |                                |
| A07 Spec set     | Yes (after revision) | First pass missed required `traceability_back_to_prd_section` field on 2 of 14 specs. A15 rejected, returned diff to A07. A07 re-ran, second pass clean. |
| A08 Criteria     | Yes          |                                |

A07 re-run audit entry: line 423.

### T+0:28 — Reconciliation

Orchestrator runs reconciliation. Conflicts detected:

- A06 PRD names the assistant `"northline-support-bot"`. A07 specs use
  `"NorthlineSupportBot"` consistently. A08 criteria use both forms.
- Resolution: orchestrator surfaces this as a naming conflict requiring
  A12 review (style consistency). A12 chooses kebab-case form per the
  client's stated naming convention; A06 unchanged, A07 and A08
  re-emitted with fixes. Audit entries 428–431.

### T+0:42 — Serialized phase: A09 Roadmap Mapper

A09 dispatches with reconciled A06/A07/A08 outputs as input. Produces
roadmap including the 2-week pre-build sprint as Phase 0. Wall time:
14 minutes.

### T+0:56 — A15 validates A09 output

Pass. Audit entry 438.

### T+0:58 — Serialized phase: A10 Release Notes

A10 dispatches. Produces internal user-communication release notes for
NorthlineCo's intended pilot users. Wall time: 9 minutes.

### T+1:07 — A15 validates A10 output

Pass. Audit entry 446.

### T+1:08 — HITL routing

A17 routes:

| Artifact          | Tier | Reviewer                | SLO     |
|-------------------|------|-------------------------|---------|
| A06 PRD           | 2    | NorthlineCo IT Director | 1 day   |
| A07 Specs         | 1    | A. Patel (BHIL)         | 4 hrs   |
| A08 Criteria      | 2    | NorthlineCo IT Director | 1 day   |
| A09 Roadmap       | 2    | J. Hurd (BHIL)          | 1 day   |
| A10 Release notes | 1    | A. Patel (BHIL)         | 4 hrs   |

A09 was pre-routed to BHIL operator because the roadmap embeds
commercial milestones (engagement billing markers) — sector-bumped
to internal review only.

### T+2:27 — All Tier-1 reviews complete

A. Patel approves A07 (with two minor revision notes — applied) and
A10 (clean). Audit entries 451–456.

### T+ next business day — Tier-2 reviews

NorthlineCo IT Director approves A06 with one revision (clarification
on out-of-scope behaviors). A07 is re-emitted to align with the
clarification. Final approvals on A06, A08, A09 land mid-morning.

## Outputs

| Path                                              | Status   |
|---------------------------------------------------|----------|
| `handoffs/atlas/prd.json`                         | Approved |
| `handoffs/atlas/specs/`                           | Approved |
| `handoffs/atlas/acceptance-criteria.json`         | Approved |
| `handoffs/atlas/roadmap.json`                     | Approved |
| `handoffs/atlas/release-notes.json`               | Approved |

All outputs written under `engagements/NL-2026-0341-FULL/handoffs/atlas/`
and now feed the KEEL operations stage.

## Lessons surfaced

1. **A07 schema miss** — the missing `traceability_back_to_prd_section`
   field suggests A07's prompt may benefit from an explicit emphasis
   on traceability. Filed as `enhancement` issue against
   `cadre/squad-atlas-product/A07-spec-decomposer.md`.
2. **Naming conflict** — operator suggests adding a "naming convention"
   field to the engagement charter so future engagements set it
   upstream rather than reconciling downstream.

These lessons stay engagement-local until promoted via
`workflows/promote-learnings.md`.
