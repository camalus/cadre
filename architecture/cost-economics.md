# Cost Economics

*Token economics, per-engagement cost envelopes, and the SKU pricing model. The CADRE Framework's commercial defensibility depends on knowing — within a tight band — what an engagement will cost to run, and pricing the engagement above that cost with margin.*

---

## The 15× factor

Anthropic's published multi-agent research finding: the orchestrator + subagent pattern delivers approximately a **90.2% improvement** over single-agent baselines on internal evaluations, at approximately **15× the token cost**. [UNCORROBORATED — vendor-published]

This number is the central operating assumption of CADRE's cost model. Every per-engagement budget envelope is computed as 15× the equivalent single-agent cost, then multiplied by an engagement-specific complexity factor.

The factor is approximate. Real engagements range from roughly 8× (research-heavy with high deduplication across subagents) to 25× (governance-heavy with many serialized PULSE invocations). The cost meter (A14) tracks actual token consumption against the engagement's envelope; envelope breaches trigger an incident, not silent overruns.

---

## Per-engagement envelopes by SKU

CADRE engagements are sold in four SKU tiers. The envelopes are denominated in token-equivalents and dollar-equivalents at Opus 4.6 / Sonnet 4.6 list pricing as of April 2026.

### Express ($4,500 — one-day diagnostic)
- **Time budget:** 8 hours (one operator day)
- **Token envelope:** ~5M total (mostly Opus orchestrator + 2–3 Sonnet subagents)
- **Inference cost:** ~$200–$400 at list pricing
- **Deliverables:** readiness diagnostic per `../readiness/diagnostic-rubric.md`, 7-dimension score, prioritized recommendations, sprint quote
- **Margin profile:** high — the engagement is mostly knowledge-work value, infrastructure cost is small

### Full ($15,000–$25,000 — two-week scoped engagement)
- **Time budget:** 60–80 hours operator time over two weeks
- **Token envelope:** ~30M total
- **Inference cost:** ~$1,500–$2,500 at list pricing
- **Deliverables:** scoped cadre deployment for one specific use case (research, product, or one operations workflow), trained operator team, handoff documentation
- **Margin profile:** strong — 6–10% inference cost relative to engagement price

### Complete ($60,000–$100,000 — six-week portfolio engagement)
- **Time budget:** 240+ hours operator time over six weeks
- **Token envelope:** ~150M total
- **Inference cost:** ~$8,000–$15,000 at list pricing
- **Deliverables:** full multi-squad cadre deployment, governance integration with operator's compliance function, eval harness wired up, phased rollout completed
- **Margin profile:** moderate — 10–15% inference cost; complexity drives operator time

### Enterprise (custom — multi-quarter engagement, $5K–$30K/month retainer)
- **Time budget:** custom; typically 2–3 named consultants part-time
- **Token envelope:** rolling; A14 Cost Meter sets monthly cap
- **Inference cost:** budgeted as separate line item (operator pays direct)
- **Deliverables:** ongoing cadre operation, monthly compliance reporting, quarterly architecture review, regulatory-change tracking
- **Margin profile:** retainer-style; predictable revenue

---

## The commercial wedge

The Express SKU is the **commercial wedge** — a one-day diagnostic priced at $4,500–$7,500 that produces a defensible readiness assessment and a sprint quote. Conversion target: ~30% of diagnostics convert to a Full or Complete engagement within 60 days. The sprint quote applies a 100% credit of the diagnostic fee against the follow-on engagement, removing the diagnostic-as-deadweight objection.

Why the wedge works:
- The buyer's risk is bounded ($5K-ish, one day, walk away if unconvinced)
- The diagnostic itself produces value even if no follow-on engagement closes (the buyer learns where they stand)
- The 7-dimension scoring makes the diagnostic feel rigorous, not consultative
- The sprint quote is concrete: scoped, priced, with named milestones

See `../readiness/pricing-packaging.md` for the diagnostic offering's full mechanics.

---

## Token economics by squad

A typical Complete-tier engagement's token consumption breakdown:

| Squad | Share | Notes |
|---|---|---|
| Orchestrator (Opus) | 15–25% | Long context; sees all subagent outputs |
| VANTA (Sonnet) | 35–50% | Heaviest fan-out; research-heavy |
| ATLAS (Sonnet) | 20–30% | Substantial but more bounded than VANTA |
| KEEL (mixed Sonnet/Haiku) | 5–10% | Eval runs are bursty; mostly Sonnet |
| PULSE (Sonnet + Haiku) | 5–10% | A19 on Haiku keeps audit logging cheap |

The Opus share grows in long engagements because the orchestrator's context accumulates. The PULSE share grows in highly-regulated engagements because every external action gates through A16 and routes through A17. The VANTA share grows in research-heavy engagements (BHIL's MERIDIAN-anchored work).

---

## Cost-meter discipline (A14)

A14 Cost Meter monitors token spend in real time and enforces three rules:

1. **Hard envelope** — engagement cannot exceed its SKU envelope without explicit operator approval logged through A19. Default is fail-closed: at envelope, A14 emits a `block` request to the orchestrator.
2. **Soft envelope warnings** — at 50%, 75%, 90% of envelope, A14 emits notifications to the engagement owner.
3. **Per-agent budget allocation** — within the engagement, each squad has a sub-envelope. Squad-level overruns trigger investigation (is VANTA fanning out too aggressively? Is PULSE gating too many actions?) before the engagement-level envelope is at risk.

A14's hard envelope is the operator's protection against runaway costs from prompt-injection or recursive subagent dispatch (a known multi-agent failure mode).

---

## The Opus 4.6 1M-context flat rate

Opus 4.6 at $5/$25 per M input/output tokens, with a 1M-context flat-rate option, materially changes the economics of long engagements. [VERIFIED — Anthropic announcement March 13, 2026]

Without flat-rate, a long-running orchestrator in a Complete engagement could accumulate substantial input-token costs as it re-reads accumulated state. With flat-rate at the 1M-context tier, the orchestrator's input cost is capped, making longer-running engagements economically tractable.

CADRE's default is to enable flat-rate for the orchestrator on Complete and Enterprise engagements, and to use standard pricing on Express and Full.

---

## Citations

- Anthropic. *How we built our multi-agent research system.* June 13, 2025. [UNCORROBORATED — 15× / 90.2% figures are vendor-published]
- Anthropic. *Claude Opus 4.6 release announcement.* March 13, 2026. [VERIFIED — pricing, 1M-context flat rate]
- Anthropic. *Claude Opus 4.7 release.* April 16, 2026. [VERIFIED]
- Anthropic. *Claude Haiku 4.5 model card and pricing.* [VERIFIED]
- BHIL ADR Blueprint — economic-discipline benchmark.

---

*BHIL CADRE Framework — architecture/cost-economics.md — v1.0.0*
