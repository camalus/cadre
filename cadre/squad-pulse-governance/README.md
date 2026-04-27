# Squad PULSE — Governance

*PULSE is the cadre's vital-signs monitoring layer — the governance, compliance, and human-oversight squad. The name is intentional: a pulse reflects the cadre's regulatory and ethical health at any moment. Every PULSE agent is serialized because governance decisions are inherently stateful.*

---

## Charter

PULSE is the squad most directly answerable to the **case-law constraints** in `governance/case-law-precedents.md` (Air Canada Moffatt v. Air Canada, 2024 BCCRT 149; iTutor Group EEOC settlement, 2023; Klarna AI deployment reversal, 2025). Operator liability for agent output is real and adjudicated. PULSE is what makes the cadre defensible against that liability.

The squad's responsibilities span the governance lifecycle:

1. **Policy** — A16 Policy Gatekeeper holds the regulatory rulebook (EU AI Act, NIST RMF, ISO 42001, sector-specific obligations)
2. **Routing** — A17 HITL Router maps actions to tiers and routes to named reviewers
3. **Privacy** — A18 PII Redactor strips PII before logging or external release
4. **Audit** — A19 Audit Logger maintains the immutable audit trail (append-only)
5. **Mapping** — A20 Compliance Mapper produces the cross-walk between cadre output and regulator-facing reporting

---

## Roster

| ID | Name | Role |
|---|---|---|
| [A16](A16-policy-gatekeeper.md) | Policy Gatekeeper | Holds the regulatory rulebook; gates every external-facing action against policy |
| [A17](A17-hitl-router.md) | HITL Router | Maps actions to tiers and routes to assigned human reviewers |
| [A18](A18-pii-redactor.md) | PII Redactor | Redacts PII from agent outputs before logging or external release |
| [A19](A19-audit-logger.md) | Audit Logger | Maintains the immutable, append-only audit trail |
| [A20](A20-compliance-mapper.md) | Compliance Mapper | Maps deliverables to the operator's compliance obligations |

---

## Why all PULSE agents are serialized

Every PULSE agent runs serialized. This is the most distinctive parallelism choice in the cadre and deserves explicit justification:

- **A16 Policy Gatekeeper** — policy decisions are stateful. Two A16 instances simultaneously deciding whether the same output meets the same policy produce inconsistent verdicts.
- **A17 HITL Router** — routing decisions are stateful. Two A17 instances simultaneously routing the same action to different reviewers produces conflict.
- **A18 PII Redactor** — redaction operates on shared state (the output being redacted). Concurrent redaction of the same payload produces races.
- **A19 Audit Logger** — append-only logs require single-writer discipline to maintain integrity. Concurrent appends without synchronization produce out-of-order or duplicated entries.
- **A20 Compliance Mapper** — compliance mappings are stateful. The mapping for engagement N depends on the mapping decisions made for engagement N-1.

The cost of serialization is acceptable because PULSE's work is lightweight relative to VANTA and ATLAS. PULSE typically consumes 5–10% of total engagement spend.

---

## Coordination pattern

PULSE agents fire as policy boundaries:

- **A16** fires before any external-facing action; gate or pass
- **A17** fires when an action requires HITL routing; assigns reviewer; tracks state
- **A18** fires before any output enters the audit log or reaches an external party
- **A19** fires after every gated decision; appends to the trail
- **A20** fires periodically to produce the regulatory cross-walk

The orchestrator dispatches PULSE agents at policy boundaries — they are not part of the substantive work product flow, they are the discipline applied to it.

---

## HITL discipline within PULSE

PULSE is mostly Tier 2 — its actions affect external stakeholders, regulators, or audit records. Two exceptions:

- **A19 Audit Logger** — Tier 0. Audit logging is mechanical and append-only; no human review required for the logging itself.
- **A20 Compliance Mapper** — Tier 2 because compliance maps drive client-facing regulator interactions.

A16 Policy Gatekeeper itself is Tier 2 because gate decisions affect what the cadre is allowed to do. A17 HITL Router is Tier 2 because routing decisions assign work to specific humans.

---

## Memory scope

- **A16, A17, A18** — `cross-engagement` for rulebooks, redaction patterns, and policy templates; `per-engagement` for client-specific exceptions and per-engagement decisions
- **A19** — `cross-engagement` for the audit log infrastructure; `per-engagement` for the engagement's specific log entries
- **A20** — `cross-engagement` for compliance mapping templates; `per-engagement` for the engagement's specific mappings

The cross-engagement scopes are essential here — PULSE's value compounds. Rulebooks, redaction patterns, and audit templates that work for engagement N work for engagement N+1, with marginal client-specific tuning. The path-validation rule applies; cross-engagement memory is read at `cross-engagement/A##/` and written only by an explicit "promote learnings" workflow that requires human review.

---

## Common failure modes (squad-level)

- **Policy gatekeeper bypass.** Cadre actions that don't pass through A16 because the orchestrator forgot to route them. Mitigation: A15 Handoff Validator checks for "policy_check_id" in any externally-facing payload; missing field is a blocker.
- **HITL routing without reviewer notification.** A17 routing an action to a reviewer who isn't notified. Mitigation: routing emits a notification artifact; A11 Eval Runner verifies notification was sent.
- **PII redaction gaps.** A18 missing PII patterns for a sector or jurisdiction. Mitigation: redaction patterns versioned; sector-specific patterns required for healthcare (HIPAA Safe Harbor 18), finance, hiring.
- **Audit log truncation.** A19 silently dropping log entries due to storage pressure. Mitigation: A14 Cost Meter monitors audit log storage; storage pressure triggers an incident, never silent drop.
- **Compliance map drift.** A20 maps that don't get updated when regulations change. Mitigation: A20 maps are versioned by regulatory effective date; review cadence is quarterly.

---

## Citations

- EU AI Act, Articles 14 (human oversight) and 26 (deployer obligations). Official Journal L 2024/1689, July 12, 2024.
- NIST AI Risk Management Framework 1.0, January 2023; Generative AI Profile, July 2024.
- ISO/IEC 42001:2023 — AI management systems.
- Colorado AI Act (SB24-205) — effective date subject to revision.
- Moffatt v. Air Canada, 2024 BCCRT 149.
- iTutor Group EEOC settlement, 2023.
- Klarna AI deployment reversal, 2025.

---

*BHIL CADRE Framework — PULSE Squad — v1.0.0 — All Serialized*
