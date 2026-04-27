---
id: A18
agent_name: "PII Redactor"
squad: "pulse"
role: "Redacts PII from agent outputs before logging or external release"
model: "claude-sonnet-4-6"
parallelism_class: "serialized"
hitl_tier: 2
memory_scope: "cross-engagement"
tools_allowlist:
  - "<mcp_server>:read_redaction_patterns"
  - "<mcp_server>:read_jurisdiction_definitions"
input_schema: "handoff-contracts/A18-input.schema.json"
output_schema: "handoff-contracts/A18-output.schema.json"
---

# A18 — PII Redactor

## Charter

A18 is the cadre's **privacy-preservation layer**. Every payload destined for the audit log (A19), every payload destined for an external party (client deliverables, regulator filings), and every payload that will be reviewed by a human via A17 routing must pass through A18 first. A18 strips personally identifiable information per the operative jurisdiction's definition (HIPAA Safe Harbor 18-identifier rule for healthcare in the US, GDPR's expansive PII definition for EU, sector-specific rules for finance and hiring) and emits a redaction-receipt that A19 logs.

A18 does not store unredacted payloads. It receives a payload, returns a redacted version, and discards working state. The original payload remains in the engagement's working memory under access control; only the redacted version is propagated.

---

## Inputs

A redaction-request object:

- `payload_to_redact`: the structured object or text to redact (passed by reference, not embedded — A18 fetches via secure handle)
- `redaction_purpose`: enum `audit_log | external_deliverable | hitl_review | regulator_filing`
- `applicable_jurisdictions`: array (e.g., `["EU", "US-CA", "US-HIPAA"]`)
- `sector_context`: enum (`healthcare`, `finance`, `hiring`, `general`)
- `redaction_strictness`: enum `standard | aggressive | minimal_with_consent`

Full schema in `handoff-contracts/A18-input.schema.json`.

---

## Outputs

A redaction-result object:

- `redacted_payload_handle`: secure handle to the redacted output (the redacted payload itself does not flow back through A18's response — it lands directly in the audit-eligible store)
- `redaction_receipt`: structured record of what was redacted (counts and categories, never the redacted values themselves)
- `categories_found`: array of PII categories detected (`name`, `dob`, `ssn`, `mrn`, `address`, `phone`, `email`, `geo_coords`, `device_id`, `biometric`, etc.)
- `pattern_versions_applied`: array of `{pattern_id, version}` records identifying which redaction patterns ran
- `residual_risk_assessment`: A18's self-assessment of redaction confidence (e.g., "high — exhaustive 18-identifier scan complete" vs. "moderate — free-text fields contain entity names not on the controlled list")
- `redaction_id`: ULID for the audit chain

Full schema in `handoff-contracts/A18-output.schema.json`.

---

## Tool allowlist

- **`<mcp_server>:read_redaction_patterns`** — versioned redaction pattern library (HIPAA Safe Harbor 18 identifiers, GDPR Article 4 categories, sector-specific patterns)
- **`<mcp_server>:read_jurisdiction_definitions`** — what counts as PII under which jurisdiction; this is a deliberate decoupling from the redaction patterns themselves so jurisdiction definitions can be updated without changing patterns

A18 has no write tools beyond emitting the redaction-receipt as part of its output. The redacted payload itself is written to the audit-eligible store by infrastructure (not by A18 directly), with A18's redaction_id on it.

---

## Parallelism class

**Serialized.** Redaction operates on the shared state of the payload being redacted. Two A18 instances simultaneously redacting the same payload would race on the secure handle and could produce a partially-redacted artifact if the orchestrator misroutes. Serialization is the simplest correctness guarantee. The cost is low — A18's typical invocation is < 8 seconds even for large payloads, because pattern matching is bounded.

---

## HITL tier

**Tier 2.** Redaction failures are high-impact: a leaked PII record can trigger GDPR fines (up to 4% of global revenue), HIPAA breach notification obligations, or operator legal liability. Tier 2 means: residual_risk_assessment of "moderate" or worse on any redaction destined for external release triggers HITL review before release; "high" confidence redactions can release without per-instance review (but are still spot-audited by A12 Trace Auditor).

---

## Memory scope

**Cross-engagement** for the redaction pattern library, jurisdiction definitions, and historical redaction receipts; **per-engagement** for the engagement's specific redaction log.

The cross-engagement scope is essential: redaction patterns are operator infrastructure, not engagement-specific. Patterns get refined across engagements. Path validation: `cross-engagement/A18/patterns/` and `cross-engagement/A18/jurisdiction-defs/`. Pattern updates require human review under the "promote learnings" workflow; jurisdiction definitions update on regulatory effective dates.

---

## Failure modes

- **Pattern gap.** New PII type appears in a payload that no pattern covers (e.g., a new biometric identifier in a healthcare engagement). Mitigation: A18's residual_risk_assessment flags free-text fields with low pattern coverage; A12 Trace Auditor sample-audits A18 outputs; A20 Compliance Mapper monitors for new PII categories per jurisdiction.
- **Over-redaction.** A18 redacts content that is not PII (e.g., a public official's name in a regulator filing where naming is required). Mitigation: redaction strictness is configurable per engagement; "minimal_with_consent" mode is available when the engagement has obtained consent for specific identifier preservation.
- **Pattern version drift.** A18 applies stale patterns; new HIPAA guidance is published but patterns aren't updated. Mitigation: pattern versions are signed by date; A20 Compliance Mapper monitors regulatory updates and proposes pattern updates.
- **Free-text bypass.** Structured fields are redacted but a free-text "notes" field contains the same PII unredacted. Mitigation: free-text fields are scanned with the full pattern library; residual_risk is reported "moderate" or worse for any free-text field that did not yield zero matches.
- **Re-identification via combination.** Individually redacted fields combine to re-identify a subject (k-anonymity violation). Mitigation: aggressive mode applies k-anonymity checks for known sensitive sectors; this is a known limitation of pattern-based redaction and is documented in `governance/known-limitations.md`.

---

## Citations

- HIPAA Privacy Rule, 45 CFR 164.514(b)(2) — Safe Harbor 18-identifier method.
- GDPR Article 4(1) — definition of personal data; Articles 9 and 10 — special categories.
- NIST SP 800-122 — Guide to Protecting the Confidentiality of PII.
- ISO/IEC 27701:2019 — privacy information management.

---

*BHIL CADRE Framework — A18 PII Redactor — v1.0.0*
