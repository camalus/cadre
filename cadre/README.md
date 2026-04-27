# Cadre — 20-Agent Specification

*This directory contains the canonical specifications for the 20 agents that compose a CADRE deployment. Each squad has its own subdirectory with a squad README and 5 per-agent specifications.*

---

## Squad architecture

| Squad | Charter | Agents | Default Parallelism |
|---|---|---|---|
| [**VANTA**](squad-vanta-research/README.md) | Market research, evidence handling, competitive intelligence | A01–A05 | Parallel-safe |
| [**ATLAS**](squad-atlas-product/README.md) | Product specification and delivery cadence | A06–A10 | Mostly parallel-safe |
| [**KEEL**](squad-keel-operations/README.md) | Runtime operations and engagement integrity | A11–A15 | Mixed |
| [**PULSE**](squad-pulse-governance/README.md) | Governance, compliance, and human oversight | A16–A20 | Serialized |

---

## The agent roster

| ID | Name | Squad | Parallelism | HITL Tier | Model |
|---|---|---|---|---|---|
| A01 | Market Scout | VANTA | parallel-safe | 0 | Sonnet 4.6 |
| A02 | Evidence Classifier | VANTA | parallel-safe | 0 | Sonnet 4.6 |
| A03 | Competitive Mapper | VANTA | parallel-safe | 1 | Sonnet 4.6 |
| A04 | Source Archivist | VANTA | parallel-safe | 0 | Haiku 4.5 |
| A05 | Synthesizer | VANTA | parallel-safe | 1 | Sonnet 4.6 |
| A06 | PRD Author | ATLAS | parallel-safe | 1 | Sonnet 4.6 |
| A07 | Spec Decomposer | ATLAS | parallel-safe | 1 | Sonnet 4.6 |
| A08 | Acceptance Curator | ATLAS | parallel-safe | 1 | Sonnet 4.6 |
| A09 | Roadmap Mapper | ATLAS | **serialized** | 2 | Sonnet 4.6 |
| A10 | Release Notes | ATLAS | parallel-safe | 1 | Haiku 4.5 |
| A11 | Eval Runner | KEEL | parallel-safe | 0 | Sonnet 4.6 |
| A12 | Trace Auditor | KEEL | parallel-safe | 1 | Sonnet 4.6 |
| A13 | Incident Responder | KEEL | **serialized** | 2 | Sonnet 4.6 |
| A14 | Cost Meter | KEEL | **serialized** | 1 | Haiku 4.5 |
| A15 | Handoff Validator | KEEL | parallel-safe | 0 | Haiku 4.5 |
| A16 | Policy Gatekeeper | PULSE | **serialized** | 2 | Sonnet 4.6 |
| A17 | HITL Router | PULSE | **serialized** | 2 | Sonnet 4.6 |
| A18 | PII Redactor | PULSE | **serialized** | 2 | Sonnet 4.6 |
| A19 | Audit Logger | PULSE | **serialized** | 0 | Haiku 4.5 |
| A20 | Compliance Mapper | PULSE | **serialized** | 2 | Sonnet 4.6 |

---

## How to read an agent specification

Each agent has its own `.md` file inside the squad directory. Every spec follows the same structure:

1. **Frontmatter** — machine-readable metadata (ID, model, parallelism class, HITL tier, memory scope, tool allowlist, schema references)
2. **Charter** — one-paragraph statement of the agent's purpose
3. **Inputs / Outputs** — what the agent reads and writes (full schemas in `handoff-contracts/`)
4. **Tool allowlist** — itemized tools with rationale
5. **Parallelism class** — with justification
6. **HITL tier** — with justification, regulatory uplift, and named-reviewer pattern
7. **Memory scope** — with path-validation strategy
8. **Failure modes** — known anti-patterns and their mitigations
9. **Citations** — primary sources for any claims the agent makes

---

## Model assignment logic

- **Opus 4.6/4.7** — orchestrator only. The orchestrator handles cross-squad coordination, holistic synthesis, and the 1M-context window for whole-engagement reasoning.
- **Sonnet 4.6** — default for substantive subagents. Good intelligence-to-cost ratio; supports the parallel-safe research and authoring patterns.
- **Haiku 4.5** — cost-optimized routine work where speed and price matter more than depth. Used for A04 (Source Archivist), A10 (Release Notes), A14 (Cost Meter), A15 (Handoff Validator), A19 (Audit Logger).

Agents can be upgraded mid-engagement if their task complexity exceeds the assigned model's capacity. Downgrades are also permitted for routine subtasks. Document any deviation from the default in the engagement-specific agent spec under `engagements/<id>/agents/`.

---

## How agents coordinate

No subagent calls another subagent directly. **All coordination flows through the orchestrator.** This is non-negotiable and is what makes the cadre auditable.

A typical handoff:

1. Orchestrator dispatches Agent X with input written to `engagements/<id>/handoffs/X-input-<timestamp>.json`
2. Agent X reads the filesystem artifact, performs its task, writes its output to `engagements/<id>/handoffs/X-output-<timestamp>.json`
3. A15 (Handoff Validator) validates the output against X's output schema
4. A19 (Audit Logger) records the handoff
5. Orchestrator reads X's output and dispatches the next agent

Filesystem artifacts at every step. JSON Schema strict mode validation at every step. Audit log entry at every step.

---

## When to override defaults

The defaults in this directory are tuned for a generic engagement. Sector-specific or jurisdiction-specific engagements override them in the per-engagement `engagements/<id>/agents/` directory:

- **Healthcare (HIPAA)**: A18 PII Redactor scope expands to the 18 HIPAA Safe Harbor identifiers; memory scopes for any agent reading PHI are forced to `per-engagement`.
- **Finance (SR 11-7 / OCC 2011-12)**: A11 Eval Runner adds model-risk-management criteria; A19 Audit Logger retention extends to 7 years.
- **Hiring (NYC AEDT, EU AI Act high-risk Annex III)**: A17 HITL Router enforces Tier 3 on any decision affecting an applicant.
- **Biometric / EU**: Tier 3 mandatory on any biometric ID decision.

The override pattern is documented in SP-02. The canonical specs in this directory are the starting point, not the endpoint.

---

*BHIL CADRE Framework — Cadre Directory — v1.0.0*
