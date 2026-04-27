# Handoff Contract Template

*JSON Schema 2020-12 skeleton for a new handoff contract between agents. The schema is the contract; CI validates handoffs against it; A15 (handoff validator) enforces it at runtime.*

---

## Template body

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://bhil.example/cadre/contracts/<contract-slug>/v1",
  "title": "<Contract Title>",
  "description": "<One-paragraph description of what this artifact represents and which agents produce/consume it.>",
  "type": "object",
  "additionalProperties": false,
  "required": ["version", "produced_by", "produced_at", "engagement_id", "payload"],
  "properties": {
    "version": {
      "const": "v1"
    },
    "produced_by": {
      "type": "string",
      "pattern": "^A[0-9]{2}$",
      "description": "Producing agent ID (e.g., A05)."
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "engagement_id": {
      "type": "string",
      "minLength": 1
    },
    "consumed_by": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^A[0-9]{2}$"
      },
      "description": "Intended consuming agents. Optional; omit when the artifact is broadcast or filesystem-published."
    },
    "citations": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/citation"
      }
    },
    "hitl_decisions": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/hitl_decision"
      }
    },
    "audit_entries": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/audit_entry"
      }
    },
    "payload": {
      "type": "object",
      "description": "Contract-specific content. Define properties here.",
      "additionalProperties": false,
      "required": [],
      "properties": {}
    }
  },
  "$defs": {
    "citation": {
      "type": "object",
      "additionalProperties": false,
      "required": ["claim_id", "classification", "source"],
      "properties": {
        "claim_id": { "type": "string" },
        "classification": {
          "enum": ["VERIFIED", "CORROBORATED", "UNCORROBORATED", "INFERENCE"]
        },
        "source": {
          "type": "object",
          "required": ["type", "ref"],
          "properties": {
            "type": { "enum": ["primary", "secondary", "vendor", "internal"] },
            "ref": { "type": "string" },
            "retrieved_at": { "type": "string", "format": "date-time" }
          }
        },
        "rationale": { "type": "string" }
      }
    },
    "hitl_decision": {
      "type": "object",
      "additionalProperties": false,
      "required": ["tier", "reviewer", "decision", "decided_at"],
      "properties": {
        "tier": { "type": "integer", "minimum": 0, "maximum": 3 },
        "reviewer": { "type": "string" },
        "decision": { "enum": ["approve", "approve_with_conditions", "reject", "defer"] },
        "decided_at": { "type": "string", "format": "date-time" },
        "rationale": { "type": "string" },
        "conditions": { "type": "array", "items": { "type": "string" } }
      }
    },
    "audit_entry": {
      "type": "object",
      "additionalProperties": false,
      "required": ["seq", "ts", "subject_kind"],
      "properties": {
        "seq": { "type": "integer" },
        "ts": { "type": "string", "format": "date-time" },
        "subject_kind": { "type": "string" },
        "summary": { "type": "string" },
        "chain_hash": { "type": "string", "pattern": "^sha256:[0-9a-f]{64}$" }
      }
    }
  }
}
```

---

## Conventions

- **Strict mode.** `additionalProperties: false` at every object level. Producers cannot smuggle undeclared fields; consumers cannot rely on undeclared fields.
- **Standard fragments.** `citation`, `hitl_decision`, `audit_entry` are reused across contracts. When a new contract requires similar but distinct semantics, define a new fragment rather than overloading; the schema-evolution discipline (see `architecture/handoff-contracts.md`) covers when forking is appropriate.
- **Versioning.** The `version` field is a const. Schema evolution increments the version and creates a new `$id`. Old and new versions coexist during deprecation windows; A15 handles version-aware validation.
- **References.** Use `$ref` to reuse fragments. Cross-contract references (e.g., another contract's payload structure) use full URIs in `$id`-form.
- **Filesystem mirror.** Contracts are stored at `cadre/contracts/<slug>/v<n>.json` (framework-level) or `engagements/<id>/contracts/<slug>/v<n>.json` (engagement-level overrides).

## Authoring checklist

- [ ] `$id` set to the canonical URI for this contract version
- [ ] `additionalProperties: false` at every object level
- [ ] `payload.required` and `payload.properties` filled in
- [ ] Standard fragments (`citation`, `hitl_decision`, `audit_entry`) reused unmodified or explicitly forked
- [ ] Reviewed by the producing agent's owner and at least one consuming agent's owner
- [ ] CI gate added: schema validates with no warnings
- [ ] Example artifact provided at `cadre/contracts/<slug>/example.json`
- [ ] Cross-references updated in producing/consuming agent specs

## Cross-references

- `architecture/handoff-contracts.md` — full schema-evolution discipline
- `cadre/squad-keel-operations/A15-handoff-validator.md` — runtime enforcement
- `governance/audit-chain-spec.md` — audit-entry fragment definition
- `governance/evidence-classification.md` — citation classification
- `governance/hitl-policy.md` — HITL tier definitions
