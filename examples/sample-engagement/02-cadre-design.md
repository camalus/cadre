---
engagement_id: NL-2026-0341-FULL
parent_engagement: NL-2026-0341
sku: Full
sku_price_usd: 22500
credit_applied_usd: 6500
net_price_usd: 16000
artifact_type: cadre-design
artifact_version: 1.0
designed_by: J. Hurd
designed_date: 2026-04-22
hitl_tier: 3
hitl_status: approved
---

# Cadre Design — NorthlineCo Full SKU Engagement

## Premise

The Express diagnostic (NL-2026-0341) converted to Full SKU within the
60-day credit window. Net price after credit: $16,000. This document
records the cadre design decision: which of the 20 agents activate, in
what sequence, and why.

## Stage activation summary

| Stage              | Active? | Justification                           |
|--------------------|---------|------------------------------------------|
| Research (VANTA)   | Limited | NorthlineCo provides own knowledge base; VANTA only confirms regulatory landscape. |
| Product (ATLAS)    | Full    | Build engagement requires PRD, specs, acceptance criteria, roadmap. |
| Operations (KEEL)  | Full    | Eval harness is the largest gap — KEEL central to closing it. |
| Governance (PULSE) | Full    | Standard activation regardless of sector. |

## Per-agent activation

### VANTA — Market Research (1 of 5 active)

| Agent                       | Active | Notes                              |
|-----------------------------|--------|------------------------------------|
| A01 Market Scout            | No     | No external scan needed.           |
| A02 Evidence Classifier     | Yes    | For client-supplied claims.        |
| A03 Competitive Mapper      | No     | No competitive workstream.         |
| A04 Source Archivist        | No     | No external sources to archive.    |
| A05 Synthesizer             | No     | Single-source synthesis trivial.   |

### ATLAS — Product (5 of 5 active)

| Agent                       | Active | Notes                              |
|-----------------------------|--------|------------------------------------|
| A06 PRD Author              | Yes    | Authoritative PRD for assistant.   |
| A07 Spec Decomposer         | Yes    | Breaks PRD into implementable specs.|
| A08 Acceptance Curator      | Yes    | Acceptance criteria — central to safe build. |
| A09 Roadmap Mapper          | Yes    | Roadmap including the 2-week pre-build sprint. |
| A10 Release Notes           | Yes    | For internal user-comms.           |

### KEEL — Operations (5 of 5 active)

| Agent                       | Active | Notes                              |
|-----------------------------|--------|------------------------------------|
| A11 Eval Runner             | Yes    | Closes the largest readiness gap.  |
| A12 Trace Auditor           | Yes    | Spot-audits A11 output.            |
| A13 Incident Responder      | Yes    | Authors NorthlineCo's first AI incident playbook. |
| A14 Cost Meter              | Yes    | Always active.                     |
| A15 Handoff Validator       | Yes    | Always active.                     |

### PULSE — Governance (5 of 5 active)

| Agent                       | Active | Notes                              |
|-----------------------------|--------|------------------------------------|
| A16 Policy Gatekeeper       | Yes    | Always active.                     |
| A17 HITL Router             | Yes    | Always active.                     |
| A18 PII Redactor            | Yes    | Routine redaction on artifacts before promotion. |
| A19 Audit Logger            | Yes    | Always active.                     |
| A20 Compliance Mapper       | Yes    | Map NorthlineCo's existing policies onto AI ops. |

**Activation count:** 16 of 20 agents.

## Sequence

The 10-step orchestration sequence runs as documented in
`prompts/P00-master-prompt.md`. Notable sequencing decisions:

1. **Steps 1–2** (charter read, readiness diag) — already completed in
   the parent Express engagement; we import the scorecard.
2. **Steps 3–7** (cadre design, handoff contracts, MCP wiring, memory
   scopes, HITL gates) — execute in week 1 of the Full engagement.
3. **Steps 8–9** (eval harness build, deployment runbook execution) —
   execute in weeks 2–4. Eval harness build is the largest single
   work item.
4. **Step 10** (synthesis and delivery) — week 5.

## Pre-build sprint (weeks 1–2)

Per the Sprint Quote, the first two weeks are pre-build: closing the
evaluation and operational gaps before any production code is written.
The cadre activation above is intentional — A11 (Eval Runner) and A13
(Incident Responder) are the lead agents during this phase.

## Cost envelope

| Stage              | Token budget (M) |
|--------------------|------------------|
| VANTA (limited)    | 0.4              |
| ATLAS              | 3.5              |
| KEEL               | 5.0              |
| PULSE              | 1.5              |
| Orchestration      | 1.6              |
| **Full SKU total** | **12.0**         |

## Reviewer roster (additions from Express)

For Full engagement, the roster expands:

| Tier | Reviewer            | Role         |
|------|---------------------|--------------|
| 1    | A. Patel (BHIL)     | Domain SME   |
| 1    | R. Kim (BHIL)       | Eval SME     |
| 2    | J. Hurd (BHIL)      | Operator     |
| 2    | NorthlineCo IT Dir. | Client SME   |
| 3    | J. Hurd (BHIL)      | Operator-prime |

Tier-2 client review is added because the engagement now produces
internal NorthlineCo deliverables that require client sign-off, not
just BHIL sign-off.

## Sign-off

| Party          | Name              | Date       |
|----------------|-------------------|------------|
| BHIL operator  | J. Hurd           | 2026-04-22 |
| Client sponsor | M. Chen (fict.)   | 2026-04-22 |
