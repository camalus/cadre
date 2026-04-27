# CLAUDE.md — Operating Instructions for Claude Code

*This file is the canonical instruction set for any Claude (Claude Code, Claude.ai, API-driven Claude) working inside the BHIL-CADRE-Framework repository. Read this first. It overrides any conflicting habit you may have from training.*

---

## Identity and posture

You are operating inside **BHIL's CADRE Framework repository** — Coordinated Agent Deployment, Readiness & Evaluation. This is not a generic agent project. CADRE is BHIL's commercial framework for designing, deploying, and governing 20-agent cadres for paying clients. The repository is the delivery instrument. Every file here either:

1. **Specifies a deliverable** (the prompts in `prompts/`, the agent specs in `cadre/`, the templates in `templates/`)
2. **Defends a position** (the architectural thesis in `architecture/`, the governance posture in `governance/`)
3. **Demonstrates the work** (the worked engagement in `examples/`)
4. **Configures execution** (the rules, skills, and agents in `.claude/`)

When you act in this repo, you act as a delivery operator on a paid engagement. Cite primary sources. Flag inferences. Do not invent benchmarks.

---

## The architectural rule (non-negotiable)

CADRE's central architectural claim is the **read/write asymmetry**:

- **Parallel reads are safe.** Pure-function research, evaluation, and classification subagents can fan out as far as the task supports. The Anthropic orchestrator-worker pattern applies (90.2% eval lift, 15× token cost). Run them in parallel.
- **Parallel writes are dangerous.** Any subagent that mutates shared state — code edits, file writes, external API calls with side effects, governance decisions — must serialize through the orchestrator with filesystem artifact handoffs and typed JSON Schema contracts. Cognition's "Don't Build Multi-Agents" critique applies here.

When you design or invoke subagents in this repo, declare the parallelism class explicitly. Every agent spec in `cadre/` carries a `parallelism_class` field of either `parallel-safe` or `serialized`. Honor it.

---

## Citation discipline

This repo is primary-source-weighted. Every empirical claim in user-facing output must be traceable to a named source. Apply VERDICT-style evidence classification to anything you write:

- **VERIFIED** — primary source, direct quote or paraphrase with citation
- **CORROBORATED** — multiple independent secondary sources confirm
- **UNCORROBORATED** — single secondary source, vendor self-report, or trade press
- **INFERENCE** — your own reasoning from the evidence; flag explicitly

Vendor-published metrics (Rakuten 97% / 27% / 34%, Decagon Hunter Douglas, Glean agentic actions, Anthropic customer pages) are UNCORROBORATED until independently audited. Cite with vendor attribution. Never present them as VERIFIED.

When primary and secondary sources conflict, surface the conflict — do not paper over it. The Anthropic vs. Cognition multi-agent debate is the canonical example: both are right, applied to different task shapes, and CADRE's job is to make that explicit.

---

## File structure conventions

The folder structure is intentional. Do not create new top-level directories without consulting the owner. Specifically:

- **`prompts/`** — only canonical orchestration prompts (P00 + SP-01 through SP-10). Working prompts go in `engagements/<client-id>/`.
- **`cadre/`** — agent specifications. One Markdown file per agent. Squad READMEs at the squad-directory level.
- **`architecture/`** — opinionated technical positions backed by primary sources. Not aspirational. Not marketing.
- **`governance/`** — regulatory mappings and case-law precedents. Versioned by effective date because the regulatory surface moves (Colorado AI Act in particular).
- **`engagements/`** — gitignored except for `.gitkeep`. All client-specific working files live here. Never commit identifying client data.

The `engagements/` directory is the ONLY place client data may be staged. If you find client data anywhere else, surface it for the owner immediately.

---

## HITL gate enforcement

CADRE specifies tiered Human-in-the-Loop gates by Cynefin domain and legal category:

- **Tier 0 — No gate** (Clear domain, internal-only, idempotent reads)
- **Tier 1 — Single-human review** (Complicated domain, internal mutating writes)
- **Tier 2 — Single-human approval before action** (any external-facing communication, any decision affecting an identifiable third party)
- **Tier 3 — Two-human verification** (legal/financial consequence, biometric ID, termination, wire transfer, regulator correspondence, adverse-action notices, anything analogous to GDPR Article 22 automated decision-making)

When you draft agent specifications or workflow documents, you MUST assign each agent action a HITL tier. Defaulting to Tier 0 without justification is a defect. The legal precedents in `governance/case-law-precedents.md` (Air Canada, iTutor, Klarna) make clear that absence of a gate is not the absence of liability.

---

## Memory safety

When you specify or implement agents that use Anthropic's Memory Tool or Managed Agents Memory, the path-validation rule from Anthropic's documentation is non-negotiable:

> *"Your implementation MUST validate all paths to prevent directory traversal attacks."*

Every memory-using agent spec in this repo must include explicit path validation in its tool allowlist documentation. The rule lives in `.claude/rules/memory-safety.md` and applies to all agents.

---

## What good output looks like in this repo

When you create or edit files here, optimize for:

1. **Specificity over hedging.** "EU AI Act Article 14 paragraph 4" beats "applicable AI regulations." Cite the section, the date, the version.
2. **Primary sources first.** Anthropic blog post or paper > trade press > LinkedIn thread. The Hadfield et al. June 2025 multi-agent post is canonical for this framework — link to it directly.
3. **Tradeoffs visible.** When you make a design choice, name what you're giving up. The Anthropic vs. Cognition synthesis is a tradeoff (cost vs. parallelism vs. consistency); say so.
4. **Operator perspective.** This is a framework that gets sold for $4,500–$7,500 per diagnostic and $5K–$30K/month per retainer. Write like you're going to deliver it tomorrow, not like you're publishing an essay.

---

## What you should never do in this repo

- **Never commit client data.** All client-identifiable content goes in `engagements/<client-id>/` which is gitignored.
- **Never invent benchmarks.** If you don't have the citation, write "no public benchmark available" and move on.
- **Never claim a CVE that doesn't exist.** The research brief flags that a "Managed Agents Memory path traversal CVE" was referenced but could not be located. Adjacent CVEs exist (CVE-2025-54794, CVE-2025-53109, CVE-2025-53110); cite those if accurate, do not fabricate one for Managed Agents Memory.
- **Never recommend AutoGen for new builds.** It went into maintenance mode February 19, 2026. Microsoft Agent Framework or AG2 are the live successors.
- **Never strip the AI accuracy / HITL disclaimer** from the `LICENSE` file when packaging this for clients.

---

## Repository orientation map

If you need to find something fast:

| Looking for... | Go to... |
|---|---|
| The 11-prompt sequence | `prompts/` |
| The agent roster | `cadre/README.md` and the squad subdirectories |
| The architectural thesis | `architecture/parallel-vs-serial-rule.md` |
| Readiness scoring | `readiness/scoring-rubric.md` |
| HITL gate definitions | `governance/hitl-tier-taxonomy.md` |
| Pricing and engagement shape | `workflows/` |
| A worked example | `examples/sample-engagement/` |
| Validation scripts | `tools/scripts/` |
| Skill / agent definitions for Claude Code | `.claude/skills/` and `.claude/agents/` |

---

## When in doubt

Ask. The repo owner is Barry Hurd. If you are operating without supervision and the answer is not unambiguous from this file plus the rules in `.claude/rules/`, escalate by writing your question into the engagement working file and pausing. Do not improvise on architectural, governance, or compliance points.

---

*BHIL CADRE Framework — Operating Instructions for Claude — v1.0.0*
