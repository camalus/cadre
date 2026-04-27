# Sprint Quote Template

*The follow-on engagement quote. Delivered alongside the diagnostic report. The Sprint Quote is short (typically 3–4 pages), concrete, and signed-or-walked-away from within 60 days.*

---

## Cover

- **Title:** [Operator Name] — Sprint Quote
- **Date issued:** [date]
- **Validity:** 60 days from date issued
- **Prepared by:** Barry Hurd, BHIL — Barry Hurd Intelligence Lab
- **Reference:** Diagnostic delivered [diagnostic date]

---

## Engagement summary (0.5 page)

Three short paragraphs:

1. **Context** — one paragraph reminding the operator of the diagnostic findings and why this Sprint scope is the recommended response
2. **Objective** — one paragraph stating what this Sprint will accomplish
3. **Outcome** — one paragraph stating what the operator will have at the end of the Sprint that they don't have now

This summary is written so the operator's CFO can read it and understand the deal in 60 seconds.

---

## Scope (1 page)

A clearly bounded scope statement:

### What this Sprint will do
- Specific deliverable 1
- Specific deliverable 2
- Specific deliverable 3

Each deliverable references the relevant CADRE framework component (e.g., "Deploy a single-squad VANTA cadre per `cadre/squad-vanta-research/README.md`"). The Sprint scope is grounded in framework structure, not invented.

### What this Sprint explicitly does not include
- Out-of-scope item 1
- Out-of-scope item 2
- Out-of-scope item 3

The exclusions list is at least as important as the inclusions. Operators sometimes assume work is included that isn't; the exclusions list pre-empts the assumption.

---

## Milestones (0.5 page)

3–5 concrete milestones, each with:

| # | Milestone | Date | Deliverable |
|---|---|---|---|
| 1 | Engagement kickoff | Day 1 | Charter, working folder, kick-off meeting summary |
| 2 | [Substantive milestone] | Day [N] | [Specific artifact] |
| 3 | [Substantive milestone] | Day [N] | [Specific artifact] |
| 4 | Engagement close | Day [N] | Final report, transition documentation |

Milestones are dated in calendar days from engagement start. A two-week Sprint has tight milestones; a six-week Sprint has more breathing room.

---

## Pricing (0.5 page)

| Item | Amount |
|---|---|
| [SKU tier] engagement | $[total] |
| Diagnostic credit (per `pricing-packaging.md`) | -$[diagnostic fee] |
| **Net engagement fee** | **$[net]** |
| Travel (if any, billed at cost) | $[estimate or "remote, none"] |

Pricing is fixed for the engagement scope as defined. Out-of-scope work is a separate engagement at the prevailing rate.

Payment terms are stated clearly: typically 50% on engagement start, 50% on engagement close. Variations are possible for enterprise procurement workflows but require documentation.

---

## Acceptance and signature (0.25 page)

- **Operator:** [Name, Title, Signature, Date]
- **BHIL:** Barry Hurd, Founder — [Signature, Date]

A signed Sprint Quote is the engagement contract. Engagement commences on the start date specified above.

---

## Out-of-scope follow-on opportunities (0.5 page)

A short list of follow-on work the diagnostic surfaced that the Sprint will not address. These are not commitments — they are visibility for the operator into work the operator may want later.

- **Follow-on opportunity 1.** What it is, why it matters, approximate scope.
- **Follow-on opportunity 2.** Same.
- **Follow-on opportunity 3.** Same.

Surfacing these is honest planning. Operators appreciate seeing the path beyond the current Sprint, even if they're not committing to it now.

---

## Standard terms

- **Confidentiality:** mutual, per BHIL standard MNDA terms (separate document)
- **IP:** operator owns all engagement-specific outputs; BHIL retains framework IP
- **Data handling:** per `../architecture/memory-architecture.md` — operator data remains in `engagements/<id>/`, never propagated to cross-engagement memory without explicit operator approval through the promote-learnings workflow
- **Liability:** standard professional services limitation, capped at engagement fee
- **Subcontractors:** none unless disclosed and approved
- **Termination:** either party may terminate with 5 business days notice; pro-rata fees apply

---

## What the template deliberately omits

- **No vague scope.** "We'll help you with AI" is not a Sprint Quote.
- **No open-ended timelines.** Every milestone has a date.
- **No success-fee variants.** BHIL's compensation is for the engagement, not for downstream operator outcomes BHIL doesn't control.
- **No equity components.** Sprint engagements are cash. Equity arrangements, if ever appropriate, are separate transactions.
- **No revenue projections** about what the cadre will produce for the operator. The cadre's value is operator-realized; BHIL's job is the deployment.

---

## Sample milestones by SKU

### Full SKU (2 weeks)
1. Day 1 — Kickoff
2. Day 5 — Cadre design (SP-01) + agent roster (SP-02)
3. Day 9 — Handoff contracts (SP-03) + MCP integration (SP-04)
4. Day 12 — Eval harness (SP-07) + shadow deployment
5. Day 14 — Engagement close, transition to operator team

### Complete SKU (6 weeks)
1. Week 1 — Kickoff + cadre design
2. Week 2 — Agent roster + handoff contracts
3. Week 3 — MCP integration + memory setup
4. Week 4 — HITL governance configuration + eval harness
5. Week 5 — Phased rollout (shadow → limited)
6. Week 6 — Full rollout + engagement close

These are starting templates. Actual milestones are tailored to the operator's situation during Sprint Quote drafting.

---

## Citations

- BHIL ADR Blueprint — engagement-discipline benchmark.
- BHIL LOCUS Framework — Sprint Quote benchmark.

---

*BHIL CADRE Framework — readiness/sprint-quote-template.md — v1.0.0*
