# Squad ATLAS — Product

*ATLAS turns research into shippable specifications. Most ATLAS agents are parallel-safe because they author independent artifacts; the exception is A09 Roadmap Mapper, which is serialized because roadmap edits are mutating decisions on shared state.*

---

## Charter

ATLAS is the cadre's product squad. It consumes VANTA's evidence base (the executive brief from A05) and produces the artifacts that make a product team able to ship: PRDs, decomposed user stories, acceptance criteria, the canonical product roadmap, and release notes. ATLAS is the squad most likely to interface directly with the client's existing product organization, which means it inherits the client's product cadence and tooling.

The squad pairs naturally with BHIL's PRD/MVP companion framework — the cadre's PRD Author, Spec Decomposer, and Roadmap Mapper assume PRD/MVP-grade input from the client. When the client lacks that maturity, the recommended bundle includes PRD/MVP alongside CADRE.

---

## Roster

| ID | Name | Role |
|---|---|---|
| [A06](A06-prd-author.md) | PRD Author | Drafts product requirements documents using EARS notation |
| [A07](A07-spec-decomposer.md) | Spec Decomposer | Breaks PRDs into typed user stories and technical sub-specs |
| [A08](A08-acceptance-curator.md) | Acceptance Curator | Authors acceptance test scenarios in Gherkin-style behavior specs |
| [A09](A09-roadmap-mapper.md) | Roadmap Mapper | **Serialized.** Maintains the canonical roadmap artifact |
| [A10](A10-release-notes.md) | Release Notes | Drafts release notes and changelog entries from completed roadmap items |

---

## Parallelism

Four of five ATLAS agents are parallel-safe — A06, A07, A08, A10 author independent artifacts and do not mutate shared state. **A09 is serialized** because the roadmap is a single shared artifact: two agents proposing roadmap edits in parallel produce conflicts, and the Cognition "Don't Build Multi-Agents" critique applies precisely here. A09 is the example used in CADRE training to make the read/write asymmetry rule concrete.

---

## Coordination pattern

A typical ATLAS cycle:

1. Orchestrator dispatches **A06 PRD Author** with the executive brief from A05; A06 returns a draft PRD
2. Orchestrator dispatches **A07 Spec Decomposer** and **A08 Acceptance Curator** in parallel — both consume the PRD; A07 produces user stories, A08 produces acceptance scenarios
3. Once A07 and A08 complete, orchestrator routes A07's output to **A09 Roadmap Mapper** *single-threaded* — A09 integrates the new specs into the canonical roadmap
4. Later, when items ship, **A10 Release Notes** authors the changelog entry from the closed roadmap items

A09 is the synchronization point. No other agent touches the roadmap directly.

---

## HITL discipline within ATLAS

ATLAS lives at Tier 1 by default — most artifacts are internal to the engagement and reviewable in batch. Two exceptions:

- **A09 Roadmap Mapper** — Tier 2. Roadmap is a contract-with-stakeholders artifact; changes affect what people are working on, expectations, and external commitments. Single-human approval before action.
- **A10 Release Notes** — Tier 1, but the orchestrator's downstream gating treats release notes intended for external publication (customer-facing changelog, blog post) as a Tier 2 action. The agent itself is Tier 1; the publication is Tier 2.

---

## Memory scope

All ATLAS agents use **per-engagement** memory by default. Drafts, prior decompositions, and roadmap snapshots are engagement-specific and don't transfer cleanly across clients.

A09's memory is the most consequential — it holds the canonical roadmap state. The path-validation rule applies strictly here; corrupting A09's memory corrupts the engagement's product plan.

---

## Common failure modes (squad-level)

- **PRD without success metrics.** A06 must produce PRDs with explicit, measurable success criteria. PRDs without them get rejected at the gate.
- **User stories without acceptance criteria.** A07 and A08 are paired for a reason. A user story decomposed without acceptance scenarios is a partial output; the orchestrator should not accept it.
- **Roadmap drift.** Multiple agents proposing roadmap edits without going through A09 produces an inconsistent roadmap. The serialization is the defense.
- **Release notes that omit breaking changes.** A10 must explicitly call out breaking changes; "minor improvements" framing for a breaking change is a defect.

---

## Citations

- EARS notation (Easy Approach to Requirements Syntax) — Mavin et al., 2009.
- Gherkin BDD format documentation.
- BHIL PRD/MVP framework — companion methodology.
- Cognition AI (Walden Yan). *Don't Build Multi-Agents.* June 12, 2025. (The Flappy Bird example informs A09's serialization.)

---

*BHIL CADRE Framework — ATLAS Squad — v1.0.0*
