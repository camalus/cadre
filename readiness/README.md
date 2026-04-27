# readiness/

*The CADRE Framework's **commercial wedge**: the one-day Readiness Diagnostic. This directory specifies the diagnostic offering — its rubric, runbook, pricing, and the templates that make it executable.*

---

## What this is

The Readiness Diagnostic is a **single-day, fixed-price engagement** that produces:

1. A 7-dimension score of the operator's current AI agent readiness
2. A prioritized list of gap-closing actions
3. A scoped Sprint Quote for the follow-on Full or Complete engagement
4. A defensible, citation-backed report the operator can share with their executive sponsor

**Price band:** $4,500–$7,500 (varies by operator size and complexity)
**Time budget:** 8 hours of consultant time, structured as the day-runbook in `day-runbook.md`
**Conversion target:** ~30% of diagnostics convert to a follow-on engagement within 60 days
**Diagnostic-credit policy:** 100% of the diagnostic fee credits against a follow-on engagement closed within 60 days

---

## Why this exists

The diagnostic is the entry-point to the BHIL commercial relationship. It works because:

- **The buyer's risk is bounded.** $5K-ish, one day, walk away if unconvinced.
- **The diagnostic itself produces standalone value.** Even if no follow-on engagement closes, the buyer has a defensible readiness assessment they can use internally.
- **The 7-dimension scoring feels rigorous, not consultative.** It's a measured score against a documented rubric, not a vibe check.
- **The Sprint Quote is concrete.** The follow-on engagement is scoped, priced, and milestoned in the diagnostic deliverable itself.
- **The 100% credit removes the diagnostic-as-deadweight objection.** A buyer who plans to engage anyway pays nothing extra for the diagnostic.

The wedge is also a screening mechanism: operators who refuse to pay $5K for a diagnostic are unlikely to invest the $60K–$100K a Complete engagement requires. The diagnostic filters for engagement-quality buyers.

---

## Layout

| File | Purpose |
|---|---|
| [`diagnostic-rubric.md`](diagnostic-rubric.md) | The 7-dimension scoring rubric with anchored descriptors |
| [`day-runbook.md`](day-runbook.md) | Hour-by-hour structure of the 8-hour delivery |
| [`pricing-packaging.md`](pricing-packaging.md) | Pricing logic, SKU positioning, conversion mechanics |
| [`scoring-template.md`](scoring-template.md) | The deliverable template — what the operator receives |
| [`sprint-quote-template.md`](sprint-quote-template.md) | The follow-on engagement quote format |

---

## How this connects to the rest of the framework

- The diagnostic is operationalized as **SP-09** in `prompts/SP-09-readiness-diagnostic.md` — that's the prompt the cadre runs to produce the diagnostic.
- The diagnostic's 7 dimensions map to the four squads: VANTA dimensions assess research/intelligence readiness, ATLAS dimensions assess product readiness, KEEL dimensions assess operations readiness, PULSE dimensions assess governance readiness.
- The Sprint Quote produced by a diagnostic typically scopes a **Full** or **Complete** engagement (per `architecture/cost-economics.md`).
- Delivery uses the `bhil-docx` skill to produce a branded report; an example is in `examples/sample-engagement/`.

---

## What the diagnostic deliberately is not

- **Not a sales pitch.** The diagnostic produces real findings, including findings that contraindicate engagement (e.g., "your governance posture is too immature for agent deployment; close gaps X, Y, Z first, then re-assess"). A diagnostic that always recommends a follow-on engagement is not a diagnostic.
- **Not a build.** The diagnostic is assessment-only. No code, no agent deployment, no infrastructure changes. The boundary between diagnostic and Sprint is sharp.
- **Not a prerequisite for engagement.** Operators who already know what they need can engage the Full or Complete SKU directly. The diagnostic is for buyers who need an assessment first.

---

*BHIL CADRE Framework — readiness/ — v1.0.0*
