# Changelog

All notable changes to the BHIL CADRE Framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-04-25

### Added — Initial release

This is the inaugural release of the CADRE Framework, built on the Anthropic agent stack as it stood in April 2026 (Claude Opus 4.6/4.7, Sonnet 4.6, Claude Code sub-agents, Claude Skills, Managed Agents Memory public beta, MCP specification revision 2025-11-25).

**Architecture**

- `architecture/parallel-vs-serial-rule.md` — central thesis: parallel reads safe, parallel writes serialized
- `architecture/orchestrator-worker-pattern.md` — Anthropic 90.2% / 15× citation
- `architecture/handoff-contracts.md` — JSON Schema strict-mode + filesystem artifact pattern
- `architecture/memory-architecture.md` — Managed Agents Memory scoping and path-validation rule
- `architecture/mcp-integration.md` — MCP 2025-11-25 spec, OAuth 2.1, async Tasks, URL Mode Elicitation
- `architecture/failure-modes.md` — Anthropic anti-patterns + Cognition Flappy Bird critique
- `architecture/cynefin-autonomy-dial.md` — Clear/Complicated/Complex/Chaotic mapping to autonomy

**11-prompt orchestration sequence**

- `prompts/P00-master-prompt.md` — orchestrator brief
- `prompts/SP-01-cadre-design.md` through `SP-10-companion-bundle.md` — full sub-prompt sequence
- `prompts/SP-09-readiness-diagnostic.md` — the $4,500–$7,500 commercial wedge

**20-agent cadre**

- `cadre/squad-vanta-research/` — A01–A05: market scout, evidence classifier, competitive mapper, source archivist, synthesizer
- `cadre/squad-atlas-product/` — A06–A10: PRD author, spec decomposer, acceptance curator, roadmap mapper, release notes
- `cadre/squad-keel-operations/` — A11–A15: eval runner, trace auditor, incident responder, cost meter, handoff validator
- `cadre/squad-pulse-governance/` — A16–A20: policy gatekeeper, HITL router, PII redactor, audit logger, compliance mapper

**Readiness scoring**

- `readiness/methodology.md` — 7-dimension scoring methodology
- `readiness/d1-data-infrastructure.md` through `readiness/d7-hitl-governance.md` — per-dimension rubrics
- `readiness/scoring-rubric.md` — composite score calculation

**Governance**

- `governance/hitl-tier-taxonomy.md` — Tier 0–3 gate definitions
- `governance/eu-ai-act-mapping.md` — Article 14 / 26 alignment
- `governance/nist-ai-rmf-mapping.md` — Govern function mapping
- `governance/iso-42001-mapping.md` — Clauses 4–10 mapping
- `governance/colorado-ai-act-notes.md` — versioned for June 2026 → January 2027 effective date
- `governance/case-law-precedents.md` — Air Canada Moffatt, iTutor, Klarna
- `governance/disclosure-templates.md`

**Commercial workflows**

- `workflows/tier-1-discovery-call.md` — free intro
- `workflows/tier-2-readiness-diagnostic.md` — SP-9 one-day diagnostic ($4,500–$7,500)
- `workflows/tier-3-readiness-sprint.md` — 2–4 weeks, 100% diagnostic credit
- `workflows/tier-4-cadre-operator.md` — $5K–$30K/month retainer
- `workflows/tier-5-enterprise-program.md`

**Companion framework integrations**

- `integration/companion-pathfinder.md` — AI literacy curriculum
- `integration/companion-axiom.md` — AI governance overlay
- `integration/companion-verdict.md` — research integrity discipline
- `integration/companion-nexus.md` — data substrate
- `integration/companion-prd-mvp.md` — product delivery cadence

**Templates**

- `templates/agent-spec-template.md`
- `templates/handoff-contract-template.json`
- `templates/readiness-scorecard-template.md`
- `templates/hitl-gate-template.md`
- `templates/eval-harness-template.md`
- `templates/runbook-template.md`

**Worked example**

- `examples/sample-engagement/` — full SP-9 readiness diagnostic for a representative mid-market client

**Claude Code configuration**

- `.claude/settings.json`
- `.claude/rules/` — handoff contracts, memory safety, HITL tier enforcement, citation discipline
- `.claude/skills/` — new-cadre-engagement, run-readiness-diagnostic, run-cadre-blueprint, run-hitl-mapping, run-synthesis
- `.claude/agents/` — orchestrator, research-subagent, evaluator-subagent, governance-subagent

**CI/CD**

- `.github/workflows/validate-handoffs.yml` — JSON Schema validation
- `.github/workflows/markdown-lint.yml` — markdown linting and link integrity
- `.github/workflows/release.yml` — release packaging
- `.github/pull_request_template.md` — PR template with citation and HITL checklists

**Tools**

- `tools/scripts/validate-handoff.py` — JSON Schema validator
- `tools/scripts/score-readiness.py` — readiness composite calculator
- `tools/scripts/trace-audit.py` — OTel trace auditor

---

## Roadmap

### [1.1.0] — Planned

- **Cynefin-keyed autonomy presets** — pre-configured autonomy dials per domain (Clear / Complicated / Complex / Chaotic) so operators don't have to reason from first principles
- **Sector-specific governance overlays** — healthcare (HIPAA), finance (SR 11-7 / OCC 2011-12), hiring (NYC AEDT, EU AI Act high-risk Annex III)
- **Multi-engagement memory architecture** — patterns for cross-engagement learning while honoring per-client data isolation
- **Cost-optimization agent specs** — Haiku-tier subagents for routine work in VANTA and KEEL

### [1.2.0] — Planned

- **MCP Apps integration** — once MCP App marketplace patterns stabilize, document the pairing of CADRE agents with vetted MCP servers
- **AG2 / Microsoft Agent Framework parity specs** — alternative implementations for non-Anthropic stacks
- **Public benchmarks** — replace UNCORROBORATED vendor metrics with BHIL-run independent benchmarks where feasible

### [2.0.0] — Aspirational

- **Self-instrumenting cadre** — agents that produce their own eval scaffolding from their JSON Schema contracts
- **Auto-generated runbooks** — orchestrator-authored deployment runbooks per `templates/runbook-template.md`

---

## Versioning policy

- **Major** (X.0.0) — breaking changes to the architectural thesis, agent contract schema, or HITL tier taxonomy
- **Minor** (1.X.0) — new agents, new prompts, new governance mappings, new examples, non-breaking template additions
- **Patch** (1.0.X) — typo fixes, citation upgrades, broken-link corrections, regulatory effective-date updates

Regulatory updates that change the *effective date* of an existing mapping are patch releases. Regulatory updates that change the *substance* of compliance obligations are minor releases.

---

*BHIL CADRE Framework — Changelog — maintained by BHIL*
