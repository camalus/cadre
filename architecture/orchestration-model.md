# Orchestration Model

*The CADRE Framework's central design thesis — and the document that resolves the apparent contradiction between Anthropic's "multi-agent research wins" finding and Cognition's "don't build multi-agent systems" warning.*

---

## The thesis in one sentence

**Parallel reads are safe; parallel writes must be serialized.**

This rule reconciles the empirical evidence:

- Anthropic's June 2025 multi-agent research system showed Opus orchestrator + Sonnet subagents achieve a 90.2% lift over single-agent Opus on internal evaluation, at roughly 15× the token cost. [UNCORROBORATED — vendor-published]
- Cognition's 2025 "Don't build multi-agent systems" essay documented production failures where parallel writes diverged irreconcilably, the orchestrator could not reconcile conflicting state, and the system became less reliable than a single agent.

Both findings are correct, applied to different problem classes. Research is read-heavy: subagents fetch sources, summarize them, return citation graphs. The fan-out is naturally idempotent — multiple subagents reading the web do not corrupt each other's state. Production engineering work (the kind Cognition observed failing) is write-heavy: subagents propose code changes, infrastructure mutations, file edits — all of which conflict if attempted in parallel.

The CADRE Framework explicitly classifies every agent's parallelism as either `parallel-safe` (read-only or pure-function over independent inputs) or `serialized` (mutates shared state). The orchestrator dispatches accordingly.

---

## The orchestrator role

CADRE uses **Opus 4.7** as the orchestrator (Opus 4.6 is acceptable for cost-sensitive deployments). The orchestrator does not perform substantive work itself — it dispatches subagents and reconciles their outputs. Its responsibilities:

1. **Parse the engagement brief** into a directed acyclic plan of subagent tasks
2. **Classify dispatches** as parallel-safe (fan out) or serialized (queue)
3. **Pre-partition scope** for parallel subagents so they do not duplicate work
4. **Reconcile outputs** — combine citation graphs, resolve conflicts in handoff contracts, surface inconsistencies for HITL review
5. **Enforce policy boundaries** by routing through PULSE before any external-facing artifact emits
6. **Maintain the engagement state machine** in `engagements/<id>/state.json`

The orchestrator runs serialized by definition — there is exactly one orchestrator per engagement at any time. Multiple orchestrators on the same engagement would race on the state machine.

---

## Subagent fan-out patterns

### VANTA (Research) — fan-out heavy
VANTA is the squad most heavily fanned out. A typical research engagement:

- 2–4 instances of A01 Market Scout, partitioned by subtopic
- 1–2 instances of A03 Competitive Mapper, partitioned by competitor segment
- 1 instance of A02 Evidence Classifier (parallel-safe but rarely benefits from fan-out — bottleneck is upstream)
- 1 instance of A04 Source Archivist (serialized — single archive)
- 1 instance of A05 Synthesizer (serialized — produces single coherent narrative)

The fan-out delivers most of the speedup. Anthropic's reported eval lift comes from this pattern.

### ATLAS (Product) — mixed
ATLAS is mostly parallel-safe but with sequential dependencies:

- A06 PRD Author runs serialized (single PRD per scope)
- A07 Spec Decomposer can fan out by feature slice once the PRD is stable
- A08 Acceptance Curator runs after A07; serialized
- A09 Roadmap Mapper and A10 Release Notes are parallel-safe at the artifact level

### KEEL (Operations) — mostly serialized
KEEL deals with shared infrastructure state — eval runs, traces, incidents, cost meters. Most KEEL agents are serialized to avoid races on shared logs and meters.

### PULSE (Governance) — all serialized
Every PULSE agent is serialized. See `cadre/squad-pulse-governance/README.md` for the per-agent rationale.

---

## The 10-step orchestration sequence

A canonical CADRE engagement runs through this sequence:

1. **Brief intake** — orchestrator reads the engagement brief from `engagements/<id>/brief.md`
2. **Cynefin mapping** — orchestrator classifies each task as Clear, Complicated, Complex, or Chaotic per `cadre/squad-pulse-governance/README.md` and routes accordingly
3. **Cadre design** — orchestrator runs SP-01 (cadre-design.md) to produce `cadre-blueprint.md` for this engagement
4. **Agent roster instantiation** — SP-02 populates per-agent spec adjustments for sector and jurisdiction
5. **Handoff contract generation** — SP-03 emits per-agent JSON schemas
6. **MCP integration setup** — SP-04 establishes MCP servers, OAuth flows, RFC 8707 resource scoping
7. **Memory scope setup** — SP-05 establishes memory paths and path-validation rules
8. **HITL governance configuration** — SP-06 wires up tier mappings and reviewer roster
9. **Eval harness deployment** — SP-07 configures per-agent eval suites
10. **Phased rollout** — SP-08 runs shadow → limited → full deployment with cutover checklist

Each step emits a deliverable to `engagements/<id>/` and an audit-chain entry through A19.

---

## Reconciliation: how the orchestrator combines subagent outputs

When N parallel-safe subagents return outputs that need combining (most commonly: N A01 Market Scout instances returning citation graphs), the orchestrator follows this reconciliation pattern:

1. **Schema validation** — every input must validate against the agent's output schema; non-conforming outputs fail closed
2. **Deduplication** — sources, claims, or entries appearing in multiple subagent outputs are deduplicated by canonical key (URL hash for sources, claim text hash for claims)
3. **Conflict detection** — when two subagents return contradictory facts on the same claim, the orchestrator does not silently pick one. The conflict is preserved in the merged output and flagged for downstream A02 Evidence Classifier handling.
4. **Coverage assessment** — gaps reported by individual subagents are unioned; the merged coverage_assessment reflects total scope coverage
5. **Audit chain entry** — A19 logs the reconciliation event with input audit_entry_ids and the merged output's audit_entry_id

The orchestrator does not invent content during reconciliation. It is a deterministic merger, not a creative synthesizer. Synthesis is A05's job, downstream.

---

## Why this design resists known multi-agent failure modes

| Failure mode | Source | CADRE mitigation |
|---|---|---|
| Parallel agents produce conflicting state | Cognition essay | Parallelism classification; only `parallel-safe` agents fan out |
| Orchestrator can't reconcile divergent outputs | Cognition essay | Reconciliation is deterministic and schema-validated, not LLM-mediated |
| Subagents hallucinate citations | LLM literature | Citation discipline in `../governance/evidence-classification.md`; A02 cross-checks |
| Long-context Opus orchestrator drifts | Anthropic platform notes | Orchestrator uses memory tools (Managed Agents Memory, GA April 23, 2026) for state, not chat-window scrolling |
| Cost runs away under fan-out | 15× token cost figure | A14 Cost Meter enforces budget envelope; SKU tier sets ceiling per engagement |
| Oversight fails when scaled across agents | Cognition essay | PULSE squad makes oversight enforceable per `../governance/hitl-policy.md` |

---

## Citations

- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025. [UNCORROBORATED — vendor-published metrics]
- Cognition. *Don't build multi-agent systems.* 2025 essay. [VERIFIED — primary source]
- Anthropic. *Managed Agents Memory* — public beta announcement, April 23, 2026. [VERIFIED]
- Anthropic. *Claude Opus 4.7* — release notes, April 16, 2026. [VERIFIED]
- Anthropic. *Claude Opus 4.6* — release announcement and pricing ($5/$25 per M tokens, 1M context flat-rate), March 13, 2026. [VERIFIED]

---

*BHIL CADRE Framework — architecture/orchestration-model.md — v1.0.0*
