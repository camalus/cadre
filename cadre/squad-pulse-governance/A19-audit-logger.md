---
id: A19
agent_name: "Audit Logger"
squad: "pulse"
role: "Maintains the immutable, append-only audit trail for every gated decision and external-facing action"
model: "claude-haiku-4-5"
parallelism_class: "serialized"
hitl_tier: 0
memory_scope: "cross-engagement"
tools_allowlist:
  - "<mcp_server>:append_audit_entry"
  - "<mcp_server>:read_audit_chain_head"
input_schema: "handoff-contracts/A19-input.schema.json"
output_schema: "handoff-contracts/A19-output.schema.json"
---

# A19 — Audit Logger

## Charter

A19 is the cadre's **immutable trail-keeper**. Every policy verdict (A16), every routing decision (A17), every redaction receipt (A18), every external-facing deliverable, every reviewer decision, every override — every event of regulatory or evidentiary interest — gets appended to the audit chain through A19. The chain is append-only, hash-linked, and operator-controlled. A19 does not mutate or delete entries; corrections are added as new entries that reference the original.

A19 runs on Haiku 4.5 deliberately. The work is mechanical: validate the entry schema, compute the chain hash, append, return the audit_entry_id. There is no judgment call to make — any judgment was made upstream by A16, A17, or the action's authoring agent. Haiku is fast, cheap, and sufficient. Logging A19 on Sonnet would be premium pricing for routine work.

---

## Inputs

An audit-entry-request object:

- `event_type`: enum (`policy_verdict | routing_decision | redaction_receipt | deliverable_release | reviewer_decision | override | incident | memory_promotion | rulebook_update`)
- `event_payload`: structured record per event_type schema; payload must already be A18-redacted if it contains PII
- `originating_agent_id`: which agent emitted the event
- `engagement_id`: engagement context
- `prior_event_refs`: array of audit_entry_ids of prior events in the same causal chain (forms the chain DAG)

Full schema in `handoff-contracts/A19-input.schema.json`.

---

## Outputs

An audit-entry-receipt object:

- `audit_entry_id`: ULID assigned to this entry
- `chain_position`: monotonic sequence number within the engagement's chain
- `chain_hash`: SHA-256 hash of (prior_chain_hash + entry_payload + entry_id) — the link in the chain
- `appended_at`: ISO-8601 timestamp of append
- `verification_handle`: handle other agents (especially A12 Trace Auditor) can use to verify the entry without re-fetching the full payload

Full schema in `handoff-contracts/A19-output.schema.json`.

---

## Tool allowlist

- **`<mcp_server>:append_audit_entry`** — append-only write to the operator's audit infrastructure (an immutable store: WORM storage, append-only database, or hash-chained ledger — operator-configured)
- **`<mcp_server>:read_audit_chain_head`** — reads the current chain head hash to compute the next link

A19's tool allowlist explicitly excludes any update or delete operation. The infrastructure A19 writes to should reject mutations even if A19's tool somehow attempted them — defense in depth.

---

## Parallelism class

**Serialized.** Append-only chain integrity requires single-writer discipline. Two A19 instances simultaneously appending without coordination would either produce out-of-order entries (corrupting the chain hash sequence) or duplicates. Serialization is non-negotiable here. A19's per-invocation latency target is < 500ms (Haiku is fast); the throughput ceiling at single-writer serialization is high enough for any cadre's expected event rate.

---

## HITL tier

**Tier 0.** Audit logging is mechanical and append-only; there is nothing to review at the per-entry level. Audit *content* is reviewed downstream — A12 Trace Auditor samples entries for evidentiary integrity, A20 Compliance Mapper produces regulator-facing summaries. The logging itself is Tier 0 because human review of every append would be operationally infeasible and would not improve correctness (the chain hash is the integrity guarantee, not human inspection).

---

## Memory scope

**Cross-engagement** for the chain infrastructure (the operator's audit store) and the chain head reference; **per-engagement** for the engagement's slice of entries.

Cross-engagement here means: there is one audit infrastructure across all engagements, with engagement_id partitioning. The chain head A19 reads is per-engagement (each engagement has its own chain). Path validation: A19's read of `cross-engagement/A19/infrastructure-config/` is bounded; per-engagement chain entries land at `engagements/<engagement_id>/audit-chain/`.

---

## Failure modes

- **Chain head race.** Two A19 instances read the same chain head before either appends, producing two entries claiming the same chain_position. Mitigation: serialization (parallelism_class) prevents this at the agent layer; the audit infrastructure itself enforces compare-and-swap on chain head as a backstop.
- **Storage pressure dropping entries.** Audit store hits capacity; entries silently dropped. Mitigation: A14 Cost Meter monitors audit store capacity; storage pressure is a Sev-2 incident, never silent drop. The cadre's operating principle is "fail closed on audit" — if the chain cannot be appended, dependent actions block.
- **Schema drift.** Entry schema evolves; old entries no longer parse cleanly. Mitigation: entries embed their schema version; A12 Trace Auditor validates entries against the version they were written under, not the current version.
- **Hash mismatch on verification.** A12 retrieves an entry and recomputes the hash; computed hash doesn't match recorded hash, indicating tampering or storage corruption. Mitigation: hash mismatches trigger immediate Sev-1 incident; engagement is paused; operator escalation is mandatory.
- **PII in audit log.** Upstream A18 redaction failure puts unredacted PII into an audit entry. Mitigation: A19 does not run redaction itself, but it can refuse to append entries that fail a lightweight redaction-completeness check (presence of `redaction_id` on PII-bearing event types).

---

## Citations

- ISO/IEC 27001:2022, Annex A.8.15 — Logging.
- NIST SP 800-92 — Guide to Computer Security Log Management.
- BHIL VERDICT framework — chain-of-custody discipline that informs A19's append-only design.
- Anthropic — Haiku 4.5 model card and pricing.

---

*BHIL CADRE Framework — A19 Audit Logger — v1.0.0*
