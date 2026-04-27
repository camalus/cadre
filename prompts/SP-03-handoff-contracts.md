---
id: CADRE-SP-03
title: "SP-03 — Handoff Contracts"
version: "1.0"
type: sub-prompt
sequence: 3
input_artifacts: ["agents/A##-*.md"]
output_artifact: "handoff-contracts/*.schema.json"
hitl_tier: 1
---

# SP-03 — Handoff Contracts

*Produces JSON Schema strict-mode contracts for every inter-agent handoff. These schemas are validated by A15 (Handoff Validator) at runtime; an invalid handoff halts the engagement.*

---

## Purpose

Typed handoffs are what makes CADRE auditable. Every input to and output from a subagent is a JSON object validated against a schema. The schemas live in `engagements/<id>/handoff-contracts/` and are referenced by every agent spec.

The discipline is borrowed from the Anthropic structured outputs pattern: **`strict: true`** on every schema, no additional properties, no fallback-to-string. If the agent can't produce a payload that validates, the handoff fails loudly rather than degrading silently.

---

## Inputs

- **`engagements/<id>/agents/A##-*.md`** — agent specs from SP-02
- **`templates/handoff-contract-template.json`** — schema scaffolding
- **`architecture/handoff-contracts.md`** — the architectural pattern

---

## Output

Two JSON Schema files per agent, written to `engagements/<id>/handoff-contracts/`:

- **`A##-input.schema.json`** — schema for what the orchestrator passes IN to the agent
- **`A##-output.schema.json`** — schema for what the agent returns OUT to the orchestrator

Each schema must:

- Use **JSON Schema Draft 2020-12**
- Set **`additionalProperties: false`**
- Mark all required fields explicitly in `required`
- Include `description` strings on every field (these become the agent's docstrings)
- Use **`strict: true`** at the root

---

## Step-by-step

### Step 1 — Read the agent's I/O summaries

From each agent spec's "Inputs" and "Outputs" sections, extract the field list. The summaries are prose; SP-03's job is to formalize them into schema.

### Step 2 — Construct the input schema

For each input field:

- **Name** — snake_case, descriptive
- **Type** — string / number / integer / boolean / array / object (avoid `null` unless the field is genuinely optional)
- **Description** — one sentence explaining what the field carries
- **Constraints** — `enum` for closed sets, `pattern` for formats (UUIDs, ISO dates), `minimum`/`maximum` for numerics, `minLength`/`maxLength` for strings

### Step 3 — Construct the output schema

Output schemas are stricter than input schemas because they're what gets logged to the audit trail. Every output schema must include:

- **`agent_id`** — string, must match the agent's ID (e.g., "A01")
- **`engagement_id`** — string, format UUID
- **`timestamp`** — string, format date-time (ISO 8601)
- **`status`** — enum: ["success", "partial", "failure", "escalated"]
- **`payload`** — the agent's actual output, structured per its charter
- **`citations`** — array of citation objects (for any agent that makes empirical claims)
- **`evidence_classification`** — enum per claim: ["VERIFIED", "CORROBORATED", "UNCORROBORATED", "INFERENCE"]
- **`hitl_tier_required`** — integer 0–3 (the agent declares whether its output needs gating)

### Step 4 — Validate the schemas

Run the schemas through a JSON Schema validator (`tools/scripts/validate-handoff.py` includes one). Confirm:

- Every schema parses as valid Draft 2020-12
- Every `$ref` resolves
- Every required field has a description
- No `additionalProperties: true` slipped in

### Step 5 — Reference from agent specs

Update each `engagements/<id>/agents/A##-*.md` so its frontmatter `input_schema` and `output_schema` fields point to the correct schema paths.

---

## Standard schema fragments

These fragments are reused across many agents. Reference them via `$ref` rather than duplicating.

### `citation` object

```json
{
  "type": "object",
  "required": ["title", "source", "url", "access_date"],
  "additionalProperties": false,
  "properties": {
    "title": { "type": "string" },
    "source": { "type": "string", "description": "Publisher or domain" },
    "url": { "type": "string", "format": "uri" },
    "access_date": { "type": "string", "format": "date" },
    "author": { "type": "string" },
    "publication_date": { "type": "string", "format": "date" },
    "evidence_class": {
      "type": "string",
      "enum": ["VERIFIED", "CORROBORATED", "UNCORROBORATED", "INFERENCE"]
    }
  }
}
```

### `hitl_decision` object

```json
{
  "type": "object",
  "required": ["tier", "reviewer", "decision", "timestamp"],
  "additionalProperties": false,
  "properties": {
    "tier": { "type": "integer", "minimum": 0, "maximum": 3 },
    "reviewer": { "type": "string", "description": "Named human reviewer (Tier 2+)" },
    "decision": { "type": "string", "enum": ["approved", "rejected", "modified"] },
    "modifications": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "rationale": { "type": "string" }
  }
}
```

### `audit_entry` object

```json
{
  "type": "object",
  "required": ["entry_id", "engagement_id", "agent_id", "action", "timestamp"],
  "additionalProperties": false,
  "properties": {
    "entry_id": { "type": "string", "format": "uuid" },
    "engagement_id": { "type": "string", "format": "uuid" },
    "agent_id": { "type": "string", "pattern": "^A[0-9]{2}$" },
    "action": { "type": "string" },
    "input_artifact": { "type": "string", "description": "Path to input filesystem artifact" },
    "output_artifact": { "type": "string", "description": "Path to output filesystem artifact" },
    "timestamp": { "type": "string", "format": "date-time" },
    "hitl_decision": { "$ref": "#/definitions/hitl_decision" }
  }
}
```

---

## Quality criteria

A passing handoff contract set has:

- [ ] One input schema and one output schema per in-scope agent
- [ ] All schemas validate as Draft 2020-12
- [ ] All schemas use `additionalProperties: false`
- [ ] All required fields have description strings
- [ ] All output schemas include the standard envelope (agent_id, engagement_id, timestamp, status, citations, hitl_tier_required)
- [ ] Agent specs reference the correct schema paths

---

## Common failure modes

- **Loose schemas with `additionalProperties: true`.** This defeats the entire purpose. Strict mode or nothing.
- **Optional fields without explicit `required` discipline.** A field that's "usually present" should either be required (with a clear failure path when absent) or genuinely optional (tolerated downstream).
- **String-typed fields that should be enums.** "status" as a free-form string is a debugging nightmare. Enumerate the values.
- **No timestamps.** Every output needs a timestamp for the audit trail. No exceptions.
- **No citation classification.** Every claim from a research or evaluation agent must declare its evidence class. UNCORROBORATED is acceptable; absent classification is not.

---

## Citations

- JSON Schema Specification, Draft 2020-12.
- Anthropic. *Structured Outputs* documentation. (`strict: true` pattern.)
- OpenAI. *Structured Outputs* announcement, August 2024. (Originator of the `strict` mode pattern that Anthropic later adopted.)

---

*BHIL CADRE Framework — SP-03 — v1.0.0*
