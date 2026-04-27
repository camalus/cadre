# HITL Policy

*Tier 0–3 taxonomy, SLO defaults, and reviewer roster discipline. This document is the contract between the cadre's automation and the operator's human oversight function.*

---

## The four tiers

CADRE classifies every action into one of four tiers. The tier determines whether human review is required, the SLO for that review, and the consequences if the SLO is breached.

### Tier 0 — Mechanical, no human review
- **Examples:** A19 Audit Logger appending an entry; A14 Cost Meter recording a token usage; an agent reading a per-engagement file
- **Review required:** none
- **Audit:** logged through A19; A12 Trace Auditor sample-audits patterns periodically
- **Failure handling:** Tier 0 actions either succeed mechanically or trigger an incident; there is no human-judgment fallback

### Tier 1 — Internal, human-aware but not human-gated
- **Examples:** Routine agent outputs that flow within the cadre but not externally; eval results published to internal dashboards
- **Review required:** aware human; can be batched
- **SLO:** acknowledgment within 4 hours of business day
- **Audit:** logged through A19; reviewer acknowledgment recorded
- **Failure handling:** SLO breach triggers an A13 Incident Responder ticket but does not block the action

### Tier 2 — External or consequential, human-gated
- **Examples:** Client-facing deliverables; A16 policy verdicts; A18 redaction outputs destined for external release; A20 compliance maps for regulator filings
- **Review required:** named reviewer with relevant role/jurisdiction/sector competency
- **SLO:** decision within 24 hours of routing
- **Audit:** logged through A19; reviewer decision recorded with rationale
- **Failure handling:** SLO breach triggers escalation to next reviewer in the path; the action is held until decision is recorded

### Tier 3 — High-stakes, multi-reviewer
- **Examples:** Decisions affecting individuals (hiring, lending, healthcare access); regulator filings; public statements; cadre policy or rulebook changes
- **Review required:** at least two reviewers; named compliance officer is one of them
- **SLO:** decision within 72 hours of routing; expedited paths defined for time-sensitive cases
- **Audit:** logged through A19; both reviewers' decisions and rationales recorded
- **Failure handling:** SLO breach is a Sev-2 incident; the action is held; operator's compliance function is notified

---

## Tier assignment per action type

| Action type | Default tier | Notes |
|---|---|---|
| Internal agent-to-agent handoff | Tier 0 | Schema-validated; no review |
| Cadre internal report | Tier 1 | Aware reviewer can spot-check |
| Client-facing draft (any) | Tier 2 | Reviewer required before delivery |
| Client-facing final | Tier 2 | Same reviewer or designated deputy |
| Decision affecting an individual | Tier 3 | Two reviewers; compliance officer is one |
| Regulator filing | Tier 3 | Two reviewers; compliance officer signs |
| Cadre rulebook update | Tier 3 | Two reviewers; CHANGELOG entry; A19 logged |
| Cross-engagement memory promotion | Tier 2 | One reviewer, but rigorously logged |
| External public statement | Tier 3 | Compliance + legal review |

These are defaults. Engagement-specific overrides are documented in `engagements/<id>/hitl-overrides.md` and are themselves Tier 2 changes.

---

## Reviewer roster discipline

The reviewer roster is operator-maintained and lives in operator infrastructure (not in CADRE's repository). The roster contains:

- **Role label** (e.g., "Compliance Officer — EU Region")
- **Jurisdiction competencies** (which jurisdictions this reviewer is qualified to review)
- **Sector competencies** (healthcare, finance, hiring, general)
- **Current load** (how many open reviews)
- **Availability** (out-of-office, on-call status)
- **Escalation path** (who to escalate to if this reviewer is unavailable)

The roster does **not** contain personal identifying information (no names, no email addresses, no phone numbers). Personal identifiers are resolved by the operator's identity infrastructure at notification time. This is a deliberate decoupling — the roster is auditable, the personal identifiers are not in the audit chain.

A17 HITL Router reads the roster at routing time. Routing logic prioritizes:

1. Jurisdiction match (a Tier 2 action affecting EU subjects routes to an EU-jurisdiction reviewer)
2. Sector match (a healthcare action routes to a HIPAA-competent reviewer)
3. Role match (a regulator-filing action routes to a Compliance Officer, not to a Technical Reviewer)
4. Load balancing (within the matching set, prefer the lightest-loaded reviewer)
5. Availability (skip unavailable reviewers; escalate per their escalation path)

---

## SLO breach handling

When a Tier 2 or Tier 3 SLO is breached:

- **A13 Incident Responder** opens a ticket
- **A17 HITL Router** escalates per the reviewer's escalation path
- **A19 Audit Logger** records the breach as a `slo_breach` event
- **A20 Compliance Mapper** includes breach statistics in compliance reports

Breach rates are a measured metric. Operators with chronic Tier 2 or Tier 3 breach rates above 5% should investigate roster sufficiency, reviewer load, or whether their tier-assignment defaults are over-routing.

---

## Override discipline

Reviewers can override A16 policy verdicts (e.g., approve a `gate` verdict to proceed, or block a `pass` verdict). Overrides are governed:

- Override rationale is required (free-text, mandatory)
- Override is logged through A19 with the reviewer's role identifier
- Overrides above a threshold (operator-configurable, default >10% of decisions) trigger A12 Trace Auditor sampling
- Repeated overrides on similar actions indicate either a rulebook gap (escalate to A20 for catalog update) or a reviewer training gap

Overrides are not a bug. They are the safety valve that prevents A16 from over-blocking. But they are **monitored**, because the same mechanism could enable rubber-stamping.

---

## What HITL is not

- **Not a guarantee.** Human reviewers make mistakes. HITL reduces error rates compared to fully autonomous deployment but does not eliminate them. The 2024 Air Canada case (Moffatt v. Air Canada, 2024 BCCRT 149) included human-aware AI deployments that still produced operator liability. [VERIFIED]
- **Not optional.** "We'll add HITL later" is not a CADRE deployment. The diagnostic flags this in Dimension 4 scoring.
- **Not theatrical.** HITL routing must produce real notifications to real, accountable humans within real SLOs. A17's design assumes this and the audit chain enforces it.
- **Not a substitute for governance.** HITL is one element of governance, alongside regulatory mapping, audit chain integrity, evidence classification discipline, and memory policy.

---

## Citations

- EU AI Act, Article 14 — human oversight obligations.
- NIST AI Risk Management Framework 1.0 + Generative AI Profile — MEASURE function emphasizes human-AI configuration.
- ISO/IEC 42001:2023 — AI management systems.
- Moffatt v. Air Canada, 2024 BCCRT 149. [VERIFIED]
- BHIL ADR Blueprint — review-discipline benchmark.

---

*BHIL CADRE Framework — governance/hitl-policy.md — v1.0.0*
