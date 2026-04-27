# Diagnostic Scoring Template

*The deliverable template. The diagnostic report the operator receives is generated against this template using the `bhil-docx` skill. This file documents the structure; the actual rendering happens in the day-of synthesis hour.*

---

## Cover page

- **Title:** [Operator Name] — AI Agent Readiness Diagnostic
- **Date:** [date of diagnostic]
- **Prepared by:** Barry Hurd, BHIL — Barry Hurd Intelligence Lab
- **Version:** 1.0 (BHIL CADRE Framework v1.0.0)
- **Confidentiality:** [per engagement contract]

The cover uses BHIL's dark-navy cover palette per the bhil-docx skill (cover background `#1C1C2E`, accent `#1B4FD8`).

---

## Executive summary (1 page)

A single page summarizing:

- **Composite score** (0–28)
- **Score breakdown** (mini bar chart of the 7 dimensions)
- **Headline finding** (1–2 sentence assessment of overall readiness)
- **Top 3 gap-closing actions** (numbered, concrete)
- **Recommended Sprint scope** (Foundational / Full / Complete / Enterprise / Re-assess in 6 months)

The executive summary is what the sponsor will read and circulate. It is written for that audience: short, declarative, and decision-ready.

---

## Scope and method (0.5 page)

- What was assessed (dimensions, attendees, hours)
- What was not assessed (boundary clarity)
- Methodology reference (this rubric, this runbook)
- Caveats (what the consultant could not verify in one day)

Honesty about scope limits is part of the deliverable's credibility. A diagnostic that pretends to assess things it didn't actually assess is worse than one that names the limits.

---

## Per-dimension findings (7 sections, 1 page each)

For each of the 7 dimensions:

### Dimension N — [Dimension Name]

- **Score:** [0–4]
- **Anchor descriptor matched:** [the rubric anchor that best fits]
- **Evidence observed:** structured list of what the consultant saw (artifacts reviewed, statements heard, examples given). Each evidence item carries an evidence_class per `../governance/evidence-classification.md`.
- **Strengths:** what is working
- **Gaps:** what is not working
- **Recommended action(s):** 1–2 concrete actions, sized to be discussable

The per-dimension sections are the deliverable's substance. They take the time they take to write — typically 20–30 minutes per dimension during Hour 7 synthesis.

---

## Prioritized recommendations (1 page)

The 2–3 highest-impact gap-closing actions, with:

- **Action:** what to do
- **Rationale:** why this and not other actions
- **Approximate effort:** small / medium / large in operator-team time
- **Approximate calendar:** weeks to months
- **Dependency on Sprint engagement:** can the operator do this themselves, or does it benefit from BHIL's involvement?

Actions are not all consultant-led. Some are operator-internal work. The prioritization is independent of BHIL revenue interest.

---

## Sprint Quote (separate document)

The Sprint Quote is a separate deliverable per `sprint-quote-template.md`. The diagnostic report references it but does not embed it; this is so the Sprint Quote can stand alone if the operator's procurement workflow needs it separately.

---

## Appendix A — Evidence inventory

A table of every evidence item the consultant relied on:

| Item | Source (artifact / statement / observation) | Evidence class | Used in dimension |
|---|---|---|---|
| ... | ... | VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE | ... |

This appendix is what makes the diagnostic defensible. If the operator (or their auditor, or their board) wants to interrogate any score, the evidence trail is here.

---

## Appendix B — Pre-engagement questionnaire response

The operator's pre-engagement intake responses, included verbatim. This appendix is light but important — it shows the consultant what the operator said before the day, which sometimes contradicts what the operator says during the day. The contradiction itself is informative.

---

## Appendix C — Glossary

Brief glossary of terms used in the report:
- HITL tiers (0/1/2/3)
- Evidence classes (VERIFIED / CORROBORATED / UNCORROBORATED / INFERENCE)
- Squad names (VANTA, ATLAS, KEEL, PULSE)
- SKU tiers (Express, Full, Complete, Enterprise)
- Cynefin framework

The glossary is for operators whose reviewers are not BHIL-conversant. A board-level reader should be able to read the diagnostic without prior cadre knowledge.

---

## Branding application

The deliverable uses the bhil-docx skill with:

- Cover: dark navy `#1C1C2E` background; cobalt `#1B4FD8` accents; white type
- Body: standard professional layout; section headers in cobalt
- Footer: "BHIL — Barry Hurd Intelligence Lab — Confidential" on every page
- Logo placement per the bhil-docx skill defaults

The branding is consistent with BHIL's other CADRE / LOCUS / ADR Blueprint deliverables. Operators who engage across multiple BHIL frameworks see a coherent identity, not a different aesthetic per engagement.

---

## What the template deliberately omits

- **No client logos** on the report unless the operator specifically requests co-branding (uncommon; usually a poor idea for an independent assessment).
- **No revenue projections.** The diagnostic is assessment, not forecasting.
- **No vendor recommendations** (e.g., "use vendor X for your CRM"). Out of scope.
- **No personnel assessments.** Dimension 7 is about organizational readiness, not individual capability assessment.
- **No competitive comparisons** ("you're behind your peers"). Such comparisons require evidence the diagnostic does not gather; absent that evidence, they are speculation.

---

## Citations

- BHIL bhil-docx skill — branding application.
- BHIL ADR Blueprint — deliverable-discipline benchmark.
- BHIL LOCUS Framework — readiness deliverable benchmark.

---

*BHIL CADRE Framework — readiness/scoring-template.md — v1.0.0*
