# Workflows

*Multi-agent operational sequences. Each workflow is a named, reproducible procedure that crosses agent boundaries and has explicit start conditions, exit conditions, and audit emissions.*

---

## Layout

- `new-engagement-startup.md` — intake, scoping, cadre composition, charter
- `weekly-cadence.md` — recurring eval, audit, and cost-review cycles
- `incident-response.md` — Sev-1 / Sev-2 / Sev-3 flow, including A13 ownership
- `engagement-closeout.md` — deliverable finalization, archive, learnings extraction
- `promote-learnings.md` — the cross-engagement memory promotion workflow

## Reading order

If you are new to the framework, read in the order above. New-engagement-startup establishes the context that all subsequent workflows depend on. Weekly cadence is the steady-state. Incident response and engagement closeout are the punctuated events. Promote-learnings is the cross-engagement boundary crossing.

## What workflows are not

Workflows are not the same as prompts (in `prompts/`) or agent specs (in `cadre/`). Prompts produce design artifacts; agent specs describe individual agents. Workflows describe how the agents operate together over time. A workflow may invoke many prompts and many agents; the workflow is the connective tissue.

## Cross-references

- `prompts/SP-08-deployment-runbook.md` — single-engagement deployment sequence; workflows describe what happens after deployment
- `governance/hitl-policy.md` — tier model invoked by every workflow
- `governance/audit-chain-spec.md` — emission discipline that workflows follow
