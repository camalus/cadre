# Audit Chain Specification

*The append-only, hash-linked log that records every consequential action the cadre takes. The chain is the principal evidence artifact for incidents, audits, regulator inquiries, and operator due-diligence. A19 (audit logger) is the only sanctioned writer; A12 (trace auditor) is the principal verifier.*

---

## Design principles

The audit chain is built on four non-negotiable principles:

1. **Append-only.** Entries are never modified or deleted. Corrections are themselves new entries that reference the original.
2. **Hash-linked.** Each entry contains the hash of the previous entry, forming a chain. Tampering with any entry breaks every subsequent hash.
3. **Fail-closed on audit.** When the cadre cannot write to the chain, downstream consequential actions are blocked, not silently dropped. The chain is a precondition, not a side effect.
4. **Independent verifiability.** Anyone with read access to the chain can verify integrity without trusting the cadre that produced it. The verifier needs only the public hash function and the chain bytes.

---

## Entry structure

Every chain entry is a JSON object with a stable schema. The current schema version is `v1`:

```
{
  "version": "v1",
  "seq": 12345,
  "ts": "2026-04-26T16:30:00.000Z",
  "engagement_id": "eng-2026-042",
  "actor": {
    "type": "agent" | "human" | "system",
    "id": "A19" | "reviewer:carla.j@operator.example" | "system:rollback",
    "role": "audit-logger" | "tier-2-reviewer" | "incident-responder"
  },
  "subject": {
    "kind": "handoff" | "decision" | "memory_write" | "tool_call" | "incident" | "rollback" | "promotion" | "policy_change",
    "ref": "<artifact-path or external ID>"
  },
  "tier": 0 | 1 | 2 | 3,
  "classification": "VERIFIED" | "CORROBORATED" | "UNCORROBORATED" | "INFERENCE" | null,
  "summary": "<short human-readable description>",
  "payload_hash": "sha256:<hex>",
  "prev_hash": "sha256:<hex>",
  "chain_hash": "sha256:<hex>"
}
```

Field semantics:

- **version.** Schema version. Schema evolution follows the same JSON Schema 2020-12 evolution discipline as handoff contracts (see `architecture/handoff-contracts.md`).
- **seq.** Monotonically increasing integer per engagement. Gaps in the sequence are themselves a control finding.
- **ts.** ISO 8601 UTC timestamp. The cadre's clock is provider-trusted; clock drift is an A12 audit concern.
- **engagement_id.** The engagement under which the action occurred. Cross-engagement actions (promote-learnings, framework policy changes) use a reserved `cadre-system` value.
- **actor.** Who performed the action. Agents identify by ID (A01–A20); humans identify by stable handle resolved against the operator's reviewer roster; system actions identify by the originating subsystem.
- **subject.** What the entry documents. The `ref` field points to the artifact or external ID; the audit chain itself does not embed the full artifact, only its hash.
- **tier.** The HITL tier under which the action was authorized. See `governance/hitl-policy.md`.
- **classification.** When the action involves a claim, the evidence classification. See `governance/evidence-classification.md`. Mechanical actions have null classification.
- **summary.** Short human-readable description for chain readers. Not the artifact itself; the artifact is referenced by `subject.ref` and hashed in `payload_hash`.
- **payload_hash.** SHA-256 of the canonical JSON serialization of the action's full payload. Allows external verification that the artifact pointed to by `ref` matches what was logged.
- **prev_hash.** SHA-256 of the immediately preceding entry's `chain_hash`. The chain head has `prev_hash = "sha256:0000...0000"` (genesis).
- **chain_hash.** SHA-256 of the canonical serialization of all preceding fields in this entry. This is the field that links the chain.

---

## Hashing discipline

The chain uses SHA-256 throughout. Canonical serialization follows RFC 8785 (JSON Canonicalization Scheme) so that hashes are reproducible across implementations.

The verifier computes each entry's `chain_hash` from the entry's contents and verifies that the next entry's `prev_hash` matches. Any mismatch indicates tampering or corruption. A12 runs full-chain verification at every audit cycle and after every incident.

The `payload_hash` is verified against the artifact pointed to by `ref`. When the artifact has been moved, archived, or sanitized, the verification chain depends on the operator preserving the artifact in its original form (or preserving a hash-equivalent form). A20 maintains the artifact-preservation policy per engagement.

---

## What gets logged

Every action in the following categories produces a chain entry:

- **Handoff acceptance/rejection.** When agent X passes an artifact to agent Y, A15 (handoff validator) emits an entry recording the schema validation outcome.
- **HITL decisions.** Every Tier 1, 2, or 3 decision produces an entry. The reviewer's identity, decision, and rationale are recorded.
- **Memory writes.** Every write to per-engagement or cross-engagement memory produces an entry. The path validator emits both accepted and rejected writes.
- **Tool calls (Tier 2 and above).** Tool calls that produce external effects (external API writes, MCP server actions with side effects) are logged. Read-only Tier 0 tool calls are sampled rather than fully logged, with the sample rate documented per engagement.
- **Incidents.** A13 (incident responder) opens, updates, and closes incidents through chain entries. The incident's full timeline is reconstructable from the chain.
- **Rollbacks.** Every rollback is itself a chain entry. The rollback does not delete prior entries; it appends a rollback entry that references the affected entries.
- **Learning promotions.** The promote-learnings workflow emits entries at proposal, review, sanitization, and publication.
- **Policy changes.** Modifications to operator policy, allowlists, reviewer rosters, or HITL tier defaults produce entries under the `cadre-system` engagement.

Tier 0 mechanical actions are not individually logged; they are summarized in periodic batch entries that record the count, the agent, and a representative sample. The sampling discipline is documented in `cadre/squad-keel-operations/A12-trace-auditor.md`.

---

## Storage and retention

The chain is stored as immutable append-only objects. Specific storage substrate is operator-chosen; the framework's reference deployment uses object storage with object-lock (write-once-read-many) semantics. Operators with stricter requirements may use append-only databases with cryptographic anchoring to external timestamping services.

Retention follows the memory policy retention schedule (see `governance/memory-policy.md`) with one override: the chain is never purged earlier than the underlying artifacts it references. Purging the chain ahead of artifacts orphans the verification path and is treated as a Sev-1 control failure.

Chain compaction (older entries summarized into batch entries) is permitted under the same canonical serialization discipline, with the compaction itself being a chain entry. Operators pursuing compaction must document the compaction policy and obtain Tier 3 approval; the default is no compaction.

---

## Independent verification

The verifier needs:

- Read access to the chain
- The SHA-256 hash function (no trust in the cadre needed)
- The canonical serialization rules (RFC 8785)
- Read access to artifacts (for `payload_hash` verification, where in scope)

The verification procedure:

1. Read entries in sequence order
2. For each entry, recompute `chain_hash` from the entry's contents
3. Verify the next entry's `prev_hash` matches the recomputed `chain_hash`
4. For entries where artifact verification is in scope, recompute `payload_hash` from the canonical serialization of the artifact and verify the match
5. Report any mismatches

The reference verification implementation lives in `tools/scripts/verify_audit_chain.py` and is exercised in the CI pipeline.

---

## Failure handling

- **Write failure.** When the chain write fails, the cadre fails the action it would have logged. The operation is not retried silently; A13 opens an incident; the operator's compliance function is notified. The cadre does not proceed past a failed log write.
- **Verification failure.** When verification detects a mismatch, A12 opens a Sev-1 finding; A13 begins incident response; further consequential actions in the affected engagement are paused until the chain integrity is restored or the affected scope is bounded.
- **Storage failure.** Storage outages are treated as cadre outages. The cadre does not buffer entries in volatile memory and proceed; entries that cannot be written are equivalent to actions that did not happen. The deployment runbook (SP-08) covers storage-failure response.
- **Clock drift.** When the cadre's clock disagrees with the trusted clock (typically the provider's authenticated time), A12 opens a finding. Entries with timestamps inconsistent with the surrounding entries are flagged for investigation.

---

## What the chain does not do

The audit chain does not:

- Provide non-repudiation against the operator. The operator runs the cadre and could in principle produce the chain bytes. External anchoring (e.g., periodic chain-head publication to a public ledger or a regulator-trusted timestamping service) is required for true non-repudiation and is operator-configured rather than framework-default.
- Replace operator records-management. Sector-specific records retention obligations may require artifact preservation outside the chain; the chain references rather than embeds artifacts.
- Replace external auditing. The chain is the substrate that enables auditing efficiently; it is not itself an audit.
- Detect insider tampering by an actor with full system privileges. The principal defense is independent verification by parties without those privileges; the chain makes external verification feasible but not automatic.

---

## Cross-references

- `cadre/squad-pulse-governance/A19-audit-logger.md` — the writer
- `cadre/squad-keel-operations/A12-trace-auditor.md` — the verifier
- `cadre/squad-keel-operations/A13-incident-responder.md` — failure response
- `governance/hitl-policy.md` — tier definitions logged in entries
- `governance/evidence-classification.md` — classification field source of truth
- `governance/memory-policy.md` — interaction with memory-write logging
- `governance/known-limitations.md` — gaps in current chain coverage
- `architecture/handoff-contracts.md` — schema evolution discipline shared with the chain
