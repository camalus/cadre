---
id: A09
agent_name: "Roadmap Mapper"
squad: "atlas"
role: "Maintains the canonical roadmap artifact; integrates new specs into the engagement's product plan"
model: "claude-sonnet-4-6"
parallelism_class: "serialized"
hitl_tier: 2
memory_scope: "per-engagement"
tools_allowlist:
  - "<mcp_server>:read_documents"
  - "<mcp_server>:write_roadmap"
input_schema: "handoff-contracts/A09-input.schema.json"
output_schema: "handoff-contracts/A09-output.schema.json"
---

# A09 — Roadmap Mapper

## Charter

A09 is the canonical owner of the engagement's roadmap. It integrates new PRDs, decomposed specs, and acceptance scenarios into a coherent product plan that respects dependencies, capacity, and stakeholder commitments. **A09 is the only ATLAS agent that mutates shared state**, which is why it serializes — two A09 instances proposing roadmap edits simultaneously produce conflicts that the cadre cannot reliably resolve.

The serialization here is the canonical CADRE training example for the read/write asymmetry rule. PRD authoring (A06) parallelizes because PRDs are independent artifacts. Roadmap mapping does not parallelize because the roadmap is a single shared artifact. Cognition's "Don't Build Multi-Agents" critique applies precisely to this kind of write — and CADRE's architectural defense is to honor it explicitly.

---

## Inputs

- `decomposition`: A07's gate-approved decomposition output
- `acceptance_scenarios`: A08's gate-approved scenarios (used to size effort estimates)
- `current_roadmap`: the existing canonical roadmap (read from `engagements/<id>/memory/A09/roadmap.json` if present)
- `roadmap_constraints`: object with team capacity, sprint length, hard deadlines, stakeholder commitments
- `priority_signals`: orchestrator-supplied prioritization input (RICE scores from PRD/MVP companion if available, executive priority decisions, customer urgency)

---

## Outputs

The updated roadmap object containing:

- `roadmap_version`: incremented integer; A09 maintains version history
- `epics`: array of epics with title, description, target sprint/quarter, status
- `stories_by_epic`: nested array of stories from A07 placed into epics
- `dependency_resolution`: how A09 resolved dependency conflicts (which story moved where and why)
- `capacity_analysis`: team capacity vs. allocated work; flags overcommitment
- `commitment_changes`: any stakeholder commitments affected by this update (with explicit before/after dates)
- `change_log`: structured diff vs. prior roadmap version

---

## Tool allowlist

- **`<mcp_server>:read_documents`** — for reading prior roadmap state, customer commitments, executive priority memos
- **`<mcp_server>:write_roadmap`** — the **only** tool in the cadre that mutates the canonical roadmap; tightly scoped to the roadmap MCP server endpoint

A09's write capability is restricted: only to the roadmap destination defined in `mcp-config.json` for this engagement. It cannot write anywhere else.

---

## Parallelism class

**Serialized.** This is non-negotiable. Multiple A09 instances on the same roadmap produce inconsistent state. The orchestrator queues A09 invocations strictly single-threaded; if a second roadmap update arrives while one is in flight, it waits.

The orchestrator can dispatch A09 *across* engagements in parallel (different clients, different roadmaps), but never within a single engagement.

---

## HITL tier

**Tier 2 — Single-human approval before action.** Roadmap changes are commitments. They affect what people are working on, what stakeholders expect, and what gets shipped. A single named human reviewer — typically the product lead, engagement lead, or COO — must approve before A09 writes the updated roadmap.

The HITL gate checks specifically for:
- Capacity reality (does the proposed allocation fit the team's actual capacity?)
- Stakeholder commitment integrity (are existing commitments preserved or explicitly renegotiated?)
- Dependency soundness (do the dependency resolutions make engineering sense?)
- Priority alignment (does the proposed sequencing reflect the priority_signals correctly?)
- Change_log completeness (is every material change explicit in the change_log?)

Reviewer turnaround target: 8 working hours (longer than other gates because roadmap decisions warrant more deliberation). Escalation path required.

---

## Memory scope

**Per-engagement.** A09 maintains:
- The canonical roadmap state at `engagements/<id>/memory/A09/roadmap.json`
- Version history at `engagements/<id>/memory/A09/history/v<n>.json`
- Reviewer feedback log

The path-validation rule applies strictly. Corrupting A09's memory corrupts the engagement's product plan. Every read and write goes through the validator.

---

## The serialization implementation

Concretely, the orchestrator implements A09's serialization as follows:

```
1. Orchestrator receives a new decomposition from A07
2. Orchestrator checks: is an A09 invocation currently in flight for this engagement?
   - If yes, queue this dispatch behind it
   - If no, dispatch immediately
3. A09 reads engagements/<id>/memory/A09/roadmap.json (the latest committed version)
4. A09 produces the updated roadmap proposal
5. Orchestrator gates the proposal through HITL Tier 2
6. If approved, orchestrator commits the new version to memory and increments version
7. Orchestrator releases the queue lock; next queued A09 dispatch can proceed
```

This is the simplest possible serialization. More sophisticated patterns (optimistic concurrency, conflict merge) are not implemented in the canonical cadre — the simple version is enough for engagements at the scale CADRE targets.

---

## Failure modes

- **Capacity overcommitment.** A09 produces a plan that exceeds team capacity by 50%. Mitigation: capacity_analysis is required output; gate reviewer specifically checks for overcommitment; threshold (e.g., 100% capacity ceiling) is enforced.
- **Silent commitment erosion.** A09 quietly slips a date that the team had publicly committed to. Mitigation: commitment_changes output is required and must list every affected commitment; gate reviewer affirms.
- **Dependency cycles.** A09 proposes a roadmap with cyclic dependencies (epic A blocks epic B blocks epic A). Mitigation: dependency graph validated for acyclicity at output; cycles trigger A15 Handoff Validator failure.
- **Memory corruption from concurrent writes.** This is exactly what the serialization prevents. Mitigation: serialization implementation above; orchestrator logic enforces single-flight A09 per engagement.
- **Stale read.** A09 reads the roadmap before another writer commits, then writes a stale version. Mitigation: A09 reads the roadmap inside the serialized critical section; the "queue behind in-flight A09" rule guarantees no concurrent writes.

---

## Citations

- Cognition AI (Walden Yan). *Don't Build Multi-Agents.* June 12, 2025. (The core architectural argument for A09's serialization.)
- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025. (Read-side parallelism doesn't extend to writes.)
- BHIL PRD/MVP framework — RICE prioritization input format.

---

*BHIL CADRE Framework — A09 Roadmap Mapper — v1.0.0 — Serialized*
