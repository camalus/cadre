# Model Selection

*When to use Opus 4.7, Opus 4.6, Sonnet 4.6, or Haiku 4.5 across orchestrator and subagent roles. Model selection is the most-tweaked operating parameter in CADRE; this document defines the defaults and the rationale.*

---

## Defaults at a glance

| Role | Default model | Rationale |
|---|---|---|
| Orchestrator | Opus 4.7 (or 4.6 for cost-sensitive engagements) | Long-context reasoning, complex multi-step planning, reconciliation |
| VANTA subagents | Sonnet 4.6 | Strong on research and synthesis; cost-effective at fan-out volumes |
| ATLAS subagents | Sonnet 4.6 | Strong on structured product authoring; cost-effective |
| KEEL subagents | Sonnet 4.6, except A14 Cost Meter on Haiku 4.5 | Sonnet for judgment-required ops; Haiku for routine metering |
| PULSE subagents | Sonnet 4.6, except A19 Audit Logger on Haiku 4.5 | Sonnet for governance judgment; Haiku for mechanical logging |

---

## Why Opus 4.7 for the orchestrator

The orchestrator's job — parsing engagement briefs, classifying parallelism, reconciling subagent outputs, enforcing policy boundaries — is the cadre's hardest reasoning task. It sees the most context, makes the most consequential decisions, and is the agent whose failure cascades hardest.

Opus 4.7 (released April 16, 2026) is the most capable model in Anthropic's lineup as of CADRE v1.0.0's release date. Its incremental gain over Opus 4.6 on multi-step orchestration tasks is documented in Anthropic's release notes and is sufficient justification for the price differential on Complete and Enterprise engagements.

For Express and Full engagements where cost discipline is tighter, Opus 4.6 is acceptable. The eval harness (A11) verifies that orchestrator behavior on the engagement's specific task profile meets quality bar regardless of model choice; that is the safeguard that lets us flex between 4.6 and 4.7.

---

## Why Sonnet 4.6 for most subagents

Sonnet 4.6 is the cost/capability sweet spot for substantive subagent work. It's strong enough to:

- Conduct iterative research (A01, A02)
- Author structured PRDs and specs (A06, A07)
- Run eval suites and interpret results (A11)
- Apply policy rulebooks with nuance (A16, A17)
- Produce compliance cross-walks (A20)

...and it's cheap enough to use under fan-out without breaking the engagement budget. The 90.2% / 15× figure from Anthropic's research is computed against Sonnet subagents; that's the evidence base.

Putting subagents on Opus would inflate the 15× figure significantly — closer to 30–40× by rough estimate — which makes the economics untenable for most engagements. Putting subagents on Haiku would underperform on research and synthesis quality. Sonnet is the answer.

---

## Why Haiku 4.5 for A14 and A19

Two CADRE agents do mechanical work where Sonnet capability is wasted:

### A14 Cost Meter
A14's job is metering: reading token consumption from the API, comparing to budget, emitting notifications and blocks. There is no judgment call here — the math is the math. Haiku 4.5 is fast (sub-second response on most invocations), cheap, and sufficient.

### A19 Audit Logger
A19's job is appending entries to the audit chain: validate schema, compute chain hash, append, return ID. Same shape as A14 — mechanical, no judgment. Haiku is the right choice.

Putting A14 or A19 on Sonnet would be premium pricing for routine work. The savings compound: on a Complete engagement, A14 fires hundreds of times and A19 fires thousands of times. Haiku here is a meaningful cost difference without quality cost.

---

## When to upgrade an agent to Opus

Three patterns warrant upgrading a specific agent from Sonnet to Opus:

1. **Persistent eval failures.** A11 reports that an agent's quality bar is not being met even after prompt iteration. Upgrade is one of the last levers; first investigate input quality, prompt quality, and tool allowlist. If those are correct and the agent still misses, model upgrade is justified.
2. **Engagement complexity exceeding Sonnet's reasoning depth.** Some engagements (highly regulated, multi-jurisdictional, or operating against unusually complex source material) push subagent reasoning past Sonnet's capability. The eval harness shows this as systematic miss patterns, not random variation. Upgrade A02 Evidence Classifier or A05 Synthesizer in these cases.
3. **HITL load reduction.** When an agent is consistently producing Tier-2 outputs that need human review, upgrading to Opus may reduce the review load by improving quality. The math has to pencil: Opus cost per invocation × invocation count vs. reviewer time saved × reviewer hourly rate.

Every upgrade is a CHANGELOG-tracked decision and is logged through A19 as a `configuration_change` event.

---

## When to downgrade an agent to Haiku

The mirror pattern: when an agent's work is mechanical or extremely well-bounded, Haiku may be sufficient. Candidates include:

- **A04 Source Archivist** — if archiving is purely mechanical (write to S3, write metadata, return reference), Haiku may be adequate. Test before defaulting.
- **A15 Handoff Validator** — schema validation is mechanical; Haiku may handle it.

Downgrade decisions are also CHANGELOG-tracked. Both directions of model change need eval-harness evidence, not intuition.

---

## Model deprecation discipline

Anthropic deprecates models periodically. CADRE's discipline:

- **Track release dates.** The README and CHANGELOG document the model versions used.
- **Plan for deprecation.** When Anthropic announces deprecation, A20 Compliance Mapper surfaces it as a regulatory-class event (because some compliance regimes care about the underlying model).
- **Version-pin in production.** Engagement contracts pin models. Mid-engagement model swaps are not allowed without explicit re-contracting.
- **Use the eval harness for migration.** When upgrading from Sonnet 4.6 to Sonnet 4.7 (when released), the eval harness verifies behavior equivalence on the engagement's task profile before cutover.

---

## A note on Opus 4.6 1M-context flat-rate

Opus 4.6 introduced a 1M-context flat-rate option (announced March 13, 2026). [VERIFIED] For long-running orchestrators, this can be the difference between economic and uneconomic. CADRE's default is to enable flat-rate for the orchestrator on Complete and Enterprise engagements; see `cost-economics.md` for the full rationale.

Opus 4.7 inherits this option per Anthropic's April 2026 release notes. [VERIFIED]

---

## Citations

- Anthropic. *Claude Opus 4.7 release.* April 16, 2026. [VERIFIED]
- Anthropic. *Claude Opus 4.6 release announcement.* March 13, 2026. [VERIFIED — including 1M-context flat-rate]
- Anthropic. *Claude Sonnet 4.6 model card.* [VERIFIED]
- Anthropic. *Claude Haiku 4.5 model card and pricing.* [VERIFIED]
- Anthropic. *How we built our multi-agent research system.* June 13, 2025. [UNCORROBORATED — 90.2% / 15× figures vendor-published]

---

*BHIL CADRE Framework — architecture/model-selection.md — v1.0.0*
