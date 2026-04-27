# BHIL CADRE Framework

**Coordinated Agent Deployment, Readiness & Evaluation**

*Human-Directed. AI-Enabled. Commercially Tested.*

---

> *"Multi-agent systems with Claude Opus orchestrators and Sonnet subagents outperform single-agent baselines by 90.2% on research evals — at roughly 15× token cost. Anthropic, June 13, 2025. CADRE is the playbook that makes that lift defensible: parallel reads safe, parallel writes serialized, handoffs typed, governance tiered, and the whole thing scoped to what a solo founder or a Fortune 500 line-of-business can actually run."*

---

## What this is

CADRE is BHIL's framework for designing, deploying, and governing **20-agent cadres** built on the Anthropic stack (Claude Opus 4.6/4.7, Claude Sonnet 4.6, Claude Code sub-agents, Claude Skills, Managed Agents Memory, MCP servers). It packages a decade of multi-agent research — Anthropic's orchestrator-worker pattern, Cognition's single-threaded discipline, Cynefin domain mapping, and the case-law constraints from Air Canada Moffatt, iTutor, and Klarna — into an opinionated, repeatable engagement.

The thesis is one sentence: **parallel reads are safe; parallel writes are dangerous**. Every architectural choice in this repo follows from that rule.

This repository contains the complete CADRE delivery system:

- An **11-prompt orchestration sequence** (Master Prompt + SP-1 through SP-10) that walks an engagement from intake through final diagnostic
- A **20-agent cadre specification** organized into four squads (VANTA research, ATLAS product, KEEL operations, PULSE governance), each with charter, I/O contract, tool allowlist, parallelism class, HITL tier, and model assignment
- A **7-dimension readiness scoring methodology** with rubric, weights, and a Cynefin-mapped autonomy dial
- A **governance layer** mapping HITL gate tiers to EU AI Act Article 14/26, NIST AI RMF, ISO 42001 Clauses 4–10, and the Colorado AI Act (effective date versioned for the June 2026 → January 2027 rewrite)
- A **5-tier commercial SKU** anchored by a $4,500–$7,500 one-day Readiness Diagnostic (SP-9) that converts into $5K–$30K/month Cadre Operator retainers
- A **worked example engagement** demonstrating the full SP-9 deliverable end to end
- **Claude Code configuration** (rules, skills, agents) so Claude Code can execute CADRE engagements directly

---

## Repository layout

```
BHIL-CADRE-Framework/
├── prompts/              11-prompt orchestration sequence (P00 + SP-01..SP-10)
├── cadre/                20-agent specification across 4 squads
├── architecture/         Read/write asymmetry rule, MCP, memory, failure modes
├── readiness/            7-dimension scoring methodology
├── governance/           HITL tiers, regulatory mapping, case-law precedents
├── workflows/            5-tier commercial SKU (Discovery → Enterprise)
├── integration/          Companion framework bridges (PATHFINDER, AXIOM, VERDICT, NEXUS, PRD/MVP)
├── templates/            Reusable agent specs, handoff contracts, scorecards
├── examples/             Worked SP-9 readiness diagnostic engagement
├── tools/                Validation and audit scripts
├── engagements/          Working directory for live engagements (gitignored)
├── .claude/              Claude Code rules, skills, agents
└── .github/              CI/CD workflows and PR template
```

---

## The architectural thesis

CADRE resolves the **Anthropic vs Cognition conflict** — the most important open question in multi-agent design — through a single operational rule:

> **Pure-function research, evaluation, and classification subagents parallelize.** They read external state (the web, documents, internal records) and return typed artifacts to the orchestrator. The Anthropic orchestrator-worker pattern applies here: 90.2% eval lift, 15× token cost, fan-out as far as the task supports.
>
> **Any subagent that mutates shared state serializes.** Cognition's "Don't Build Multi-Agents" critique applies the moment two subagents start making conflicting decisions about the same artifact. Code edits, file writes, external API calls with side effects, and stateful integrations route single-threaded through the orchestrator with filesystem artifact handoffs.

This is the operating rule for every agent in `cadre/`. Each agent's specification declares a `parallelism_class` of either `parallel-safe` (read-only, idempotent) or `serialized` (mutating, stateful). The orchestrator routes accordingly.

See `architecture/parallel-vs-serial-rule.md` for the full argument and citations.

---

## The 20-agent cadre

Four squads, five agents each, designed to cover the full lifecycle of an early-stage company or a Fortune 500 line of business.

| Squad | ID Range | Focus | Default Parallelism |
|---|---|---|---|
| **VANTA** | A01–A05 | Market research, evidence classification, competitive mapping | Parallel-safe |
| **ATLAS** | A06–A10 | PRD authoring, spec decomposition, roadmap, release notes | Mostly parallel-safe |
| **KEEL** | A11–A15 | Eval running, trace auditing, incident response, cost metering, handoff validation | Mixed (eval + audit parallel; incident + cost serialized) |
| **PULSE** | A16–A20 | Policy gatekeeping, HITL routing, PII redaction, audit logging, compliance mapping | Serialized (governance writes are inherently stateful) |

See `cadre/README.md` for the squad architecture and the per-agent specifications inside each squad directory.

---

## Quick start

If you are an **engagement operator** (BHIL or a partner using this framework to deliver to a client):

1. Read `prompts/P00-master-prompt.md` to understand the orchestration sequence
2. Run the appropriate workflow tier from `workflows/` (`tier-2` is the SP-9 one-day diagnostic — the most common entry)
3. Use `templates/` to scaffold deliverables; persist working files in `engagements/<client-id>/`
4. Score against the rubric in `readiness/scoring-rubric.md`

If you are a **buyer or evaluator** (a CTO, COO, or Chief AI Officer reviewing CADRE for fit):

1. Start with `architecture/parallel-vs-serial-rule.md` — that's the thesis
2. Skim `cadre/README.md` for the agent roster
3. Read `governance/hitl-tier-taxonomy.md` for how risk gets gated
4. Look at `examples/sample-engagement/` for what a finished diagnostic looks like
5. Pricing and engagement shape: `workflows/`

If you are **Claude Code** working inside this repo:

1. Read `CLAUDE.md` first — it contains your operating instructions
2. Honor the rules in `.claude/rules/` for every action
3. Use the skills in `.claude/skills/` for repeatable tasks
4. The agents in `.claude/agents/` define your sub-agent roster

---

## Companion frameworks

CADRE is the anchor framework in a five-framework retainer architecture:

- **[PATHFINDER](#)** — AI literacy curriculum for the humans who approve, oversee, and override agent output. Solves the Prosci ADKAR "Awareness" and "Desire" barriers.
- **[AXIOM](#)** — AI governance overlay. Operationalizes EU AI Act, ISO 42001, and NIST AI RMF.
- **[VERDICT](#)** — Research data integrity. Evidence classification (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE) applied to every agent-generated artifact.
- **[NEXUS](#)** — Data universe. Single-source-of-truth substrate that feeds both human analytics and agent retrieval layers.
- **[PRD/MVP Design](#)** — Product delivery cadence. RICE prioritization, Opportunity Solution Trees, North Star Metric — flows directly into the ATLAS squad.

See `integration/` for each pairing and the retainer architecture.

---

## Citations and primary sources

CADRE is built on primary-source-weighted research. The full citation graph lives in the `architecture/` and `governance/` files and is summarized in the research brief. Key anchors:

- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025.
- Cognition AI (Walden Yan). *Don't Build Multi-Agents.* June 12, 2025.
- Anthropic. *Claude Skills* and *Managed Agents Memory* documentation, October 2025–April 2026.
- Model Context Protocol. *Specification revision 2025-11-25.* Linux Foundation Agentic AI Foundation.
- Snowden, D. & Boone, M. *A Leader's Framework for Decision Making (Cynefin).* HBR, November 2007.
- EU AI Act, Articles 14 and 26 (entered into force August 1, 2024; phased applicability through 2026–2027).
- NIST AI Risk Management Framework 1.0, January 2023; Generative AI Profile, July 2024.
- ISO/IEC 42001:2023 — AI management systems.

---

## License

MIT, with an AI accuracy and HITL disclaimer. See `LICENSE`.

---

## About BHIL

The Barry Hurd Intelligence Lab builds opinionated, citation-rich frameworks for AI deployment in mid-market and enterprise contexts. CADRE joins LOCUS (location intelligence), MERIDIAN, SENTINEL, VANTAGE, VERDICT, and CODEX in the BHIL framework portfolio.

Website: [barryhurd.com](https://barryhurd.com)
Repo home: [github.com/camalus](https://github.com/camalus)

---

*CADRE Framework v1.0.0 — Barry Hurd Intelligence Lab — © 2026*
