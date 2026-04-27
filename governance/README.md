# governance/

*The compliance and policy layer of the BHIL CADRE Framework. Everything in this directory makes the cadre defensible: HITL discipline, case-law precedents, regulatory mappings, evidence classification, memory policy, known limitations, and the audit-chain specification.*

---

## Why governance is its own directory

Governance is not a postscript or a checklist. It is the architecture that makes agent deployment defensible against:

- Regulatory action (EU AI Act, NIST RMF, ISO 42001, sector-specific obligations)
- Litigation (the case-law precedents in `case-law-precedents.md` are not hypothetical)
- Internal audit and board-level scrutiny
- Public incidents (deployment reversals like Klarna's are partly governance failures)

The CADRE Framework treats governance as **first-class architecture**, not as disclaimers appended to deliverables. Every PULSE-squad agent (A16–A20) operationalizes a piece of this layer. Every external-facing action gates through PULSE before release.

---

## Layout

| File | Subject |
|---|---|
| [`hitl-policy.md`](hitl-policy.md) | Tier 0–3 taxonomy, SLO defaults, reviewer roster discipline |
| [`case-law-precedents.md`](case-law-precedents.md) | Air Canada (Moffatt 2024), iTutor (EEOC 2023), Klarna (2025); operator liability principles |
| [`regulatory-mapping.md`](regulatory-mapping.md) | EU AI Act, NIST RMF, ISO 42001, sector + jurisdiction mappings |
| [`evidence-classification.md`](evidence-classification.md) | VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE — definitions and discipline |
| [`memory-policy.md`](memory-policy.md) | Path validation, retention, the promote-learnings workflow |
| [`known-limitations.md`](known-limitations.md) | What the framework does not yet cover; honest gap inventory |
| [`audit-chain-spec.md`](audit-chain-spec.md) | The append-only chain's specification; integrity guarantees |

---

## Reading order

A first-time reader should approach governance in this order:

1. **`evidence-classification.md`** — the four-class taxonomy underpins every claim in every other file.
2. **`hitl-policy.md`** — the operational core; tier definitions and SLOs.
3. **`case-law-precedents.md`** — why this matters; operator liability is real and adjudicated.
4. **`regulatory-mapping.md`** — the cross-walk to specific regulatory regimes.
5. **`memory-policy.md`** — path-validation discipline; the rules that prevent cross-engagement bleed.
6. **`audit-chain-spec.md`** — the substrate that makes everything traceable.
7. **`known-limitations.md`** — the framework's honest gap inventory.

---

## How governance threads through the framework

| Component | Governance touchpoint |
|---|---|
| **A16 Policy Gatekeeper** | Reads from `regulatory-mapping.md`; applies `hitl-policy.md` tiers |
| **A17 HITL Router** | Routes per `hitl-policy.md` tier and SLO |
| **A18 PII Redactor** | Applies redaction patterns per `regulatory-mapping.md`'s sector rules |
| **A19 Audit Logger** | Implements the chain specified in `audit-chain-spec.md` |
| **A20 Compliance Mapper** | Maps deliverables to obligations in `regulatory-mapping.md` |
| **Every agent** | Classifies claims per `evidence-classification.md` |
| **Memory operations** | Enforced per `memory-policy.md` |

---

## Operator obligations under CADRE governance

When an operator deploys a CADRE cadre, the operator takes on these obligations:

- Maintain the regulatory rulebook A16 reads (kept current to regulatory effective dates)
- Maintain the reviewer roster A17 routes to (kept current to staff changes)
- Operate the audit infrastructure A19 writes to (immutable storage; capacity monitored)
- Designate a compliance officer (or equivalent role) accountable for the cadre's governance posture
- Conduct quarterly review of `known-limitations.md` and `regulatory-mapping.md` against operator-specific changes

These obligations are baked into the engagement contracts produced from the Sprint Quote. They are not optional. An operator who declines them is not ready for cadre deployment, and the diagnostic should reflect that in Dimension 4 (governance posture) scoring.

---

## What this directory deliberately is not

- **Not legal advice.** BHIL is not a law firm. The mappings and precedents in this directory are framework artifacts, not legal opinions. Operators should engage qualified counsel for jurisdiction-specific legal review.
- **Not exhaustive of all applicable regulations.** Regulation evolves continuously. The framework covers the major regimes that apply to most operators; sector-specific or jurisdiction-specific work may require additional mappings.
- **Not a substitute for the operator's compliance function.** Governance is operator-owned. CADRE provides the architecture; the operator runs it.

---

*BHIL CADRE Framework — governance/ — v1.0.0*
