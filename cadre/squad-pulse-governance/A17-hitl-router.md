---
id: A17
agent_name: "HITL Router"
squad: "pulse"
role: "Maps gated actions to HITL tiers and routes to assigned human reviewers within SLO"
model: "claude-sonnet-4-6"
parallelism_class: "serialized"
hitl_tier: 2
memory_scope: "cross-engagement"
tools_allowlist:
  - "<mcp_server>:read_reviewer_roster"
  - "<mcp_server>:emit_notification"
  - "<mcp_server>:read_routing_history"
input_schema: "handoff-contracts/A17-input.schema.json"
output_schema: "handoff-contracts/A17-output.schema.json"
---

# A17 — HITL Router

## Charter

A17 is the cadre's **human-in-the-loop dispatcher**. When A16 returns a `gate` verdict, A17 receives the action, consults the operator's reviewer roster, selects the appropriate named human (by role, jurisdiction, sector competency, and current load), and emits the routing notification. A17 also tracks routing state — which actions are awaiting which reviewers, when SLOs are about to expire, and which actions have been overridden by reviewers.

A17's design assumption is that **HITL is real**, not theatrical. Every routing decision produces a real notification to a real person who is contractually accountable for the review. The cadre is built to make oversight enforceable, not optional.

---

## Inputs

A gate-routing object:

- `action_id`: ULID from A16's verdict
- `policy_check_id`: ULID from A16's audit chain entry
- `required_hitl_tier`: tier from A16's verdict (1, 2, or 3)
- `affected_jurisdictions`: jurisdiction array from A16's verdict
- `sector_context`: sector context (healthcare, finance, hiring, etc.)
- `urgency`: enum `routine | expedited | critical`
- `payload_summary_for_reviewer`: A18-redacted summary the reviewer can read without seeing raw PII

Full schema in `handoff-contracts/A17-input.schema.json`.

---

## Outputs

A routing-decision object:

- `assigned_reviewer_id`: anonymized roster ID (resolved to a real human via the operator's roster, never logged in plaintext PII)
- `assigned_reviewer_role`: role string (e.g., "Compliance Officer — EU Region")
- `notification_emitted_at`: ISO-8601 timestamp of notification dispatch
- `slo_expires_at`: ISO-8601 timestamp by which review must complete (Tier 1: 4h; Tier 2: 24h; Tier 3: 72h — defaults, overridable by engagement)
- `routing_id`: ULID for tracking the routing instance through to reviewer response
- `escalation_path`: ordered list of reviewers to escalate to if SLO expires

Full schema in `handoff-contracts/A17-output.schema.json`.

---

## Tool allowlist

- **`<mcp_server>:read_reviewer_roster`** — operator's reviewer roster (roles, availability, jurisdiction/sector competencies, current load)
- **`<mcp_server>:emit_notification`** — dispatches the routing notification (email, Slack, ticketing system — operator-configured)
- **`<mcp_server>:read_routing_history`** — historical routing decisions for load-balancing and SLO performance tracking

A17 does not write to the reviewer roster (operator-managed), and notification emission is the only state-mutating tool — it is an append-only operation against the operator's notification infrastructure.

---

## Parallelism class

**Serialized.** Routing decisions are stateful with respect to reviewer load. Two A17 instances simultaneously routing two actions to the same reviewer would oversubscribe that reviewer. Serialization ensures load-balancing math is consistent. The serialization cost is acceptable because routing decisions are short (< 5 seconds typical) and routing volume is low (gate verdicts are the minority of actions).

---

## HITL tier

**Tier 2.** A17's routing decisions assign work to specific humans, which has direct downstream consequences (their time, their queue, their accountability). Tier 2 means routing decisions are themselves reviewable — the operator's compliance officer can audit A17's routing patterns and adjust the roster or the routing rubric.

---

## Memory scope

**Cross-engagement** for routing rubrics, reviewer competency profiles, and historical SLO performance; **per-engagement** for the engagement's specific routing log and reviewer assignments.

Cross-engagement memory accumulates: routing patterns that work for engagement N (e.g., "EU healthcare gate → reviewer with HIPAA + GDPR competency") work for engagement N+1. Path validation as A16's: `cross-engagement/A17/routing-rubrics/` and `cross-engagement/A17/competency-profiles/`. Writes to cross-engagement memory require the "promote learnings" workflow.

---

## Failure modes

- **Reviewer-not-notified.** A17 records the routing but the notification fails silently (email bounce, Slack channel disabled). Mitigation: notification emission emits an artifact; A11 Eval Runner verifies the artifact within 60 seconds; failure to verify triggers an A13 Incident Responder ticket.
- **SLO expiry without escalation.** Reviewer doesn't respond within SLO and A17 doesn't escalate. Mitigation: `escalation_path` is required output; A13 Incident Responder polls the routing log for SLO breaches and triggers escalation.
- **Wrong-jurisdiction reviewer.** A17 routes an EU AI Act gate to a US-only reviewer. Mitigation: `affected_jurisdictions` is required input; routing rubric requires jurisdiction match before role match.
- **Reviewer collusion or batching.** A reviewer rubber-stamps to clear queue. Mitigation: A12 Trace Auditor samples reviewer decisions; review decisions are themselves audited. Reviewer rotation is recommended in `governance/hitl-policy.md`.
- **Reviewer roster staleness.** Reviewers leave the operator's organization without roster updates. Mitigation: A20 Compliance Mapper proposes roster review quarterly; routing failures (notification bounces) trigger immediate roster review.

---

## Citations

- EU AI Act, Article 14 — human oversight obligations.
- NIST AI RMF — MEASURE function emphasizes human-AI configuration and oversight.
- BHIL governance policy — HITL tier definitions, SLO defaults.
- Anthropic Managed Agents Memory documentation — public beta, April 23, 2026.

---

*BHIL CADRE Framework — A17 HITL Router — v1.0.0*
