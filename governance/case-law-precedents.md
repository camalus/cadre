# Case Law Precedents

*Three cases that establish operator liability for AI agent output, regardless of operator awareness or vendor disclaimers. These are not hypotheticals — they are adjudicated outcomes that inform CADRE's governance architecture.*

---

## Why these cases matter

The CADRE Framework's HITL discipline, audit chain, and policy gating are not built for theoretical risks. They are built for the specific risks these cases established. An operator deploying agents without these controls is exposed to the same liability patterns these defendants discovered.

The cases span three jurisdictions and three failure modes:

- **Air Canada (Canada, 2024)** — operator liability for chatbot-stated terms that contradicted official policy
- **iTutor Group (US, 2023)** — operator liability for algorithmic discrimination in hiring
- **Klarna (multi-jurisdictional, 2025)** — operator-driven deployment reversal after AI-driven service degradation

---

## Moffatt v. Air Canada, 2024 BCCRT 149

### Facts
A passenger interacted with Air Canada's chatbot regarding bereavement fare policy. The chatbot stated a refund-after-purchase policy that contradicted Air Canada's actual published policy. The passenger booked at full fare relying on the chatbot's stated policy and later sought the refund. Air Canada denied the refund, arguing the chatbot's statement was not Air Canada's policy.

### Holding
The British Columbia Civil Resolution Tribunal held Air Canada liable for the refund. The Tribunal rejected Air Canada's argument that the chatbot was a separate legal entity or that its statements did not bind Air Canada.

### Why CADRE incorporates this
**Operators are accountable for the statements their agents make to external parties, regardless of how the agent generated those statements.**

This principle is operationalized in CADRE through:

- **A16 Policy Gatekeeper** must approve every external-facing claim against the operator's policy rulebook before release
- **A18 PII Redactor** ensures audit logs preserve what was actually said
- **A19 Audit Logger** maintains the immutable record of what the agent stated to whom, when
- **HITL Tier 2 routing** for any external-facing claim that A16 cannot definitively pass

The case also established a defensive principle CADRE incorporates: an operator cannot disclaim AI output via end-user disclaimer alone. Boilerplate "this is AI-generated" notices do not transfer liability.

### Citation
Moffatt v. Air Canada, 2024 BCCRT 149. British Columbia Civil Resolution Tribunal. [VERIFIED — primary source available via tribunal records]

---

## EEOC v. iTutor Group (settled 2023)

### Facts
iTutor Group, an online tutoring service, used an algorithmic hiring tool that filtered out women applicants over 55 and men over 60 — automatically rejecting applications based on age proxies in resumes. The Equal Employment Opportunity Commission filed suit alleging age discrimination in violation of the Age Discrimination in Employment Act.

### Settlement
iTutor Group settled for $365,000 plus injunctive relief, including changes to its hiring practices and ongoing monitoring.

### Why CADRE incorporates this
**Algorithmic systems used in employment decisions are subject to anti-discrimination law, and the operator is the liable party — not the vendor of the algorithm.**

This principle informs CADRE's:

- **Tier 3 HITL routing** for any decision affecting an individual (hiring, lending, healthcare access, housing). Two reviewers, including a compliance officer.
- **Sector-specific compliance mapping** in `regulatory-mapping.md` for hiring use cases, including NYC Local Law 144 (AEDT) bias-audit requirements
- **Evidence classification discipline** — UNCORROBORATED algorithmic outputs cannot drive Tier 3 decisions without HITL review, regardless of vendor performance claims

The case also established that the operator cannot point at the algorithm's vendor as the responsible party. iTutor was the deployer; iTutor was liable.

### Citation
EEOC v. iTutor Group, settled 2023. [VERIFIED — EEOC press release primary source; settlement terms public]

---

## Klarna AI deployment reversal (2025)

### Facts
Klarna, the buy-now-pay-later fintech, publicly announced in 2024 that AI agents had replaced approximately 700 customer service roles, with reported productivity and cost benefits. In 2025, Klarna's leadership publicly walked back the deployment, citing service quality issues and a need to re-hire human staff.

### Outcome
No litigation; the reversal was a public business decision. The case nonetheless established a strong public-record cautionary precedent about what happens when AI deployment scales ahead of the organization's capacity to govern it.

### Why CADRE incorporates this
**Deployment success requires organizational change capacity, not just technical capability.**

This principle informs CADRE's:

- **Dimension 7** in the Readiness Diagnostic — organizational readiness, not technical readiness, is the most often-overestimated dimension
- **Phased rollout discipline** in SP-08 (`prompts/SP-08-deployment-runbook.md`) — shadow → limited → full, with rollback at each stage
- **A11 Eval Runner** continuous quality monitoring — quality degradation is detectable before it becomes public
- **A14 Cost Meter** + **A13 Incident Responder** — operational discipline that prevents silent service degradation

The Klarna case also matters as a counterweight to vendor-published deployment-success metrics. Reported productivity gains are UNCORROBORATED; published reversals are likewise public business decisions whose details vary by source. CADRE incorporates both as cautionary signals — confidence in any direction (success or failure) requires more than press releases.

### Citation
Public reporting on Klarna AI deployment reversal, 2025. [UNCORROBORATED — public sources vary in detail; primary corporate communications from Klarna and reporting in Reuters, Financial Times, Bloomberg]

---

## What these cases together establish

1. **Operator liability is the default.** AI vendors do not absorb liability through end-user disclaimers, terms of service, or vendor contracts. The operator is the legally accountable party.
2. **Liability does not require operator awareness.** Air Canada did not author the chatbot's statement; iTutor did not personally code the age filter. They were liable anyway.
3. **HITL discipline is risk mitigation, not compliance theater.** The case-law trail is what makes Tier 2 and Tier 3 routing economically rational, not just regulatorily mandated.
4. **Reversals are real costs.** Klarna's reversal had real revenue, brand, and re-hiring costs. Deployment risk is not just legal — it is operational.
5. **Audit infrastructure is the defensive moat.** When an Air Canada or iTutor case happens, the operator's defense depends on what the audit chain shows. An operator with a clean audit chain showing HITL discipline and policy adherence is in a materially different position than an operator with no audit infrastructure.

---

## Why this list is not exhaustive

The case-law landscape on AI deployment is evolving rapidly. The three cases here are well-known anchor points; they are not the totality of relevant precedent. CADRE operators should:

- Engage qualified counsel for jurisdiction-specific legal review
- Monitor the **A20 Compliance Mapper**'s regulatory-change tracking
- Include legal counsel in quarterly governance reviews

The framework will incorporate additional cases as they become foundational. CHANGELOG entries track these additions.

---

## Citations (primary)

- Moffatt v. Air Canada, 2024 BCCRT 149.
- EEOC v. iTutor Group, settled 2023.
- Public reporting on Klarna AI deployment reversal, 2025.
- BHIL VERDICT framework — research-integrity discipline that informs source classification here.

---

*BHIL CADRE Framework — governance/case-law-precedents.md — v1.0.0*
