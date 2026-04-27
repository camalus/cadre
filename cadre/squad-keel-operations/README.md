# Squad KEEL — Operations

*KEEL is the cadre's structural backbone — the runtime layer that runs evaluations, audits traces, responds to incidents, meters cost, and validates handoffs. The name is intentional: a keel is what keeps a vessel upright and on course. Mixed parallelism — eval and audit are parallel-safe; incident response and cost metering are serialized because they mutate engagement-state.*

---

## Charter

KEEL is the operational integrity layer. Every other squad produces deliverables; KEEL keeps the cadre itself running correctly. Its responsibilities span four domains:

1. **Quality** — A11 Eval Runner executes the per-agent eval suites against every output
2. **Observability** — A12 Trace Auditor reads OTel traces and flags anomalies
3. **Resilience** — A13 Incident Responder owns the playbook when something breaks
4. **Cost discipline** — A14 Cost Meter tracks token spend, session-hours, and budget against engagement SLA
5. **Contract integrity** — A15 Handoff Validator validates JSON Schema strict-mode contracts at every inter-agent handoff

The four domains map onto the operational tasks an SRE team would handle in a traditional services context, adapted to multi-agent runtime concerns.

---

## Roster

| ID | Name | Role | Parallelism |
|---|---|---|---|
| [A11](A11-eval-runner.md) | Eval Runner | Executes the per-agent eval suite against agent outputs | parallel-safe |
| [A12](A12-trace-auditor.md) | Trace Auditor | Reads OTel-compliant traces and flags anomalies | parallel-safe |
| [A13](A13-incident-responder.md) | Incident Responder | Owns the incident playbook | **serialized** |
| [A14](A14-cost-meter.md) | Cost Meter | Tracks token spend and session-hours | **serialized** |
| [A15](A15-handoff-validator.md) | Handoff Validator | Validates JSON Schema strict-mode contracts | parallel-safe |

---

## Mixed parallelism rationale

KEEL is the squad where the read/write asymmetry rule is most visible:

- **A11, A12, A15 — parallel-safe.** They read state (agent outputs, traces, schemas) and emit verdicts. They don't mutate the engagement's substantive state.
- **A13, A14 — serialized.** They mutate engagement-state (incident records, cost ledger). Concurrent writes here corrupt the engagement's operational records.

This is the same logic A09 follows in ATLAS: anything that owns and writes a single shared artifact must serialize. The cost ledger and incident log are exactly such artifacts.

---

## Coordination pattern

KEEL agents fire continuously throughout the engagement:

- A11 fires whenever an agent produces an output (parallel-safe; runs alongside other evals)
- A12 fires periodically and on incident-detection signals (parallel-safe; runs across batches of traces)
- A13 fires on incident escalation; serialized; only one A13 instance per incident
- A14 fires on every billable agent invocation; serialized; tracks cumulative spend
- A15 fires at every inter-agent handoff; parallel-safe; runs alongside other handoffs

The orchestrator dispatches them as side-effects of other agent activity rather than as standalone steps in the engagement sequence.

---

## HITL discipline within KEEL

KEEL is mostly Tier 0 or Tier 1. Two exceptions:

- **A13 Incident Responder** — Tier 2. Incidents have stakeholder-impact consequences (notifications, customer comms, regulator disclosure). Single-human approval on each runbook step that affects stakeholders.
- **A14 Cost Meter** — Tier 1. Cost overruns trigger budget renegotiation; alerts go to the named cost-monitoring owner.

A11 (Eval Runner) is Tier 0 because eval execution itself is internal; the *eval failures* it produces are gated downstream by whichever agent owns the failed output.

---

## Memory scope

- **A11, A12** — `cross-engagement` for eval criteria templates and trace-anomaly rulebooks; `per-engagement` for actual run results
- **A13** — `per-engagement` for incident records (incidents are engagement-specific)
- **A14** — `per-engagement` for cost ledger; `cross-engagement` for cost-projection models calibrated against historical engagements
- **A15** — `none`; each handoff is independently validated

---

## Common failure modes (squad-level)

- **Eval pass-rate gaming.** Setting eval thresholds too loose so everything passes. Mitigation: gate reviewer on eval suites checks for meaningful blocker definitions.
- **Trace audit silent failures.** Anomaly detection that doesn't fire because the rules are too narrow. Mitigation: A12 maintains its own meta-evals that test the audit ruleset against known-bad traces.
- **Incident response playbook drift.** Runbooks that get out of sync with reality. Mitigation: A13's runbook is versioned; quarterly review required.
- **Cost meter under-counting.** Token usage from MCP tool calls or sub-tool invocations not captured. Mitigation: A14 reconciles against the actual API billing record at engagement close; discrepancies are escalated.
- **Handoff validator over-fitting.** A15 schemas that are too strict and reject valid outputs. Mitigation: schemas reviewed during SP-03; A15's own evals test the schema set against known-valid outputs.

---

## Citations

- OpenTelemetry GenAI semantic conventions, experimental status as of April 2026.
- Google SRE Workbook — SLO, error budget, and incident response patterns.
- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025. (Cost discipline and observability rationale.)
- Cognition AI. *Don't Build Multi-Agents.* June 12, 2025. (Why A13 and A14 must serialize.)

---

*BHIL CADRE Framework — KEEL Squad — v1.0.0*
