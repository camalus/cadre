# Agent Spec Template

*Canonical structure for adding or replacing an agent. Copy this file to `cadre/squad-<name>/A<NN>-<role-slug>.md` and fill in. The framework expects every agent spec to have all sections below; missing sections fail CI validation.*

---

## Template body

```markdown
---
id: A<NN>
agent_name: <Title-Case Name>
squad: <vanta-research | atlas-product | keel-operations | pulse-governance>
role: <one-line role>
model: <claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5>
parallelism_class: <parallel-safe | serialized>
hitl_tier: <0 | 1 | 2 | 3>
memory_scope: <none | per-engagement | cross-engagement>
tools_allowlist:
  - <tool-name-1>
  - <tool-name-2>
input_schemas:
  - <schema-id>
output_schemas:
  - <schema-id>
---

# A<NN> — <Agent Name>

*<One-paragraph orientation describing why this agent exists and what it owns.>*

---

## Charter

<What this agent is responsible for. What it is not responsible for. The boundary with adjacent agents.>

## Inputs

<Structured description of inputs. Reference handoff schemas. Note any optional inputs and their default behaviors.>

## Outputs

<Structured description of outputs. Reference handoff schemas. Note any optional outputs.>

## Tool allowlist

<Specific tools this agent may invoke. Cross-reference engagement allowlist for engagement-specific overrides.>

## Parallelism class

<parallel-safe | serialized — and the rationale. Parallel-safe agents may be invoked in parallel with peer agents reading the same upstream artifacts. Serialized agents must complete before downstream consumers proceed.>

## HITL tier

<0 | 1 | 2 | 3 — and the rationale per `governance/hitl-policy.md`. Reference the action class(es) this agent produces.>

## Memory scope

<none | per-engagement | cross-engagement — and the rationale. Cite the path validation rules that apply.>

## Failure modes

<Enumerated failure modes specific to this agent, with the cadre's response for each. Cross-reference incident-response workflow for severity handling.>

## Citations

<Literature, prior art, primary sources informing this agent's design. Use evidence classification (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE) inline.>

---

## Cross-references

<Internal references to architecture, governance, prompts, workflows, and adjacent agents.>
```

---

## Conventions

- Frontmatter is YAML; agents whose tools, schemas, or model assignments change require frontmatter updates first, then content updates
- Use the `parallel-safe` / `serialized` strings exactly as shown; CI validates these
- Use the HITL tier numbers (0–3) exactly as shown; CI validates against the policy
- Tool allowlist is the framework default; engagements may further constrain (never relax) per the engagement charter
- Citations follow `governance/evidence-classification.md`; vendor-published metrics are UNCORROBORATED
- Length target: 100–300 lines, similar to existing agent specs
- Section order is fixed; CI validates section presence and order

## Cross-references

- `cadre/README.md` — overall agent-spec posture
- `governance/hitl-policy.md` — tier definitions
- `governance/evidence-classification.md` — citation discipline
- `architecture/handoff-contracts.md` — schema referencing rules
- `architecture/memory-architecture.md` — scope choice rationale
