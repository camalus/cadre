---
id: CADRE-SP-08
title: "SP-08 — Deployment Runbook"
version: "1.0"
type: sub-prompt
sequence: 8
input_artifacts: ["agents/A##-*.md", "evals/*.yaml", "hitl-gate-map.md", "mcp-config.json", "memory-config.md"]
output_artifact: "runbook.md"
hitl_tier: 2
---

# SP-08 — Deployment Runbook

*Authors the engagement-specific deployment runbook: phased rollout plan, cost monitoring SLOs, incident escalation paths, and the cutover checklist. Outputs `runbook.md`.*

---

## Purpose

The runbook is the document the engagement team works from after the cadre goes live. It is operational, not aspirational. Every step is something a named human or a named agent can execute. Every threshold is a number. Every escalation has a named owner.

The runbook also functions as evidence of operational maturity for compliance reviews — ISO 42001 Clauses 6–10 and NIST AI RMF Manage function both expect operators to have documented operational procedures.

---

## Inputs

- All prior engagement artifacts: `cadre-blueprint.md`, `agents/`, `handoff-contracts/`, `mcp-config.json`, `memory-config.md`, `hitl-gate-map.md`, `evals/`
- **`templates/runbook-template.md`** — runbook scaffolding
- **`workflows/tier-N.md`** — for SKU-specific operational expectations

---

## Output

**`engagements/<id>/runbook.md`** — the engagement-specific runbook. Standard sections:

1. **Engagement summary** — client, scope, SKU tier, key dates, named contacts
2. **Cadre topology** — visual or tabular summary of the 20 (or fewer) agents and their relationships
3. **Phased rollout plan** — what goes live when
4. **Cost SLOs and monitoring** — token budget, session-hour budget, alert thresholds, owner
5. **Eval SLOs** — pass-rate targets per agent, alert thresholds, owner
6. **Latency SLOs** — p95 latency targets per agent
7. **Incident response** — playbook for the most likely failure modes
8. **HITL escalation** — what happens when a named reviewer is unavailable
9. **Cutover checklist** — what must be true before go-live
10. **Rollback plan** — how to disable the cadre and revert to prior state

---

## Step-by-step

### Step 1 — Define the rollout phases

Default three-phase rollout (adjust per SKU tier):

- **Phase 1 — Shadow mode** (1–2 weeks): cadre runs alongside the existing process; outputs reviewed but not used in production. Eval suite establishes baseline.
- **Phase 2 — Limited production** (2–4 weeks): cadre takes ownership of a defined subset (e.g., one team, one product line, one region). Tier 2+ HITL gates active on all external-facing actions.
- **Phase 3 — Full production**: cadre takes the full scope. Continuous eval and audit. Quarterly review of cadre composition.

For Tier-2 (Readiness Diagnostic) engagements, there is no production rollout — the runbook is a recommendation for future implementation, not an operational document.

### Step 2 — Set cost SLOs

From SP-04 budget envelope:

- **Daily token budget** — total tokens per day across the cadre
- **Per-agent daily ceiling** — most agents should be at <30% of total daily budget
- **Alert thresholds** — A14 (Cost Meter) alerts at 50%, 75%, 90% of daily budget
- **Owner** — name the human responsible for cost monitoring

Document the per-engagement projection vs. actual reconciliation cadence (weekly is typical).

### Step 3 — Set eval SLOs

From SP-07 eval suite:

- **Per-agent blocker pass rate** — typically 100% (any blocker fail halts the agent)
- **Per-agent warning pass rate** — typically 95%+
- **Cadre composite pass rate** — weighted average of per-agent rates
- **Owner** — typically the operator's lead engineer or the BHIL engagement lead

### Step 4 — Set latency SLOs

Per-agent p50, p95, p99 latency targets. Defaults from SP-07 stand unless adjusted per client expectation. For real-time customer-facing cadres, p95 latency budgets tighten significantly.

### Step 5 — Author the incident playbook

For each of the documented failure modes in `architecture/failure-modes.md`, write a paragraph-length response procedure:

- **Hallucinated citation released externally** — quarantine the output; trigger A19 audit; root-cause via A12 trace audit; update VANTA prompts; report to client per disclosure policy
- **Cost runaway (90% of daily budget at noon)** — halt non-critical subagent dispatches; alert A14 owner; emergency cadre composition review
- **HITL reviewer unavailable for Tier 3 action** — hold the action; trigger named alternate; escalate to operator if alternate also unavailable; document the hold duration in audit
- **MCP server outage** — fall back to declared alternate per `mcp-config.json` if available; otherwise halt dependent agents; alert MCP owner
- **Evidence Classifier (A02) flags >5% INFERENCE on a research output** — automatic re-dispatch to VANTA with elevated scrutiny; if still >5%, escalate to operator
- **Two parallel-safe subagents return contradictory evidence** — orchestrator dispatches A02 tie-breaker; if unresolved, escalate

### Step 6 — Define the HITL escalation tree

For each named reviewer (from SP-06), document:

- Primary contact method (email, Slack, phone)
- Hours of availability
- Named alternate
- Escalation if both unavailable

Tier 3 actions never proceed without two reviewers; document the "hold and escalate" pattern with maximum hold duration.

### Step 7 — Author the cutover checklist

Pre-go-live checklist. Every item must be true before the cadre takes production load:

- [ ] All in-scope agent specs reviewed and signed off
- [ ] All handoff contracts validated
- [ ] MCP server credentials provisioned and tested
- [ ] Memory paths provisioned with validation tests passing
- [ ] HITL reviewers notified, on call, and confirmed available
- [ ] Eval suite running in shadow mode for the prior phase with passing rates
- [ ] Cost meter operational with alerts wired
- [ ] Audit log destination provisioned with retention configured
- [ ] Rollback plan tested at least once in lower environment
- [ ] Disclosure language reviewed by client legal (per client jurisdiction)
- [ ] Data-residency compliance confirmed (US/EU per `mcp-config.json`)
- [ ] Sector-specific compliance items (HIPAA / SR 11-7 / AEDT / etc.) confirmed

### Step 8 — Author the rollback plan

How to disable the cadre and revert to prior state:

- Disable orchestrator dispatch (the orchestrator queues no new subagent invocations)
- Drain in-flight invocations (allow current parallel subagents to complete; halt new dispatches)
- Snapshot the current state of all per-engagement memory
- Notify all named HITL reviewers that the cadre is offline
- Revert any production-routed traffic to the prior process
- Preserve the audit trail; do not delete

Document expected rollback duration (typically 15–60 minutes for a clean drain).

### Step 9 — Write `runbook.md`

Use `templates/runbook-template.md` as the scaffold. Persist to `engagements/<id>/runbook.md`. Distribute to all named participants.

---

## Quality criteria

- [ ] Every phase has clear entry and exit criteria
- [ ] Every SLO has a number (no "fast" or "good")
- [ ] Every alert threshold has a named owner
- [ ] Every documented failure mode has a response procedure
- [ ] Every named reviewer has a named alternate
- [ ] Cutover checklist is comprehensive (all 12 standard items + sector-specific)
- [ ] Rollback plan has an expected duration

---

## Common failure modes

- **Aspirational runbooks that no one will execute.** Test the runbook in lower environments before signing off.
- **SLOs without owners.** "We will monitor" is not ownership. Name a person.
- **Incident playbooks that say "escalate to engineering."** Be specific. Which engineer? On what schedule? With what runbook?
- **Cutover checklists copy-pasted without sector adjustment.** Healthcare cadres need HIPAA confirmations. Hiring cadres need AEDT confirmations. Don't elide.
- **Rollback plans that don't preserve audit trails.** Audit trails survive rollback. Anything else is a regulatory failure.

---

## Citations

- ISO/IEC 42001:2023 — AI management systems, Clauses 6–10 (operational planning, evaluation, improvement).
- NIST AI Risk Management Framework, Manage function.
- Google SRE Workbook — SLO methodology (latency, cost, error-rate budgeting).
- Anthropic. *Claude API* documentation — pricing and rate-limit references.

---

*BHIL CADRE Framework — SP-08 — v1.0.0*
