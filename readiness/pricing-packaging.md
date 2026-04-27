# Pricing and Packaging

*The pricing logic for the Readiness Diagnostic, the Sprint Quote conversion mechanics, and the SKU positioning across the BHIL CADRE engagement portfolio.*

---

## Diagnostic price band

The Readiness Diagnostic is priced at **$4,500–$7,500** depending on operator size and complexity:

| Operator profile | Price | Rationale |
|---|---|---|
| Single business unit, < 500 employees, single jurisdiction | $4,500 | Smaller surface area; fewer attendees; less prep |
| Mid-sized operator, multiple business units, single jurisdiction | $5,500 | Default mid-band |
| Multi-jurisdictional or regulated sector (healthcare, finance, hiring) | $6,500 | Compliance complexity drives Hours 3 + 6 prep |
| Enterprise with > 5,000 employees or multiple regulated sectors | $7,500 | Coordination overhead; multiple sponsors |

Pricing is determined at intake based on the pre-engagement questionnaire. There is no haggling — the price is what the price is. Operators who want a custom-priced diagnostic are in the wrong product; refer them to a Full SKU.

---

## What's included

Every diagnostic includes:

- 0.5 hour pre-day prep
- 8 hours of consultant time on the day (per `day-runbook.md`)
- The polished `.docx` diagnostic report (using the bhil-docx skill)
- The Sprint Quote PDF
- A 60-day follow-up call

Excluded:
- Travel (billed at cost if on-site is requested; default is remote)
- Multi-day variants (this is a one-day product; multi-day work is a Full SKU engagement)
- Implementation work of any kind (assessment-only)

---

## The 100% credit policy

If the operator engages BHIL on a Full or Complete SKU within **60 days** of the diagnostic delivery, the entire diagnostic fee is credited against the follow-on engagement.

The 60-day window is not negotiated. After 60 days, the operator's situation has changed enough that the diagnostic's findings are no longer current; a new diagnostic (or scoped re-diagnostic) is appropriate.

The credit is clearly stated in the Sprint Quote (`sprint-quote-template.md`) so the buyer's CFO sees it. The credit removes the diagnostic-as-deadweight objection ("we'll just engage; why pay for a diagnostic?") and creates a 60-day urgency window without manufactured pressure.

---

## SKU positioning

The diagnostic sits at the entry of a four-SKU portfolio. Every diagnostic produces a Sprint Quote at one of the SKU tiers:

| SKU | Price | Time | Diagnostic credit applies? |
|---|---|---|---|
| Express (the diagnostic itself) | $4,500–$7,500 | 1 day | n/a |
| Full | $15K–$25K | 2 weeks | Yes |
| Complete | $60K–$100K | 6 weeks | Yes |
| Enterprise | $5K–$30K/month retainer | Multi-quarter | First month credited |

The composite score from the diagnostic determines which SKU is recommended in the Sprint Quote (per `diagnostic-rubric.md`'s composite-score interpretation table). The operator can engage at a different SKU than recommended; the recommendation is BHIL's professional opinion, not a contractual requirement.

---

## Conversion mechanics

The conversion target is **~30% of diagnostics convert to a follow-on engagement within 60 days**. This is an aspirational target, not a guarantee, and is informed by:

- BHIL's prior engagements under the LOCUS and ADR Blueprint frameworks
- Industry data on consultative-sale conversion rates (typically 15–40% for well-targeted diagnostics)
- The 60-day window's structural advantage (a 90- or 180-day window dilutes urgency)

The diagnostic's value does not depend on conversion. Operators who do not convert have nonetheless paid for a useful artifact (the diagnostic report). The non-conversion outcomes split roughly:

- Operator has more foundational work to do first (Composite < 8 cases) — appropriate non-conversion
- Operator has competing priorities (budget cycle, leadership change, M&A) — re-engage when the priority returns
- Operator chose another vendor — fine; market signal

The first two cases are healthy. The third is competitive feedback worth investigating.

---

## Why not free diagnostics?

A free diagnostic would convert at higher rates but with worse buyer-quality:

- Free diagnostics attract tire-kickers
- Free diagnostics signal that the consulting itself has no value
- Free diagnostics make the diagnostic-credit mechanic incoherent (you can't credit zero against a follow-on)
- Free diagnostics push the consultant toward sales-pitch theater because the consultant isn't being paid for honesty

The $4,500–$7,500 floor is the minimum that supports rigorous, independent assessment. Consultants who can't afford to walk away from a deal won't deliver an honest diagnostic.

---

## Diagnostic vs. Sprint scope clarity

The boundary between Express (the diagnostic) and Full (the smallest Sprint) is sharp:

| Activity | Express | Full |
|---|---|---|
| Score 7 dimensions | ✓ | — |
| Recommend 2–3 priority gaps | ✓ | — |
| Produce Sprint Quote | ✓ | — |
| Build any cadre component | — | ✓ |
| Deploy any agent to production | — | ✓ |
| Run any eval suite | — | ✓ |
| Author handoff contracts | — | ✓ |
| Train operator team | — | ✓ |

The boundary protects the diagnostic's integrity. Operators who try to extract Sprint work during the diagnostic day are reframed: "That's exactly the kind of work the Sprint Quote covers — let's scope it there."

---

## The Sprint Quote itself

The Sprint Quote is delivered alongside the diagnostic report and follows the template in `sprint-quote-template.md`. Key elements:

- **Scope** — what the Sprint will and will not do
- **Milestones** — 3–5 concrete deliverables with dates
- **Price** — fixed, in the SKU's price band
- **Diagnostic credit** — the line-item credit
- **Out-of-scope items** — what would be a separate engagement
- **Validity window** — 60 days

Sprint Quotes are not modified after delivery. If the operator wants to scope differently, that's a new Quote.

---

## Citations

- BHIL ADR Blueprint — pricing-discipline benchmark.
- BHIL LOCUS Framework — diagnostic offering benchmark, github.com/camalus/BHIL-LOCUS-Framework.

---

*BHIL CADRE Framework — readiness/pricing-packaging.md — v1.0.0*
