# Evidence Classification

*Four-tier discipline for labelling every claim CADRE produces. The classification is not optional and not cosmetic; it is the contract between the cadre and the operator's reviewers, and it is what allows downstream consumers to calibrate their reliance on cadre output.*

---

## Why classification is mandatory

Cadres synthesize across many sources. Without explicit labels, downstream readers cannot distinguish primary evidence from inferred conclusions, and reviewers cannot apply proportional scrutiny. Mislabelled evidence is the single most common path from an honest research process to a reputational or legal incident.

CADRE adopts a four-tier classification: VERIFIED, CORROBORATED, UNCORROBORATED, INFERENCE. Every claim that appears in a cadre deliverable carries one of these labels, either inline or in a footnote. A19 (audit logger) records the label for every claim in a structured artifact; A12 (trace auditor) verifies that claim/label pairs are consistent.

---

## VERIFIED

A claim is VERIFIED when:

- It is supported by a primary source the cadre has read directly (not via summary or aggregator)
- The source is authoritative for the claim type — statute text for legal claims, regulator publications for regulatory claims, peer-reviewed publications for scientific claims, court records for case-law claims
- The cadre's reading agrees with the source on its plain meaning
- The source is canonical and stable (a permalink, an archived court record, a published statute version)

VERIFIED is the strongest label. Reviewers can rely on VERIFIED claims for downstream decisions without independent re-verification, though they remain free to do so.

Examples of VERIFIED claims that appear in CADRE governance:
- The text of EU AI Act articles (statute is a primary source)
- Court holdings cited from the published decision
- Anthropic-published model release dates from anthropic.com/news permalinks
- HIPAA Privacy Rule clause text from the Code of Federal Regulations

---

## CORROBORATED

A claim is CORROBORATED when:

- It is reported by two or more independent reputable sources
- The sources are not all derived from a single underlying announcement, dataset, or press release
- The cadre has not independently verified against a primary source, but the convergence of sources reduces the probability of error to a level reviewers can accept for non-load-bearing claims

CORROBORATED is the workhorse label for time-sensitive market intelligence. Reviewers should treat CORROBORATED claims as reliable for context-setting but should escalate to VERIFIED before relying on them for high-stakes decisions.

Examples:
- A reported acquisition price covered by multiple business journals citing different sources
- A regulatory effective date reported by two or more independent legal trackers
- A vendor's customer count reported by two independent industry analysts

When two sources both quote a single press release, that is one source for classification purposes, not two.

---

## UNCORROBORATED

A claim is UNCORROBORATED when:

- It comes from a single source, or
- All available sources trace to a single underlying announcement (typical case: vendor-published metrics)
- The claim has not been independently validated

UNCORROBORATED is the correct label for vendor-published performance metrics, single-blog-post claims, founder interviews, and any claim where the cadre cannot identify a second independent source.

Specific UNCORROBORATED claims that appear in CADRE governance and prompts:
- Anthropic's reported 90.2% eval lift and ~15× token cost figures (vendor-published; no independent replication)
- Rakuten, Decagon, Glean customer outcome figures (vendor case studies)
- Nerq's reported 12.9% improvement (single-source vendor claim)
- Most cost-per-engagement claims absent independent measurement

UNCORROBORATED is not a pejorative label. It correctly communicates the source structure. A claim being UNCORROBORATED does not mean it is wrong; it means downstream consumers must apply the appropriate caveat.

---

## INFERENCE

A claim is INFERENCE when:

- The cadre is reasoning from underlying evidence to a conclusion not directly stated in any source
- The reasoning chain is the cadre's contribution; the inputs may be VERIFIED, CORROBORATED, or UNCORROBORATED
- The claim's reliability depends on the reasoning, not on a citation

Every INFERENCE claim must declare what evidence the inference rests on and what reasoning bridges the gap. Reviewers can challenge the inference itself; the cadre cannot defend an INFERENCE by pointing at a citation, because the citation is for the inputs, not the conclusion.

Examples:
- Strategic recommendations synthesized across multiple data points
- Risk assessments combining regulatory, operational, and competitive evidence
- Persona narratives generalizing from individual data points
- Most "what this means" content in dossiers

INFERENCE is not weaker than UNCORROBORATED; it is different. UNCORROBORATED says "one source said this." INFERENCE says "no source said this directly; here is my reasoning."

---

## Vendor-published metrics rule

A specific failure mode justifies a dedicated rule: vendor performance metrics published by the vendor itself (or by partners with commercial relationships) must be labelled UNCORROBORATED unless an independent third party has replicated the measurement.

This rule applies to:
- AI model performance benchmarks self-reported by model providers
- Customer-outcome figures from vendor case studies
- Cost or efficiency claims from vendor marketing
- Win-rate or accuracy claims absent third-party audits

The rule does not apply to:
- Statements of fact about the vendor's own product (release dates, pricing pages, documented features) — these can be VERIFIED to the vendor's authoritative source
- Independent third-party benchmarks published by parties without commercial relationships

When uncertainty exists about whether a third party is independent, label conservatively (UNCORROBORATED) and let the operator decide whether to relabel after their own due diligence.

---

## Mixed claims

A single sentence can contain multiple claims at different classification levels. The classification rule is per-claim, not per-sentence. A19 records each labelled claim as a separate audit entry. A12 verifies that no UNCORROBORATED or INFERENCE claim has been silently absorbed into a VERIFIED claim's footprint.

When writing dossier prose, the standard is: every load-bearing claim has an inline classification or a footnote. Decorative claims (transitional language, summary restatements) inherit from the load-bearing claim they restate.

---

## Reviewer obligations

Operator reviewers are not required to re-verify VERIFIED claims, but they are required to:

- Verify that any VERIFIED label points to a real, accessible source
- Spot-check CORROBORATED claims by sampling
- Apply heightened scrutiny to UNCORROBORATED claims, particularly those load-bearing for decisions
- Engage critically with INFERENCE claims, including challenging the reasoning chain

A12 sample-audits the classification distribution. An anomalously high proportion of VERIFIED labels in time-sensitive market intelligence is itself a red flag and should trigger a review.

---

## Cross-references

- `cadre/squad-vanta-research/A02-evidence-classifier.md` — operational agent applying these rules
- `cadre/squad-keel-operations/A12-trace-auditor.md` — verifies classification consistency
- `cadre/squad-pulse-governance/A19-audit-logger.md` — records classified claims to the audit chain
- `governance/audit-chain-spec.md` — chain structure that holds classification metadata
- `governance/case-law-precedents.md` — example application to specific case-law claims
