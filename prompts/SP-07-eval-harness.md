---
id: CADRE-SP-07
title: "SP-07 — Eval Harness"
version: "1.0"
type: sub-prompt
sequence: 7
input_artifacts: ["agents/A##-*.md", "handoff-contracts/*.schema.json"]
output_artifact: "evals/*.yaml"
hitl_tier: 1
---

# SP-07 — Eval Harness

*Defines acceptance criteria for every agent output. Produces a YAML eval suite that A11 (Eval Runner) executes against agent outputs in real time.*

---

## Purpose

A multi-agent system without evals is a multi-agent system that fails silently. SP-07 defines what "good output" looks like for every agent in the cadre, in machine-checkable form. The evals run continuously: A11 (Eval Runner) executes them against every agent output, and A19 (Audit Logger) records pass/fail.

The discipline is borrowed from Anthropic's published research-eval methodology. Anthropic's reported 90.2% lift was measured against an internal research eval; CADRE's analog is the per-agent eval suite produced here.

---

## Inputs

- **`engagements/<id>/agents/A##-*.md`** — agent specs from SP-02
- **`engagements/<id>/handoff-contracts/*.schema.json`** — output schemas from SP-03
- **`templates/eval-harness-template.md`** — eval suite scaffolding

---

## Output

For each in-scope agent, write `engagements/<id>/evals/A##-evals.yaml`. Each file contains:

```yaml
agent_id: A##
agent_name: "<n>"
eval_suite_version: "1.0"
evals:
  - id: "A##-eval-001"
    type: "schema_validity"      # output validates against schema
    severity: "blocker"
    description: "Output must validate against output schema"
  - id: "A##-eval-002"
    type: "citation_density"     # has minimum citations per claim
    severity: "blocker"
    description: "Every empirical claim must have at least one citation"
    threshold: 1.0
  - id: "A##-eval-003"
    type: "evidence_classification"
    severity: "blocker"
    description: "No claim labeled VERIFIED without primary source"
  - id: "A##-eval-004"
    type: "task_specific"        # custom per-agent
    severity: "warning"
    description: "<task-specific check>"
  # ... more evals
acceptance_threshold:
  blocker_pass_rate: 1.0          # all blockers must pass
  warning_pass_rate: 0.95         # 95% of warnings can pass
escalation:
  on_blocker_fail: "halt_engagement"
  on_warning_fail: "log_and_continue"
```

---

## The standard eval categories

Every agent gets evals in these categories:

### 1. Schema validity (blocker)

Output must validate against its declared output schema (from SP-03). Any schema validation failure is a blocker.

### 2. Citation density (blocker for research/eval agents)

For VANTA agents (A01–A05) and KEEL eval/audit agents (A11, A12), every empirical claim in the output must carry at least one citation. The eval extracts claims from the output, counts citations, and computes claim-citation ratio. Threshold: 1.0 (every claim cited).

### 3. Evidence classification integrity (blocker for research agents)

For VANTA agents, every citation has a declared evidence class (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE). The eval checks that:

- VERIFIED citations point to primary sources (peer-reviewed papers, official documentation, regulatory text, vendor technical documentation)
- CORROBORATED citations are backed by 2+ independent secondary sources
- UNCORROBORATED is the default for vendor self-reports, single secondary sources, and trade press
- INFERENCE is explicitly tagged on any claim that's the agent's own reasoning

A vendor self-report tagged as VERIFIED is a blocker fail.

### 4. Task-specific correctness (mix of blocker and warning)

Per-agent custom evals. Examples:

- **A06 PRD Author**: every PRD must have an explicit problem statement, success metrics, and out-of-scope section
- **A09 Roadmap Mapper**: roadmap items must have effort estimates and dependency declarations
- **A11 Eval Runner**: must produce a pass/fail decision for every input, not "skipped"
- **A17 HITL Router**: every decision routed must have a recorded reviewer name and timestamp
- **A18 PII Redactor**: redacted output must contain no PII matching the configured pattern set

### 5. Latency (warning)

Per-agent latency budget. Defaults:

- VANTA agents (research): 90s p95
- ATLAS agents (drafting): 120s p95
- KEEL agents (validation): 30s p95
- PULSE agents (gating): 15s p95

Latency exceeding budget is a warning; chronic latency exceedance triggers a review.

### 6. Cost (warning)

Per-agent per-invocation cost ceiling. Set during SP-04 budget envelope. Cost overrun is a warning; chronic overrun triggers a review.

### 7. HITL compliance (blocker for any agent with Tier 1+ actions)

Output flagged as Tier 1+ MUST include a `hitl_decision` object with reviewer name, decision, and timestamp before being released externally. Missing or stub HITL decision on a gated action is a blocker.

---

## Step-by-step

### Step 1 — Map evals to each agent

For each in-scope agent, instantiate the standard eval categories. Adjust thresholds per the agent's role.

### Step 2 — Define task-specific evals

Read the agent's charter and outputs from SP-02. For each output, design 1–3 task-specific evals that check whether the agent fulfilled its charter. The PRD Author example: did it produce a PRD with required sections? did the success metrics include a baseline?

### Step 3 — Set acceptance thresholds

Default: blocker_pass_rate = 1.0, warning_pass_rate = 0.95. Adjust per SKU tier:

- Tier 2 (Readiness Diagnostic): same defaults
- Tier 3 (Sprint): same defaults
- Tier 4 (Cadre Operator): higher warning threshold (0.98) given continuous operation
- Tier 5 (Enterprise): tightest thresholds; consider per-domain SLOs

### Step 4 — Define escalation behavior

For each eval, set `on_fail`:

- `halt_engagement` — orchestrator stops dispatching; human required (default for blockers)
- `escalate_to_reviewer` — A17 routes to the named HITL reviewer (default for warnings on gated actions)
- `log_and_continue` — A19 logs the failure but the engagement continues (default for warnings)
- `quarantine_output` — output is held in a quarantine directory pending review (for outputs that may contain PII or compliance issues)

### Step 5 — Validate the eval suite

Run `tools/scripts/validate-eval-suite.py` to confirm:

- Every in-scope agent has an eval YAML
- Every eval has an ID, type, severity, and description
- Every blocker has an `on_fail` of `halt_engagement` or `quarantine_output`
- Every threshold is a valid number in [0.0, 1.0]
- No agent has zero blocker evals

### Step 6 — Wire to A11 (Eval Runner)

The Eval Runner reads the per-agent YAMLs at engagement start, registers them, and executes the appropriate eval whenever it observes an output from the corresponding agent. The eval results stream to A19 (Audit Logger).

---

## Quality criteria

- [ ] Every in-scope agent has an eval YAML with at least one blocker
- [ ] Every research/eval agent has citation density and evidence classification evals
- [ ] Every agent with Tier 1+ actions has a HITL compliance eval
- [ ] Every blocker eval has a halt or quarantine on_fail
- [ ] Every task-specific eval has a clear pass criterion (not vague "looks good")

---

## Common failure modes

- **Eval suites that only check schema validity.** Schema is necessary but not sufficient. A schema-valid output that hallucinates is still wrong. Add citation and task-specific evals.
- **Warnings dressed up as blockers.** If a failure isn't actually disqualifying, it's a warning. Don't escalate cosmetic issues to halt-engagement.
- **Blockers dressed up as warnings.** If a failure means the output is unusable, it's a blocker. Don't pretend a hallucinated citation is a "minor issue."
- **Per-agent thresholds set by feel.** Use real numbers from observed runs. Adjust as data accumulates.
- **No eval for HITL compliance.** This is a regulatory failure waiting to happen. Every gated action must have HITL eval.

---

## Citations

- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025. (90.2% eval lift; eval methodology.)
- Anthropic. *Claude's evaluation methodology.* Various engineering blog posts.
- OpenTelemetry GenAI semantic conventions, experimental as of April 2026 (pin versions in eval scripts).

---

*BHIL CADRE Framework — SP-07 — v1.0.0*
