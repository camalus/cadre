# Known Limitations

*An honest catalog of the gaps, edge cases, and known-imperfect controls in the current CADRE design. The point is not to apologize but to make the limitations visible so operators can compensate and so the framework can be improved deliberately.*

---

## Why this file exists

Every framework has limitations. Frameworks that pretend otherwise produce surprises during incidents and embarrassments during audits. CADRE chooses to document its limitations explicitly, in one canonical location, so that:

- Operators can apply compensating controls where the cadre's own controls fall short
- Reviewers know where to apply heightened scrutiny
- Future framework versions have a clear backlog of substantive improvements
- A20 (compliance mapper) can reference this file when producing per-engagement risk registers

A18 (PII redactor) explicitly links to this file as a guardrail: when the redactor's coverage is incomplete, the failure mode is "stop and route to Tier 2," not "best-effort and ship."

---

## PII redaction: pattern coverage gaps

A18 uses pattern-based redaction (regex, named-entity recognition) plus an allowlist/blocklist policy. Pattern-based redaction is necessary but not sufficient. Known gaps:

- **Indirect identifiers.** Job title plus rare condition plus date can re-identify an individual even when name and SSN are removed. Pattern-based redaction cannot detect this combinatorial leakage.
- **Free-text quasi-identifiers.** Descriptive phrases ("the senior VP who just relocated from the Boston office") can identify individuals without containing any structured identifier.
- **Domain-specific identifiers.** Healthcare-specific identifiers (patient encounter IDs, prescription numbers), financial-specific identifiers (loan numbers, account fragments), and education-specific identifiers (student IDs) require sector-tuned patterns. The default pattern set covers common general-PII patterns; sector engagements require operator-supplied pattern packs.
- **Adversarial inputs.** Inputs deliberately constructed to evade redaction (Unicode normalization tricks, character substitutions, custom encodings) are out of scope for pattern-based redaction.

Compensating control: A18's HITL tier is 2 when output is destined for external release. Tier 2 review is the safety net for pattern coverage gaps. A20 maintains the operator-specific pattern pack and is responsible for sector tuning.

---

## K-anonymity: not enforced by default

CADRE does not enforce k-anonymity, l-diversity, or t-closeness on aggregated outputs. When a cadre produces aggregate statistics (e.g., a market segmentation summary, a portfolio-level metric), the result can in principle re-identify individuals if the segments are too small.

Compensating control: when the cadre produces aggregations from sensitive data, A20 (compliance mapper) flags the aggregation for k-anonymity review. The review itself is operator-side; CADRE supplies the underlying counts but does not enforce minimum cell size by default.

Future framework version: tooling-layer enforcement of minimum cell sizes for sensitive aggregations is in the v1.x backlog. Until then, the gap is operator-mitigated.

---

## RFC 8707 Resource Indicators: absent operators

RFC 8707 (Resource Indicators for OAuth 2.0) is required by the MCP specification revision 2025-11-25 and is the principal defense against confused-deputy attacks across MCP servers.

The limitation: not all third-party MCP servers in the field correctly implement RFC 8707. When CADRE connects to an MCP server that does not support resource indicators, the architectural defense degrades. The cadre's response (per `architecture/mcp-integration.md`) is to refuse the connection by default and require explicit operator opt-in for known-non-conformant servers, with documented compensating controls.

Compensating controls when an operator opts into a non-conformant server:

- The connection is treated as a higher trust tier than a conformant connection (effectively Tier 3 caution applied to all uses)
- Per-tool allowlists are enforced strictly; broad allowlists are rejected
- A12 audits every interaction with the non-conformant server; pattern anomalies trigger A13
- The opt-in itself is logged as a Tier 3 decision in the audit chain

This is a degradation, not a workaround. The honest framing: until the MCP ecosystem reaches conformance, operators using non-conformant servers carry residual risk that CADRE controls only partially address.

---

## Eval coverage: cannot prove absence of failure modes

The eval harness (SP-07, A11) measures specific behaviors against specific inputs. No finite eval set can prove the absence of all failure modes. Specific gaps:

- **Distributional shift.** Evals built on past data may not predict behavior on future data with different statistics.
- **Adversarial inputs.** Evals built on benign data do not measure adversarial robustness.
- **Long-tail failure modes.** Failures that occur in <0.1% of inputs may not be detected by reasonable eval set sizes.
- **Compositional failures.** Cadres with many agents can fail in ways no single-agent eval catches.

Compensating controls: A12 trace auditing on production traffic; A13 incident response with mandatory post-mortem; the eval harness is augmented after every incident with regression tests for the specific failure mode. The honest framing: evals measure known failures, not all failures.

---

## Citation provenance: best-effort, not absolute

A02 (evidence classifier) and A04 (source archivist) maintain citation provenance, but the chain has known gaps:

- **Source-side modifications.** When a primary source is modified after the cadre cited it, the citation may no longer support the claim. A04 archives at read time, but archiving is not legally equivalent to the live source.
- **Aggregator interposition.** When a source is reached through an aggregator, the aggregator may have introduced summarization errors. The cadre's policy is to follow citations to primary sources where feasible, but feasibility varies.
- **Paywalled sources.** When the source is paywalled, the cadre may rely on the abstract or a cached version. The classification accounts for this with the UNCORROBORATED label, but the gap remains visible.

Compensating control: A04's archiving captures the source state at read time; A12 spot-checks citations during audit cycles; reviewers are obligated to follow load-bearing citations themselves before approving Tier 2 or Tier 3 outputs.

---

## Reviewer roster: jurisdiction and sector matching

The HITL policy requires reviewer roster discipline (jurisdiction match, sector match, role match, load match). The limitation: operator rosters frequently lack reviewers with all four attributes for niche cases (e.g., a banking-AI-Act-EU-jurisdiction Tier 3 case).

Compensating control: the policy permits temporary external reviewers (qualified outside counsel, retained subject-matter experts) for niche cases, provided the engagement covers the cost and the audit entry records the external reviewer's credentials and rationale. The honest framing: a thin roster is itself a control finding that A20 surfaces in the per-engagement risk register.

---

## Non-deterministic model behavior

Cadres run on probabilistic models. Even with fixed seeds and identical inputs, outputs vary across runs because of provider-side scheduling, batching, and infrastructure factors. The eval harness accommodates this with statistical thresholds, but reviewers and operators must understand:

- The cadre cannot guarantee bit-identical outputs across runs
- Reproducibility means same-inputs-same-conclusions, not same-inputs-same-bytes
- Some operations (e.g., regulator filings) require stronger reproducibility than the cadre can guarantee, in which case the operator must capture and preserve the exact output rather than rely on regeneration

Compensating control: deterministic substrates (citations, classifications, audit entries) are byte-stable across re-runs because they are generated by deterministic logic given the same model output. The deliverable's prose is not byte-stable.

---

## Provider dependency

CADRE is designed against the Anthropic stack (Opus orchestrator, Sonnet subagents, Haiku for narrow utility roles). Provider dependency is a deliberate architectural choice but a real limitation:

- Provider-side incidents (model outage, MCP server outage, capacity throttling) propagate to the cadre
- Provider-side policy changes (model deprecation, pricing changes, BAA terms) require operator response
- Multi-provider architectures are out of scope for v1.x; operators with multi-provider obligations carry the integration burden

Compensating controls: SP-08 (deployment runbook) covers provider-side incident response; SP-04 (MCP integration) covers provider-side policy change response. The honest framing: the cadre is a function of its provider; provider risk is operator risk.

---

## Cost predictability

Cadre cost varies with input complexity, retry behavior, and trace audit intensity. The cost-economics document (`architecture/cost-economics.md`) provides envelopes per SKU; actual costs vary. Known sources of cost variance:

- Long-context inputs (Opus 4.6's 1M context flat-rate softens but does not eliminate the effect) [VERIFIED — Opus 4.6 1M context flat-rate]
- Retry storms triggered by upstream failures
- Trace audit re-runs during incident investigation
- Eval harness expansion after incidents

Compensating controls: A14 (cost meter) is the per-engagement budget watcher; engagement-level cost ceilings are operator-set and trigger A13 escalation when approached. The honest framing: cadre cost is bounded but not flat.

---

## Process for adding limitations

When a new limitation is identified (typically through an incident, an audit finding, or operator feedback):

1. The limitation is documented in this file with the same structure as the entries above
2. A20 maintains a cross-reference to any per-engagement risk registers that depend on the limitation
3. A12's audit cycles are updated to surface the limitation in relevant traces
4. The framework changelog records the limitation in the next release notes

Removal of a limitation requires that compensating controls have been replaced by primary controls, validated by the eval harness, and reviewed at the appropriate HITL tier. Limitations are not removed because of optimism; they are removed because they are demonstrably no longer applicable.

---

## Cross-references

- `architecture/mcp-integration.md` — RFC 8707 architectural posture
- `architecture/memory-architecture.md` — k-anonymity scope
- `governance/hitl-policy.md` — reviewer roster discipline
- `governance/audit-chain-spec.md` — provenance chain underlying citation guarantees
- `governance/evidence-classification.md` — labelling discipline that surfaces these limitations
- `cadre/squad-pulse-governance/A18-pii-redactor.md` — primary consumer of redaction limitation
- `cadre/squad-pulse-governance/A20-compliance-mapper.md` — operational counterpart for limitation tracking
