# Model Provider Integration

*The Anthropic-stack-specific operational considerations: which model variants the cadre uses, how releases are tracked, how provider-side features (Managed Agents Memory, prompt caching, batching) are evaluated, and how provider-side incidents are handled.*

---

## Stack baseline

CADRE v1.0 targets the Anthropic stack with:

- **Orchestrator:** Claude Opus 4.7 (released April 16, 2026) [VERIFIED — Anthropic release announcement, April 16, 2026]
- **Subagents (default):** Claude Sonnet 4.6
- **Utility roles (A14 Cost Meter, A19 Audit Logger):** Claude Haiku 4.5

Model assignment per agent is recorded in each agent's YAML frontmatter (`model:` field) and is reviewed at framework release time. Per-engagement assignment may downgrade or upgrade specific roles per the engagement charter; the framework defaults are the starting point.

For the architectural rationale, see `architecture/model-selection.md`. This document covers operational integration concerns.

---

## Release tracking

Anthropic publishes model releases through anthropic.com/news. The cadre's release tracking is:

- **Major version releases (e.g., 4.6 → 4.7).** The framework maintainer evaluates the release within a documented window (default: 30 days). Evaluation includes eval-suite execution against the new variant, cost-behavior comparison, capability comparison. The evaluation produces a recommendation: adopt, defer, or skip. Adoption updates the framework defaults through standard change discipline.
- **Patch releases.** Adopted in routine operations; no formal evaluation required unless an incident or evaluation gap surfaces.
- **Deprecations and sunsets.** Anthropic-announced deprecations are tracked; affected agent assignments are migrated within the announced window. Engagements running on deprecated variants are migrated proactively rather than waiting for sunset.

The release-tracking artifact lives at `tools/scripts/track_releases.md` (a checklist) and references for prior releases live in this document's update history.

---

## Opus 4.6 and 4.7 specifics

Opus 4.6 went GA on March 13, 2026, with $5/$25 per million tokens pricing and a 1M-token context flat rate. Opus 4.7 was released April 16, 2026, as the most advanced variant currently available. [VERIFIED — Anthropic public release announcements]

Operational considerations:

- **1M context flat rate (Opus 4.6).** The flat rate makes long-context orchestration cost-predictable; A14 (cost meter) tracks usage against the flat-rate threshold and flags spend that suggests context-budget exhaustion. The cadre's orchestration design is tuned to stay within the flat-rate envelope. [VERIFIED — Opus 4.6 1M context flat-rate pricing]
- **Opus 4.7 capabilities (April 16, 2026).** Currently the most advanced model variant. The framework's default is Opus 4.7 for orchestration; specific engagements may pin to 4.6 if their evals surface 4.6-specific advantages or if cost ceilings require it.
- **Subagent variant choice.** Sonnet 4.6 is the default subagent. Specific agents may upgrade to Opus for engagements where the agent's role benefits from frontier capability (typically synthesis-heavy or judgment-heavy roles); the upgrade is recorded in the engagement charter.

---

## Managed Agents Memory (beta)

Anthropic released the Managed Agents Memory feature into public beta on April 23, 2026. The feature offers provider-managed memory persistence with the model's native context-management.

CADRE v1.0 does not enable Managed Agents Memory by default. Reasons:

- The cadre's three-scope memory architecture (none / per-engagement / cross-engagement) is the principal control surface. Provider-side memory adds a parallel surface that requires policy controls of its own.
- The promote-learnings workflow is the cadre's governance for cross-engagement persistence. Provider-side memory bypasses that workflow unless explicit policy is established.
- Beta features may change. The framework adopts beta features after stability and policy posture are clear.

Operators who wish to opt into Managed Agents Memory must:

- Document the use case and the policy posture in the engagement charter
- Treat provider-side memory writes as side-effect-producing actions for HITL purposes
- Extend the audit emission requirements to cover provider-side memory operations
- Accept that provider-side memory is outside the cadre's path validator and rollback capabilities; compensating controls are required

The framework will revisit Managed Agents Memory in a future minor release after public-beta maturation.

[VERIFIED — Anthropic public beta announcement, April 23, 2026]

---

## Prompt caching

Prompt caching reduces cost and latency for repeated long-context calls. CADRE benefits from prompt caching where:

- The orchestrator's master prompt is reused across many subagent invocations
- Stable agent specs are referenced repeatedly in context
- Reference materials (regulatory text, policy documents, schema definitions) are reused across multiple deliverables

Operational considerations:

- A14 records cache-hit ratios as a cost-behavior metric
- Cache invalidation occurs on prompt edits; the cadre's edit cadence (changes through framework change discipline) is compatible with caching
- Per-engagement custom prompts are cacheable as long as they are stable across the engagement's deliverables

The cadre does not require prompt caching for correct operation; caching is a cost optimization, not a control surface.

---

## Batching

Anthropic's batch API offers reduced cost for non-time-sensitive bulk operations. CADRE uses batching for:

- Eval-suite execution (A11)
- Trace audit re-runs (A12)
- Bulk source-archiving (A04)
- Other non-real-time orchestration

Real-time orchestration (the principal cadre flow) does not use batching. The framework's eval and audit substrates are designed to work with batched and synchronous calls interchangeably.

A14 records batch-vs-synchronous cost ratios. When batched paths consume disproportionate cost, the path is reviewed.

---

## Provider-side incidents

Provider-side incidents (model outages, capacity throttling, latency spikes, MCP server outages from Anthropic-operated MCP infrastructure) propagate to the cadre. Response:

- A13 (incident responder) treats provider-side incidents as Sev-2 by default; severity may be raised based on engagement impact
- The deployment runbook (SP-08) covers fallback behavior: synchronous calls degrade to batched where possible; in-flight work is preserved or explicitly aborted; user-facing degradation is communicated via operator's standard channels
- Audit emissions continue normally during provider incidents; chain integrity is preserved
- Post-incident, the cadre recovers without operator intervention beyond resuming paused engagements

For multi-day provider incidents, the operator's continuity plan governs; the cadre is one capability in that plan, not the plan itself.

---

## API key management

Anthropic API keys are managed by the operator's secrets-management infrastructure. The cadre never embeds keys in artifacts, contracts, or memory. Specifically:

- API keys are referenced by name, not value, in engagement allowlists
- Keys are injected at runtime by the operator's infrastructure
- Key rotation is operator-side; the cadre is unaffected by key rotation as long as the new key has the same authorization scope
- Key compromise triggers operator-side incident response; the cadre's chain provides forensic substrate for scope-of-exposure analysis

The framework does not specify a particular secrets manager; operators use what their platform standardizes on.

---

## Rate limits and quotas

Anthropic-side rate limits and quotas constrain cadre throughput. Cadre design accommodates:

- A14 records per-minute and per-day usage against operator-known quotas
- Approaching limits triggers operator-side capacity decisions (request quota increase, reduce parallelism, defer non-urgent work)
- Hard rate-limit responses are handled with exponential backoff; persistent rate-limit hits trigger A13 evaluation of whether the cadre is correctly sized

Operators on enterprise capacity arrangements (custom quotas, dedicated capacity) report effective limits to the cadre's cost-meter configuration; defaults assume standard public quotas.

---

## Cross-references

- `architecture/model-selection.md` — model assignment rationale
- `architecture/cost-economics.md` — cost-behavior framework
- `cadre/squad-keel-operations/A14-cost-meter.md` — cost tracking implementation
- `prompts/SP-08-deployment-runbook.md` — provider-incident response
- `governance/known-limitations.md` — provider-dependency residual risk
