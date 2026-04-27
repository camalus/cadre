# architecture/

*The technical-architecture layer of the BHIL CADRE Framework. Everything in this directory describes **how the cadre is built and how it runs** — orchestration model, MCP integration, memory, cost economics, model selection, and handoff contracts.*

---

## Layout

| File | Subject |
|---|---|
| [`orchestration-model.md`](orchestration-model.md) | The orchestrator + subagent pattern; parallel reads safe / parallel writes serialized thesis |
| [`mcp-integration.md`](mcp-integration.md) | MCP spec rev 2025-11-25: OAuth 2.1, RFC 8707 resource indicators, async Tasks, URL Mode Elicitation, trust tiers |
| [`memory-architecture.md`](memory-architecture.md) | Managed Agents Memory scopes (none / per-engagement / cross-engagement); path-validation pattern; rollback |
| [`cost-economics.md`](cost-economics.md) | Token economics; ~15× tokens for 90.2% eval lift; per-engagement cost envelopes; SKU pricing |
| [`model-selection.md`](model-selection.md) | When to use Opus 4.7, Sonnet 4.6, or Haiku 4.5 across orchestrator and subagent roles |
| [`handoff-contracts.md`](handoff-contracts.md) | JSON Schema Draft 2020-12 strict-mode handoff contracts; standard fragments |

---

## Reading order

A first-time reader should approach the architecture in this order:

1. **`orchestration-model.md`** — the central design thesis. Without this, nothing else makes sense.
2. **`memory-architecture.md`** — the path-validation rule that keeps cross-engagement memory honest.
3. **`mcp-integration.md`** — the integration substrate (this is what makes the cadre real-world rather than a toy).
4. **`model-selection.md`** and **`cost-economics.md`** — the operating economics. These two go together.
5. **`handoff-contracts.md`** — the schema discipline that holds the whole thing together.

---

## Versioning

Architecture documents are versioned with the framework as a whole (current: v1.0.0). Major architectural changes trigger a major-version bump and a CHANGELOG entry. See `../CHANGELOG.md`.

When the architecture must change in response to upstream changes (Anthropic platform updates, MCP spec revisions, regulatory changes), the changes flow through Conventional Commits with `arch:` scope and require maintainer review per `../CONTRIBUTING.md`.

---

## Citations style

Every load-bearing factual claim in this directory carries a citation. Citation classes follow `../governance/evidence-classification.md`:

- **VERIFIED** — confirmed by primary source (Anthropic documentation, MCP spec, NIST/ISO publication, official journal)
- **CORROBORATED** — confirmed by two or more independent secondary sources
- **UNCORROBORATED** — vendor-published or single-source claim; flagged as such
- **INFERENCE** — BHIL's own reasoning; clearly labeled and grounded in cited premises

The framework's credibility depends on the cadre being honest about which class each claim falls in. Vendor-published deployment metrics (e.g., Rakuten's 97% containment, 27% efficiency gain, 34% revenue lift figures) are UNCORROBORATED until independent audit. The 90.2% multi-agent eval lift figure published by Anthropic is itself UNCORROBORATED in the sense that it is vendor-reported; we cite it as such.

---

*BHIL CADRE Framework — architecture/ — v1.0.0*
