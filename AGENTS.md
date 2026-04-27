# AGENTS.md — Cadre Roster Overview

*High-level orientation to the 20-agent cadre. For full per-agent specifications, see the squad subdirectories under `cadre/`.*

---

## Architecture summary

CADRE deploys a **Claude Opus 4.6/4.7 orchestrator** with **Claude Sonnet 4.6 subagents** organized into four squads. The orchestrator owns the engagement timeline, fans out parallel-safe tasks to subagents, serializes mutating actions, and writes filesystem artifacts at every handoff. Subagents read external state, return typed JSON Schema-validated payloads, and never call each other directly — all coordination flows through the orchestrator.

Per Anthropic's published research (Hadfield et al., June 13, 2025), this orchestrator-worker pattern delivers a 90.2% lift on internal research evals at roughly 15× single-agent token cost. Per Cognition's Walden Yan (June 12, 2025), the pattern fails the moment subagents make conflicting mutating decisions on shared state. CADRE's resolution is the **read/write asymmetry**: parallel reads are safe, parallel writes are serialized.

---

## The four squads

| Squad | Charter | Agents | Default Parallelism |
|---|---|---|---|
| **VANTA** | Market research and evidence handling | A01–A05 | Parallel-safe |
| **ATLAS** | Product specification and delivery cadence | A06–A10 | Mostly parallel-safe |
| **KEEL** | Runtime operations and engagement integrity | A11–A15 | Mixed |
| **PULSE** | Governance, compliance, and human oversight | A16–A20 | Serialized |

---

## VANTA — Market Research squad (A01–A05)

VANTA is the cadre's eyes on the outside world. All five VANTA agents are parallel-safe by default because they read external state and return classified evidence — they do not mutate anything except their own working directory.

- **A01 — Market Scout.** Web search and document retrieval against a structured research brief. Returns a citation graph.
- **A02 — Evidence Classifier.** Applies VERDICT-style classification (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE) to every claim. Hallucination defense layer.
- **A03 — Competitive Mapper.** Builds market maps, competitor matrices, and positioning grids from A01's evidence.
- **A04 — Source Archivist.** Snapshots sources to durable storage, records access dates, manages link rot.
- **A05 — Synthesizer.** Compresses VANTA outputs into a single executive brief for the orchestrator. The only VANTA agent that writes orchestrator-visible state.

---

## ATLAS — Product squad (A06–A10)

ATLAS turns research into shippable specifications. Most ATLAS agents are parallel-safe because they author independent artifacts; the exception is A09 (Roadmap Mapper), which is serialized because roadmap edits are mutating decisions on shared state.

- **A06 — PRD Author.** Drafts product requirements documents using the EARS notation pattern.
- **A07 — Spec Decomposer.** Breaks a PRD into typed user stories, acceptance criteria, and technical sub-specs.
- **A08 — Acceptance Curator.** Authors acceptance test scenarios and Gherkin-style behavior specs.
- **A09 — Roadmap Mapper.** *Serialized.* Maintains the canonical roadmap artifact; orchestrator routes all roadmap edits through this agent.
- **A10 — Release Notes.** Drafts release notes and changelog entries from completed roadmap items.

---

## KEEL — Operations squad (A11–A15)

KEEL is the runtime backbone. It runs evaluations, audits traces, responds to incidents, meters cost, and validates handoffs. Mixed parallelism — eval and audit are parallel-safe; incident response and cost metering are serialized because they mutate engagement-state.

- **A11 — Eval Runner.** Executes the eval harness against agent outputs. Parallel-safe.
- **A12 — Trace Auditor.** Reads OTel-compliant traces and flags anomalies. Parallel-safe.
- **A13 — Incident Responder.** *Serialized.* Owns the incident playbook; writes to engagement state.
- **A14 — Cost Meter.** *Serialized.* Tracks token spend, session-hours, and budget against engagement SLA.
- **A15 — Handoff Validator.** Validates JSON Schema strict-mode contracts at every inter-agent handoff. Parallel-safe.

---

## PULSE — Governance squad (A16–A20)

PULSE is the human-oversight layer. Every PULSE agent is serialized because governance decisions are inherently stateful — you cannot have two agents simultaneously deciding whether the same output meets the HITL gate. PULSE is also the squad most directly answerable to the case-law constraints in `governance/case-law-precedents.md`.

- **A16 — Policy Gatekeeper.** Holds the regulatory rulebook (EU AI Act, NIST AI RMF, ISO 42001, sector-specific obligations). Every agent action passes A16 before external release.
- **A17 — HITL Router.** Maps actions to HITL tiers (0–3) and routes to the assigned human reviewer.
- **A18 — PII Redactor.** Redacts personally identifiable information from agent outputs before logging or external release.
- **A19 — Audit Logger.** Maintains the immutable audit trail. Append-only log of every gated decision.
- **A20 — Compliance Mapper.** Maps engagement deliverables to the operator's compliance obligations (the cross-walk between agent output and regulator-facing reporting).

---

## How the squads work together

A typical engagement cycle:

1. **Orchestrator** receives a task from the operator.
2. **VANTA** is dispatched in parallel to gather evidence; returns a classified brief.
3. **ATLAS** is dispatched to draft specifications from VANTA's brief.
4. **KEEL** runs evals on every ATLAS output and audits traces continuously.
5. **PULSE** gates every external-facing action behind the appropriate HITL tier.
6. **Orchestrator** assembles the final deliverable, with **A19 (Audit Logger)** producing the trail.

No subagent calls another subagent directly. All coordination is mediated by the orchestrator and persisted to filesystem artifacts. This is what makes CADRE auditable.

---

## Per-agent specifications

Each agent has its own `.md` file inside the squad directory. The specification format is standardized — see `templates/agent-spec-template.md` for the schema. Every agent spec contains:

- **Charter** — one-paragraph statement of purpose
- **Inputs** — JSON Schema of accepted input
- **Outputs** — JSON Schema of returned artifact
- **Tools** — allowlisted tools (web_search, web_fetch, bash, str_replace, MCP server names, etc.)
- **Parallelism class** — `parallel-safe` or `serialized`
- **HITL tier** — 0, 1, 2, or 3
- **Model** — Opus (orchestrator only) or Sonnet (default subagents) or Haiku (cost-optimized routine work)
- **Memory scope** — `none`, `per-engagement`, or `cross-engagement`
- **Failure modes** — known anti-patterns and their mitigations
- **Citations** — primary sources for any claims the agent makes

---

## Configuring Claude Code

The Claude Code agent files in `.claude/agents/` are the executable counterparts to the specifications in `cadre/`. The specification files in `cadre/` are the *contract*; the files in `.claude/agents/` are the *runtime*. They must agree.

When you change an agent's tool allowlist, parallelism class, or HITL tier in `cadre/`, propagate the change to `.claude/agents/` in the same commit. The CI workflow in `.github/workflows/validate-handoffs.yml` checks that the two stay in sync.

---

*BHIL CADRE Framework — Cadre Roster — v1.0.0*
