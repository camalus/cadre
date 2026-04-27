---
id: CADRE-SP-06
title: "SP-06 — HITL Governance"
version: "1.0"
type: sub-prompt
sequence: 6
input_artifacts: ["agents/A##-*.md", "cadre-blueprint.md"]
output_artifact: "hitl-gate-map.md"
hitl_tier: 3
---

# SP-06 — HITL Governance

*Maps every agent action to a Human-in-the-Loop tier (0–3) and assigns named human reviewers. Outputs `hitl-gate-map.md`. This is the most consequential prompt in the sequence — it determines what the cadre is and is not allowed to do without human authorization.*

---

## Purpose

CADRE's central commercial defensibility comes from its HITL discipline. The case-law precedents in `governance/case-law-precedents.md` (Air Canada Moffatt v. Air Canada, 2024 BCCRT 149; iTutor Group EEOC settlement, 2023; Klarna AI deployment reversal, 2025) make clear that operator liability for agent output is real and adjudicated. SP-06 is where the engagement makes its HITL discipline explicit and traceable.

---

## Inputs

- **`engagements/<id>/agents/A##-*.md`** — agent specs from SP-02
- **`engagements/<id>/cadre-blueprint.md`** — sector and jurisdiction
- **`governance/hitl-tier-taxonomy.md`** — the tier definitions
- **`governance/eu-ai-act-mapping.md`**, `nist-ai-rmf-mapping.md`, `iso-42001-mapping.md`, `colorado-ai-act-notes.md` — regulatory requirements
- The engagement brief's `human_reviewers` list — named humans available for Tier 1+ gates

---

## Output

**`engagements/<id>/hitl-gate-map.md`** — the canonical HITL gate map. For each agent action, the document specifies:

- The action being gated
- The Cynefin domain (Clear / Complicated / Complex / Chaotic)
- The HITL tier (0 / 1 / 2 / 3)
- The named reviewer (Tier 1+) or pair of reviewers (Tier 3)
- The regulatory basis (which articles, clauses, or precedents drive this tier)
- The escalation path if the reviewer is unavailable

---

## The tier taxonomy (canonical reference)

| Tier | Description | When to use |
|---|---|---|
| **0 — No gate** | Agent output flows without human review | Cynefin Clear, internal-only, idempotent reads, no third-party impact |
| **1 — Single-human review** | Agent output reviewed by one named human before persistence | Cynefin Complicated, internal mutating writes, low third-party impact |
| **2 — Single-human approval before action** | Agent output gated; action does not proceed until one named human approves | Any external-facing communication, any decision affecting an identifiable third party, Cynefin Complex |
| **3 — Two-human verification** | Agent output requires two independent named humans to approve | Legal/financial consequence, biometric ID, termination, wire transfer, regulator correspondence, adverse-action notices, GDPR Article 22 automated decisions, Cynefin Chaotic |

The full taxonomy lives in `governance/hitl-tier-taxonomy.md`.

---

## Step-by-step

### Step 1 — Enumerate agent actions

For each in-scope agent, list every action it can take. An "action" is a discrete operation that produces an output the orchestrator might persist or send externally. A single agent typically has 3–10 actions. Examples:

- A01 Market Scout: "execute_research_query", "fetch_url", "snapshot_source"
- A06 PRD Author: "draft_prd_section", "revise_prd_from_feedback", "finalize_prd"
- A13 Incident Responder: "classify_incident", "execute_runbook_step", "notify_oncall", "close_incident"
- A17 HITL Router: "route_to_reviewer", "escalate_unavailable_reviewer", "record_decision"

### Step 2 — Classify each action by Cynefin domain

For each action, decide which Cynefin domain it operates in. The same agent can have actions in different domains. Example: A06 PRD Author's "draft_prd_section" might be Complicated (good practice with established patterns), while its "finalize_prd" might be Complex (the finalization decision depends on emergent stakeholder feedback that cannot be fully specified in advance).

### Step 3 — Determine baseline tier from Cynefin

Apply the canonical mapping:

- Clear → Tier 0
- Complicated → Tier 1
- Complex → Tier 2
- Chaotic → Tier 3

This is the **floor**. Regulatory and contractual obligations may raise it.

### Step 4 — Apply regulatory uplift

Check each action against the regulatory mappings:

- **EU AI Act Article 14** (high-risk AI systems must have human oversight) — minimum Tier 2 for any high-risk system action, Tier 3 for biometric ID
- **EU AI Act Article 26** (deployer obligations) — minimum Tier 2 for any deployer-facing decision affecting EU data subjects
- **NIST AI RMF Govern function** — recommends Tier 2 for any externally-impactful AI decision
- **ISO 42001 Clauses 4–10** — requires documented oversight for AI management system; aligns with Tier 1+ floor
- **Colorado AI Act** (effective June 30, 2026 or January 1, 2027) — requires human review for any "consequential decision" by a "high-risk AI system"
- **NYC AEDT** — requires bias audit and candidate notification; minimum Tier 2 for hiring decisions
- **GDPR Article 22** — automated individual decision-making with legal/significant effects requires meaningful human intervention; minimum Tier 3
- **Healthcare HIPAA** — Tier 2 for any PHI exposure decision; Tier 3 for treatment recommendations
- **Finance SR 11-7 / OCC 2011-12** — Tier 2 for any model-driven decision affecting consumers; Tier 3 for credit denial / adverse action

### Step 5 — Apply case-law uplift

Specific patterns flagged by precedent:

- **External communication that could be construed as a binding statement** (Air Canada Moffatt) — Tier 2 minimum
- **Hiring or candidate evaluation decisions** (iTutor) — Tier 2 minimum, often Tier 3 for adverse decisions
- **Customer-facing AI agents replacing humans entirely** (Klarna reversal) — operator must demonstrate Tier 1+ for the reversal pattern; Klarna's lesson is that wholesale replacement without HITL was reversed within a year

### Step 6 — Assign named reviewers

For every Tier 1+ action, name the human reviewer. Use the `human_reviewers` list from the engagement brief. For Tier 3, name two reviewers and confirm they have independent reporting lines (the spirit of two-human verification is independence, not just count).

If a tier requires more reviewers than the engagement has named, escalate. Operating without named reviewers is a defect — defaulting to "the operator" is unacceptable for Tier 2+ actions.

### Step 7 — Define escalation paths

For every named reviewer, define what happens if they're unavailable. Options:

- Named alternate reviewer (preferred)
- Hold the action for a stated duration (e.g., 4 hours) before escalating
- Refuse the action (default if no alternate)

Tier 3 actions never proceed without two reviewers; "hold and escalate" is the only acceptable pattern.

### Step 8 — Write `hitl-gate-map.md`

Use `templates/hitl-gate-template.md` as the scaffold. The output is a structured document with one row per agent action.

---

## Quality criteria

- [ ] Every in-scope agent has every action enumerated
- [ ] Every action has a Cynefin classification with rationale
- [ ] Every action has a HITL tier with regulatory and/or case-law citation
- [ ] Every Tier 1+ action has a named reviewer
- [ ] Every Tier 3 action has two named reviewers with independent reporting lines
- [ ] Every named reviewer has an escalation path
- [ ] No action defaults to Tier 0 without explicit "no third-party impact" justification

---

## Common failure modes

- **Defaulting everything to Tier 0 because "the agent is good."** This is the iTutor / Air Canada / Klarna failure pattern. Tier 0 is the exception, not the default.
- **Naming "the operator" as the reviewer.** This is unspecific. Name a person.
- **Tier 3 with two reviewers in the same reporting line.** Defeats the purpose. Independence matters.
- **Skipping regulatory uplift because "we'll add it later."** The regulatory uplift is the engagement's defense in a dispute. Add it now.
- **No escalation path.** Reviewers go on vacation. Plan for it.

---

## Citations

- EU AI Act, Articles 14 (human oversight) and 26 (deployer obligations). Official Journal L 2024/1689, July 12, 2024.
- NIST AI Risk Management Framework 1.0, January 2023; Generative AI Profile, July 2024.
- ISO/IEC 42001:2023 — AI management systems.
- Colorado AI Act (SB24-205), enacted May 17, 2024; effective date subject to revision (currently June 30, 2026; proposed rewrite to January 1, 2027).
- NYC Local Law 144 (Automated Employment Decision Tools), effective July 5, 2023.
- GDPR Article 22 (Regulation (EU) 2016/679).
- Moffatt v. Air Canada, 2024 BCCRT 149.
- iTutor Group EEOC settlement, 2023 (~$365,000).
- Snowden, D. & Boone, M. *A Leader's Framework for Decision Making.* HBR, November 2007.

---

*BHIL CADRE Framework — SP-06 — v1.0.0*
