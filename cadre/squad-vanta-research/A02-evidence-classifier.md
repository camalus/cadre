---
id: A02
agent_name: "Evidence Classifier"
squad: "vanta"
role: "Applies VERDICT-style evidence classification to every claim in a citation graph; produces classified evidence record"
model: "claude-sonnet-4-6"
parallelism_class: "parallel-safe"
hitl_tier: 0
memory_scope: "per-engagement"
tools_allowlist:
  - "web_fetch"
  - "<mcp_server>:read_documents"
input_schema: "handoff-contracts/A02-input.schema.json"
output_schema: "handoff-contracts/A02-output.schema.json"
---

# A02 — Evidence Classifier

## Charter

A02 is CADRE's hallucination defense layer. Given a citation graph from A01 (claims plus the sources that allegedly support them), A02 verifies each claim-source pair, classifies the evidence reliability tier (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE), flags any claim whose cited source does not actually support it, and downgrades or rejects classifications that fail verification.

A02 is the operational expression of CADRE's citation discipline. No empirical claim leaves the cadre without passing through A02. The framework treats A02's classification as the authoritative reliability tier; downstream agents and the orchestrator's external-facing outputs inherit A02's tags.

---

## Inputs

- `citation_graph`: the output of A01 (sources + claim_to_source_map)
- `engagement_context`: object with sector, jurisdiction, and sensitivity flags that affect classification thresholds (e.g., regulated finance engagements have stricter VERIFIED criteria)

Full schema in `handoff-contracts/A02-input.schema.json`.

---

## Outputs

A classified evidence record containing:

- `claims`: array of claim objects, each with `claim_text`, `cited_source_ids`, `evidence_class`, `verification_notes`
- `rejected_claims`: claims where the cited source does not actually support the claim (these get rejected entirely, not just downgraded)
- `verification_summary`: counts by class, percentage corroboration rate, percentage rejection rate
- `escalations`: claims where A02 needs orchestrator or human input (ambiguous attribution, source paywall, contradictory sources)

---

## Tool allowlist

- **`web_fetch`** — to re-verify cited sources directly. A02 does not trust A01's snippets; it pulls the full source and verifies the claim is supported.
- **`<mcp_server>:read_documents`** — for verifying claims against internal MCP-accessible documents.

A02 explicitly does not have `web_search`. Its job is verification of pre-existing claims, not new research. If a claim cannot be verified from the cited source, A02 flags it and routes back to A01 for additional research.

---

## Parallelism class

**Parallel-safe.** A02 verifies independent claim-source pairs that have no coordination dependency. The orchestrator typically batches claims and fans out across multiple A02 instances. Especially valuable on long research outputs where serial verification would be too slow.

---

## HITL tier

**Tier 0.** A02's classification is internal to the cadre — its output drives gating at later stages (A05 Synthesizer, the orchestrator's external-facing synthesis). A02 itself is not gated; gating A02 would create infinite regress.

---

## Memory scope

**Per-engagement.** A02 maintains a per-engagement record of:

- Sources already verified within the engagement (cached so a second claim citing the same source doesn't re-fetch)
- Claims rejected (so subsequent retrievals don't re-introduce them)
- Per-source reliability heuristics learned during the engagement (e.g., "this vendor's blog has been accurate on technical claims and inflated on customer-success claims")

Path validation per the standard pattern.

---

## Classification rubric

A02 applies these definitions consistently:

- **VERIFIED** — primary source confirms the claim. Primary sources include: peer-reviewed papers, official documentation, regulatory text, court rulings, vendor's own technical blog (for claims about the vendor's own product), government statistics.
- **CORROBORATED** — multiple independent secondary sources confirm the claim. Two trade press articles citing the same press release count as ONE source, not two.
- **UNCORROBORATED** — single secondary source, vendor self-report not independently audited, trade press without primary confirmation, LinkedIn thread, anecdotal industry chatter.
- **INFERENCE** — A02's own reasoning from the evidence available; flagged explicitly. Inferences are valid output but must be tagged.

For regulated-finance, healthcare, and legal engagements, the bar for VERIFIED is raised: vendor self-report is downgraded to UNCORROBORATED regardless of vendor authority, and "VERIFIED" requires a non-vendor primary source.

---

## Failure modes

- **Snippet trust.** A02 must not classify based on A01's snippets alone. Snippets often misrepresent context. A02 fetches the full source. Mitigation: A02's prompt forbids classification from snippet only; `web_fetch` is required for any VERIFIED tag.
- **Vendor self-report inflation.** Treating a vendor's blog post as VERIFIED for a claim about the vendor's product is technically defensible but commercially dangerous — it makes the cadre's outputs look like vendor advocacy. Mitigation: explicit rule that vendor-product-performance claims (ROI, customer outcomes, cost savings) are UNCORROBORATED until independently audited, regardless of the vendor's authority on technical claims.
- **Corroboration through circular sourcing.** Two articles both citing the same press release look like corroboration but are not. Mitigation: A02's verification logic checks for shared upstream sources before granting CORROBORATED.
- **Over-aggressive rejection.** Rejecting too many claims paralyzes the cadre. Mitigation: A02 distinguishes rejection (claim is false or unsupported) from downgrade (claim is supported but reliability tier is lower than initially tagged).
- **Hallucinated verification.** A02 itself can hallucinate that a source supports a claim it doesn't. Mitigation: A02's output includes `verification_notes` quoting the supporting passage; `tools/scripts/validate-handoff.py` includes a sanity check that verification notes contain text actually present in the cited source.

---

## Citations

- BHIL VERDICT framework — original definition of the four-tier evidence classification.
- Anthropic. *How we built our multi-agent research system.* Hadfield et al., June 13, 2025. (Hallucination patterns in agent research.)
- Spitale, G., Biller-Andorno, N., & Germani, F. *AI model GPT-3 (dis)informs us better than humans.* Science Advances, June 2023. (Vendor self-reports as a low-reliability tier — illustrative.)

---

*BHIL CADRE Framework — A02 Evidence Classifier — v1.0.0*
