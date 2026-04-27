---
engagement_id: NL-2026-0341
artifact_type: readiness-scorecard
artifact_version: 1.0
diagnostic_date: 2026-04-15
operator_lead: J. Hurd
hitl_decision_path: engagements/NL-2026-0341/handoffs/hitl/scorecard-decision.json
hitl_tier: 3
hitl_status: approved
---

# Readiness Scorecard — NorthlineCo

## Executive summary

NorthlineCo scores **14 out of 28** on the BHIL 7-dimension AI Readiness
rubric. The composite places them in the **Approaching Ready** band —
sufficient foundation for a tightly-scoped pilot, but specific gaps in
**evaluation discipline** and **operational readiness** will materially
affect engagement risk and timeline if addressed inside the build phase
rather than in a focused pre-build sprint.

We recommend a Full SKU engagement with two specific pre-build weeks
focused on closing the evaluation and operational readiness gaps before
any production-bound code is written. Sprint Quote follows.

## Scope and method

The diagnostic was conducted on-site at NorthlineCo's Seattle office on
2026-04-15. Six stakeholders participated across the day: VP Operations
(sponsor), Director of IT, Tier-1 Support Lead, two senior field
operations staff, and the head of compliance.

The scoring instrument is BHIL's seven-dimension rubric, version 1.0.
Each dimension scores 0 to 4 against published anchor descriptions;
dimensions are equally weighted; composite is the sum.

## Per-dimension findings

### Dimension 1 — Use-case clarity (Score: 3/4)

NorthlineCo's use case is narrowly and clearly scoped: tier-1 support
questions from field operations, drawn from a known and bounded
knowledge base. The sponsor (VP Operations) can articulate the success
criterion in a single sentence: "Reduce average tier-1 response time
from 45 minutes to under 5 minutes for the 60% of questions covered
by our Confluence pages."

**Gap:** No clear deferred-use-cases list — no statement of what the
assistant explicitly will not handle. Risks scope creep in build.

### Dimension 2 — Data substrate (Score: 2/4)

The Confluence pages exist, are version-controlled, and have a clear
ownership model. The Zendesk historical ticket archive is queryable.

**Gap:** ~30% of Confluence pages are over 18 months old with no
ownership signal as to whether content is current. No tagging or
classification scheme. No PII inventory in the ticket archive.

### Dimension 3 — Integration readiness (Score: 2/4)

NorthlineCo runs a managed Slack workspace; the existing tier-1 support
flow is already Slack-channel-based. Slack admin permissions and bot
provisioning are well-understood.

**Gap:** No MCP server inventory. No defined trust tier for the future
assistant's tool access. Confluence access is via API key on a single
service account — no per-agent scoping possible without preliminary
work.

### Dimension 4 — Governance posture (Score: 3/4)

Strong area. NorthlineCo has a documented data classification policy,
an active risk committee that meets quarterly, and an existing
acceptable-use policy that maps cleanly onto AI assistant deployment.
The compliance lead is engaged and informed.

**Gap:** No AI-specific incident response protocol. No documented
escalation path for when the assistant produces an incorrect answer
that affects field operations.

### Dimension 5 — Evaluation discipline (Score: 1/4)

Weakest dimension. NorthlineCo has no eval harness. There is no
benchmark set of expected questions and expected answers. There is no
regression testing on knowledge-base changes. The sponsor's stated
success criterion (5-minute response time) is a latency metric, not
a correctness metric — and no correctness metric exists at all.

**Critical gap:** Without an eval harness, NorthlineCo will not be able
to detect quality regressions when Confluence pages change, when the
underlying model is upgraded, or when prompt revisions are made. This
is the single largest risk surface.

### Dimension 6 — Operational readiness (Score: 1/4)

NorthlineCo has on-call rotations for IT infrastructure but no on-call
or escalation path for AI-specific operational issues. There is no
defined rollback procedure for prompt or model changes. No incident
playbook for "the assistant gave a confidently-wrong answer that caused
a field operations error."

### Dimension 7 — Organizational readiness (Score: 2/4)

The sponsor is engaged and the IT director is supportive. The Tier-1
Support Lead has expressed concern about job impact — a legitimate
concern that has not yet been addressed in NorthlineCo's internal
communications planning.

**Gap:** No internal communications plan. No documented training plan
for field operations staff who will interact with the assistant. No
defined feedback mechanism.

## Composite

| Dimension                     | Score |
|-------------------------------|-------|
| 1. Use-case clarity           | 3/4   |
| 2. Data substrate             | 2/4   |
| 3. Integration readiness      | 2/4   |
| 4. Governance posture         | 3/4   |
| 5. Evaluation discipline      | 1/4   |
| 6. Operational readiness      | 1/4   |
| 7. Organizational readiness   | 2/4   |
| **Composite**                 | **14/28** |

Band: **Approaching Ready** (12–18 inclusive)

## Recommendations

1. **Two-week pre-build sprint** focused on evaluation discipline and
   operational readiness. This is non-negotiable in BHIL's view —
   building without an eval harness will produce a system that cannot
   safely evolve.
2. **Confluence content audit** — narrow scope to the ~70% of pages
   with current ownership; defer remaining content from initial launch.
3. **Internal communications plan** — written and shared before any
   pilot user is touched. Address the support lead's concern directly.
4. **Defined incident playbook** — with rollback procedure and named
   on-call.

Detailed scope for these items appears in the accompanying Sprint Quote.

## Sprint Quote reference

See `engagements/NL-2026-0341/sprint-quote.md` (delivered together with
this scorecard).

## Appendices

- Appendix A — Evidence inventory (interview notes, document
  references, observations) — `engagements/NL-2026-0341/appendix-a/`
- Appendix B — Diagnostic questionnaire used —
  `readiness/diagnostic-rubric.md` § Questionnaire
- Appendix C — Glossary — `readiness/diagnostic-rubric.md` § Glossary
