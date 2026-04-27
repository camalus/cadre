---
engagement_id: NL-2026-0341-FULL
artifact_type: eval-report
artifact_version: 1.0
report_date: 2026-05-13
eval_run_id: eval-2026-05-13-NL-r004
eval_runner_agent: A11
trace_audit_agent: A12
hitl_tier: 2
hitl_status: approved
---

# Evaluation Harness Report — NorthlineCo Support Assistant

## Premise

The NorthlineCo Full SKU engagement included a pre-build sprint to
build an evaluation harness — the Express diagnostic identified
evaluation discipline as the weakest of seven dimensions (1/4). This
report covers the fourth and final pre-launch eval run before pilot
deployment.

## Eval set

| Set            | Cases | Source                                       |
|----------------|-------|----------------------------------------------|
| Golden         | 80    | Curated by Tier-1 Support Lead from historical tickets. |
| Edge           | 25    | Constructed by A11 to probe out-of-scope, ambiguous, multi-step questions. |
| Adversarial    | 15    | Constructed by A11 + A12 to probe known failure modes. |
| Regression     | 30    | Cases that previously failed in runs r001–r003. |
| **Total**      | **150** |                                              |

## Run configuration

- Model under test: Claude Sonnet 4.6 with NorthlineCo system prompt
  v0.4.1
- Knowledge base snapshot: 2026-05-12
- Temperature: 0.0 (deterministic)
- Repetitions per case: 3 (for stability check)

## Headline results

| Metric                             | r001 | r002 | r003 | r004 |
|------------------------------------|------|------|------|------|
| Golden set pass rate               | 71%  | 84%  | 91%  | 96%  |
| Edge set pass rate                 | 32%  | 48%  | 64%  | 76%  |
| Adversarial set safe-refuse rate   | 80%  | 87%  | 93%  | 100% |
| Regression set re-pass rate        | n/a  | 88%  | 96%  | 100% |
| Stability (3-rep agreement)        | 89%  | 93%  | 96%  | 99%  |

## Per-category findings

### Golden set (96%)

77 of 80 cases pass. The 3 remaining failures cluster on a single
Confluence page (`field-ops-procedures/return-merchandise.md`) that
contains contradictory information across two sections. Recommendation
to NorthlineCo: resolve the source-of-truth conflict in the underlying
documentation, not in the assistant's prompt. This is a content
hygiene gap, not an AI gap.

### Edge set (76%)

19 of 25 cases pass. Failure mode pattern: when a question requires
combining information from two Confluence pages, the assistant
sometimes summarizes one page accurately and omits the other. This is
a known limitation of single-pass retrieval; the recommended mitigation
is a re-ranking pass before answer generation.

### Adversarial set (100% safe-refuse)

All 15 adversarial cases — questions outside the documented scope,
attempts to extract knowledge not in the KB, and questions seeking
authoritative judgment on ambiguous policy — produced safe refusals
with redirection to the human support lead. This is the target
behavior.

### Regression set (100%)

All 30 cases that previously failed in earlier runs now pass. The
regression suite continues to grow as new failures are discovered in
production-like testing.

## Stability

99% three-repetition agreement at temperature 0.0 indicates the system
is operating as a deterministic function within tolerance. The 1%
disagreement is across two cases that involve dates relative to "today"
where wall-clock differences across the three repetitions caused
divergent answers. This is documented and not considered a defect.

## Cost

| Item                          | Value          |
|-------------------------------|----------------|
| Total tokens consumed (run 4) | 1.4M           |
| Cost (Sonnet 4.6 rates)       | ~$4.20         |
| Per-case average              | ~$0.028        |

## A12 audit

A12 Trace Auditor sampled 15 of 150 cases for trace-level review. All
15 traces passed audit — no fabricated citations, no off-policy tool
calls, no PII leakage in outputs.

## Recommendation

The system meets BHIL's published quality bar for pilot launch:

- ≥95% pass on golden set ✓ (96%)
- ≥75% pass on edge set ✓ (76%)
- 100% safe-refuse on adversarial set ✓
- 100% regression set re-pass ✓
- ≥95% stability ✓ (99%)

Recommend proceeding to pilot with the 12-person field operations
sub-group identified in the engagement charter. Pilot duration: 2 weeks.
Pilot success criteria documented separately.

## Artifacts

- Full case-by-case results: `engagements/NL-2026-0341-FULL/handoffs/keel/eval-r004-results.json`
- A12 audit trail: `engagements/NL-2026-0341-FULL/handoffs/keel/eval-r004-audit.json`
- Trace samples: `engagements/NL-2026-0341-FULL/handoffs/keel/eval-r004-traces/`

## HITL

Tier 2 review by NorthlineCo IT Director and BHIL operator. Both
approved on 2026-05-14. Audit entries 1207–1212.
