# Templates

*Reusable templates referenced by prompts, agent specs, workflows, and governance documents. Templates are skeletons, not policy. They make the right structure easy to produce; the policy of when to use them lives elsewhere.*

---

## Layout

- `agent-spec-template.md` — YAML frontmatter + canonical sections for a new agent
- `handoff-contract-template.md` — JSON Schema 2020-12 skeleton for a new contract
- `engagement-charter-template.md` — engagement-charter skeleton invoked by `workflows/new-engagement-startup.md`
- `incident-postmortem-template.md` — post-mortem skeleton invoked by `workflows/incident-response.md`
- `audit-finding-template.md` — finding skeleton used by A12 (trace auditor)
- `review-decision-template.md` — Tier 2 / Tier 3 review-decision form

## How to use templates

Treat templates as starting points. Copy the template into the appropriate engagement or framework location, fill in the engagement-specific content, and submit through the appropriate review path. Templates are not authoritative; the policy documents they reference are authoritative.

When a template needs to evolve, route the change through the framework's normal change discipline (Conventional Commits with `cadre(templates)` scope, peer review, CI). Do not edit templates in-place during an active engagement; copy and modify the engagement-side instance instead.

## Cross-references

- `cadre/README.md` — overall agent-spec posture
- `architecture/handoff-contracts.md` — contract structure rationale
- `workflows/` — workflows that invoke specific templates
