---
id: CADRE-SP-02
title: "SP-02 — Agent Roster"
version: "1.0"
type: sub-prompt
sequence: 2
input_artifacts: ["cadre-blueprint.md"]
output_artifact: "agents/A##-*.md (one file per in-scope agent)"
hitl_tier: 1
---

# SP-02 — Agent Roster

*Populates per-agent specifications for every agent in scope per SP-01. Each spec uses the standardized `templates/agent-spec-template.md` schema and is written to `engagements/<id>/agents/`.*

---

## Purpose

The cadre blueprint from SP-01 names which agents are in scope. SP-02 produces the actual operational specifications: charter, JSON Schema I/O contracts, tool allowlists, parallelism class, HITL tier, model assignment, memory scope, failure modes, and citations.

The canonical agent specifications live in `cadre/squad-*/A##-*.md` at the repository root. SP-02 reads those canonical files and tailors them to the engagement — adjusting tool allowlists, HITL tiers, and memory scopes based on the client's sector and jurisdiction.

---

## Inputs

- **`engagements/<id>/cadre-blueprint.md`** — the cadre design from SP-01
- **`cadre/squad-*/A##-*.md`** — canonical agent specifications
- **`templates/agent-spec-template.md`** — the schema all agent specs follow
- **`governance/`** — for sector/jurisdiction-specific HITL tier adjustments

---

## Output

For each in-scope agent, write `engagements/<id>/agents/A##-<agent-name>.md`. Each file follows the template schema:

```yaml
---
id: A##
agent_name: "<n>"
squad: "<vanta | atlas | keel | pulse>"
role: "<charter in one sentence>"
model: "<claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5>"
parallelism_class: "<parallel-safe | serialized>"
hitl_tier: "<0 | 1 | 2 | 3>"
memory_scope: "<none | per-engagement | cross-engagement>"
tools_allowlist:
  - "<tool name>"
  - "<MCP server name>:<tool>"
input_schema: "handoff-contracts/A##-input.schema.json"
output_schema: "handoff-contracts/A##-output.schema.json"
---

# A## — <Agent Name>

## Charter
[1 paragraph]

## Inputs
[summary; full schema in handoff-contracts]

## Outputs
[summary; full schema in handoff-contracts]

## Tool allowlist
[itemized with rationale per tool]

## Parallelism class
[parallel-safe or serialized, with justification]

## HITL tier
[0/1/2/3, with justification and named reviewer if Tier 2+]

## Memory scope
[none / per-engagement / cross-engagement, with path-validation strategy]

## Failure modes
[itemized known anti-patterns and mitigations]

## Citations
[primary sources for any claims this agent makes]
```

---

## Step-by-step

### Step 1 — Load the canonical specifications

For each in-scope agent ID in `cadre-blueprint.md`, read the corresponding canonical spec from `cadre/squad-<squad>/A##-<n>.md`. These are the starting point.

### Step 2 — Apply sector-specific adjustments

Some sectors require tighter constraints than the canonical specs assume:

- **Healthcare (HIPAA)** — A18 PII Redactor's allowlist must include the HIPAA Safe Harbor 18 identifiers; memory scope for any agent reading PHI must be `per-engagement` only.
- **Finance (SR 11-7 / OCC 2011-12)** — A11 Eval Runner must include model-risk-management evaluation criteria; A19 Audit Logger retention must meet 7-year minimum.
- **Hiring (NYC AEDT, EU AI Act high-risk Annex III)** — A17 HITL Router must enforce Tier 3 (two-human verification) on any decision affecting an applicant; A20 Compliance Mapper must produce the AEDT bias audit cross-walk.
- **Biometric (BIPA, EU AI Act)** — Tier 3 mandatory on any biometric ID decision.

### Step 3 — Apply jurisdiction-specific adjustments

- **EU jurisdictions** — All agents producing decisions affecting EU data subjects must include GDPR Article 22 alignment in HITL tier and disclosure language.
- **Colorado** — As of June 30, 2026 (or January 1, 2027 if the rewrite passes), CO AI Act consumer-impact assessments may be required for any agent making a "consequential decision." See `governance/colorado-ai-act-notes.md`.
- **NYC** — AEDT bias audits for hiring agents.

### Step 4 — Validate tool allowlist

Each agent's tool allowlist must be the *minimum* set required for its charter. If an agent's allowlist includes a tool it doesn't need, remove it. If it excludes a tool it does need, add it with justification.

Special cases:

- Web search tools (web_search, web_fetch) are **parallel-safe** — VANTA agents use them freely.
- Bash, str_replace, create_file are **state-mutating** — only KEEL and orchestrator agents have them.
- MCP server tools depend on the server. Read-only MCP tools are parallel-safe; mutating MCP tools are serialized.

### Step 5 — Set memory scope

Default scopes:

- **VANTA agents** — `per-engagement` (so they can accumulate research within an engagement but don't leak across clients)
- **ATLAS agents** — `per-engagement` (same rationale)
- **KEEL agents** — `cross-engagement` for eval and audit history; `per-engagement` for cost meter and incident state
- **PULSE agents** — `cross-engagement` for policy rulebooks; `per-engagement` for client-specific exceptions

For any agent with `cross-engagement` memory, the path-validation rule from `.claude/rules/memory-safety.md` applies. Document the path-validation pattern in the agent spec.

### Step 6 — Write the per-agent files

Write one `.md` file per agent to `engagements/<id>/agents/`. Use `templates/agent-spec-template.md` as the scaffold. Cross-reference the JSON Schemas (which SP-03 will produce).

---

## Quality criteria

A passing agent spec has:

- [ ] Charter is one paragraph and matches the canonical spec's intent
- [ ] Tool allowlist is minimal and explicitly justified
- [ ] Parallelism class matches the canonical default unless override is documented
- [ ] HITL tier reflects sector and jurisdiction (not just default)
- [ ] Memory scope includes path-validation pattern if cross-engagement
- [ ] At least one named failure mode with mitigation
- [ ] At least one primary-source citation

---

## Common failure modes

- **Copying canonical specs verbatim without sector adjustment.** The canonical specs are the starting point, not the endpoint.
- **Over-broad tool allowlists.** "Just give it everything" violates the minimal-allowlist principle and increases blast radius on incidents.
- **Defaulting HITL tier to 0 to save reviewer time.** This is the iTutor / Air Canada / Klarna failure mode. If the agent action affects a third party, the floor is Tier 2.
- **Setting cross-engagement memory without path validation.** This is the path-traversal vulnerability the Anthropic docs explicitly warn about.

---

## Output validation

After writing all per-agent files, run `tools/scripts/validate-handoff.py` against the engagement directory. The script checks that every agent referenced in `cadre-blueprint.md` has a corresponding `.md` file with valid frontmatter and a referenced JSON Schema (which SP-03 produces next).

---

*BHIL CADRE Framework — SP-02 — v1.0.0*
