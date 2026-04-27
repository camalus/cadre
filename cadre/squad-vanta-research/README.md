# Squad VANTA — Market Research

*VANTA is the cadre's eyes on the outside world. All five VANTA agents are parallel-safe by default because they read external state and return classified evidence — they do not mutate anything except their own working memory.*

---

## Charter

VANTA produces the evidence base on which the rest of the cadre reasons. It conducts structured research against an engagement brief, classifies the evidence by reliability tier, builds competitive maps, archives sources to defend against link rot, and synthesizes the squad's outputs into an executive brief for the orchestrator.

VANTA is the squad most directly answerable to the **citation discipline** of the framework. Every empirical claim leaving VANTA carries a citation and an evidence classification (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE). A02 Evidence Classifier is the gatekeeper; the orchestrator does not accept VANTA output that has not been classified.

---

## Roster

| ID | Name | Role |
|---|---|---|
| [A01](A01-market-scout.md) | Market Scout | Web search and document retrieval against a structured research brief |
| [A02](A02-evidence-classifier.md) | Evidence Classifier | Applies VERDICT-style classification to every claim |
| [A03](A03-competitive-mapper.md) | Competitive Mapper | Builds market maps, competitor matrices, positioning grids |
| [A04](A04-source-archivist.md) | Source Archivist | Snapshots sources, records access dates, manages link rot |
| [A05](A05-synthesizer.md) | Synthesizer | Compresses VANTA outputs into a single executive brief |

---

## Parallelism

All five VANTA agents are **parallel-safe**. They read external state (web, documents, internal sources via MCP) and return classified evidence to the orchestrator. None of them mutate shared state. The orchestrator can fan out the entire squad simultaneously when the task supports it.

The Anthropic 90.2% lift / 15× token cost from Hadfield et al. (June 13, 2025) applies to VANTA most directly. VANTA is where the parallel-research thesis pays off; it is also where the cadre's token spend concentrates (typically 30–50% of total).

---

## Coordination pattern

VANTA agents do **not** call each other. The orchestrator dispatches them in parallel and merges results. Specifically:

1. Orchestrator dispatches **A01 Market Scout** with the research brief; A01 returns a citation graph
2. Orchestrator dispatches **A02 Evidence Classifier** in parallel with **A03 Competitive Mapper** and **A04 Source Archivist**, each consuming A01's citation graph
3. Once A02, A03, A04 complete, orchestrator dispatches **A05 Synthesizer** with all four prior outputs
4. A05 produces the executive brief, which the orchestrator hands off to ATLAS or the next stage

A05 is the only VANTA agent that writes orchestrator-visible state (the executive brief). The others produce intermediate artifacts that A05 consumes.

---

## HITL discipline within VANTA

VANTA is mostly Tier 0 (research is read-only and internal). Two exceptions:

- **A03 Competitive Mapper** — Tier 1. Competitive maps can be wrong in directionally-meaningful ways (anointing the wrong leader, missing a major entrant). A single human reviewer validates the map before it informs ATLAS.
- **A05 Synthesizer** — Tier 1. The executive brief is the artifact most likely to be quoted out of context. Single-human review before the brief enters the audit trail.

A02 Evidence Classifier itself runs at Tier 0 because it produces a classification, not a claim. Its outputs are the input to the gating function, not gated themselves.

---

## Memory scope

All VANTA agents use **per-engagement** memory by default. They accumulate research within an engagement (so an A01 second-pass query benefits from the first-pass results) but their memory is destroyed at engagement close. Cross-engagement memory is not used in VANTA — research findings are client-specific and do not transfer cleanly across clients.

---

## Common failure modes (squad-level)

- **Duplicative work without division of labor** — two A01 instances researching the same topic without distinct angles. The orchestrator must divide before fan-out.
- **SEO-farm bias** — VANTA agents must prefer government data, peer-reviewed papers, vendor technical docs, and academic PDFs over content farms. A04 Source Archivist enforces this.
- **Vendor metric inflation** — vendor-published ROI numbers (Rakuten 97% / 27% / 34%, Decagon, Glean) get tagged as UNCORROBORATED until independently audited. Treating them as VERIFIED is a recurring failure mode.
- **Single-source dependency** — any claim resting on one source gets flagged for corroboration. The standard is at least one primary plus one independent secondary for CORROBORATED.

---

## Citations

- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025. (90.2% / 15× research-eval pattern.)
- BHIL VERDICT framework — evidence classification methodology.

---

*BHIL CADRE Framework — VANTA Squad — v1.0.0*
