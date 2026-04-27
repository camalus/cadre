# Regulatory Mapping

*Crosswalk between CADRE's governance controls and the legal/regulatory regimes that bind the operators we deploy for. This document does not state legal advice; it states which CADRE control surfaces map to which obligations so that operator counsel can perform conformance assessments efficiently.*

---

## Scope

CADRE is deployed by operators (the businesses paying for the cadre) into jurisdictions and sectors with overlapping AI, data protection, employment, financial services, and healthcare regulation. The cadre itself is a tool; the operator is the regulated party. CADRE's job is to make compliance demonstrable: to surface the artifacts, decisions, and audit trails that operator counsel and regulators need.

This file maps the major regimes operators encounter. It is not exhaustive; new rules and enforcement guidance appear continuously. Operators must validate the current state of any regime before relying on this map. [INFERENCE]

---

## EU AI Act (Regulation 2024/1689)

The EU AI Act is the most prescriptive horizontal AI regulation currently in force. Operators with EU users, EU data, or EU placement obligations must assess applicability. The articles most directly relevant to CADRE-style cadre deployments:

- **Article 9 — Risk management system.** High-risk AI systems require a documented, lifecycle risk management process. CADRE's eval harness (SP-07), incident pipeline (A13), and trace auditing (A12) are the substrate. Operator must own the risk management documentation.
- **Article 10 — Data and data governance.** Training and validation datasets used by high-risk systems must meet quality criteria. CADRE does not train models, but cadres that fine-tune or curate data fall under operator obligations here. The memory architecture (path-scoped writes, retention) supports demonstrable governance.
- **Article 13 — Transparency and information for users.** High-risk systems must provide instructions for use. CADRE's prompts, agent specs, and handoff contracts are the substrate; operator authors the user-facing transparency notice.
- **Article 14 — Human oversight.** High-risk systems must be designed for effective human oversight. CADRE's HITL tier model (Tier 0–3, see `governance/hitl-policy.md`) is the substrate. Operator owns reviewer staffing and the override/disagreement protocol.
- **Article 16 — Quality management.** Providers of high-risk systems must maintain a QMS. The cadre's CI/CD gates, contract validation, and changelog discipline contribute; operator's QMS is the binding artifact.
- **Article 26 — Obligations of deployers.** Deployers (operators in CADRE language) must use high-risk systems per instructions, monitor operation, and log automatically generated logs for at least six months. A19's audit chain meets the log retention substrate; operator sets retention duration per policy.
- **Article 50 — Transparency for AI interactions.** Users must be informed when interacting with an AI system. Where the cadre produces user-facing output, the operator must add the disclosure; CADRE does not generate consumer disclosures by default.
- **Article 72 — Post-market monitoring.** Providers must establish post-market monitoring. Where the operator is also the provider (because they composed the cadre into a product), the eval harness and incident pipeline are the substrate.
- **Article 79 — Procedure for AI systems posing a risk.** When a system is found to pose risks, market surveillance authorities can require corrective action. CADRE's rollback and incident-replay capabilities support compliance with such orders. [VERIFIED — text of the EU AI Act, Regulation 2024/1689; see `governance/case-law-precedents.md` for cross-references]

CADRE does not classify systems as high-risk or limited-risk; that classification is operator counsel's job under Article 6.

---

## NIST AI Risk Management Framework

NIST AI RMF 1.0 (January 2023) is voluntary in the United States but is the de facto reference framework for federal contractors and many regulated sectors. Its four functions map cleanly to CADRE substrates:

- **GOVERN.** Policies, accountability structures, organizational risk culture. CADRE's `governance/` directory and the operator's policy artifacts are the substrate. The HITL tier model and reviewer roster discipline operationalize accountability.
- **MAP.** Context, categorization, capability/limitation assessment. SP-09 (readiness diagnostic) and SP-01 (cadre design) are the substrate; the diagnostic dossier captures the MAP function output.
- **MEASURE.** Metrics, evaluation, tracking. SP-07 (eval harness), A11 (eval runner), A12 (trace auditor), A14 (cost meter) are the substrate. The eval harness is intentionally designed to produce MEASURE artifacts.
- **MANAGE.** Risk response, prioritization, communication. A13 (incident responder), A16 (policy gatekeeper), A17 (HITL router), and the rollback discipline are the substrate.

[VERIFIED — NIST AI RMF 1.0 published January 2023; framework structure publicly documented]

---

## ISO/IEC 42001 (AI Management Systems)

ISO/IEC 42001:2023 is the AI management systems standard. Operators pursuing certification must establish an AIMS aligned to ISO's PDCA structure. CADRE's contribution:

- **Plan.** Policy artifacts, risk treatment plans, objectives. The `governance/` directory plus operator policies.
- **Do.** Implementation. The cadre itself, including agent allowlists, HITL routing, and deployment runbook (SP-08).
- **Check.** Monitoring, internal audit, management review. Eval harness, trace auditor, audit chain.
- **Act.** Corrective and preventive action. Incident pipeline, rollback, schema evolution governance.

CADRE does not certify operators against ISO 42001; it provides substrates the certifier examines. [INFERENCE]

---

## Sector-specific regimes

### Healthcare — HIPAA Privacy Rule

Operators handling protected health information (PHI) must satisfy the HIPAA Privacy Rule (45 CFR Part 164). Two clauses bind cadre deployments most directly:

- **45 CFR 164.514(b) — De-identification.** The Safe Harbor method requires removal of 18 specified identifiers. A18 (PII redactor) is the substrate; the operator's privacy officer must validate that the redaction policy meets Safe Harbor or that an Expert Determination is on file.
- **45 CFR 164.530 — Administrative requirements.** Workforce training, sanctions, audit policies. A19's audit chain plus operator HR policy.

CADRE deployments touching PHI must operate under a Business Associate Agreement (BAA). Anthropic's BAA terms govern the model side; the operator owns the deployment-side BAA chain. [VERIFIED — HIPAA Privacy Rule text at 45 CFR Part 164]

### Banking — SR 11-7 (Model Risk Management)

US banking supervisors apply SR 11-7 model risk management guidance to AI systems used in regulated banking activities. The key requirement is independent model validation. CADRE's contribution:

- **Independent validation.** A12 (trace auditor) is structured for independence from the executing agents; the operator's model risk function performs the formal validation.
- **Ongoing monitoring.** Eval harness and trace audit cycles meet the substrate; operator's MRM function owns the formal monitoring program.
- **Documentation.** Agent specs, handoff contracts, eval results, and incident records are the artifacts. [VERIFIED — SR 11-7 published April 4, 2011; reaffirmed by US banking supervisors as applicable to AI/ML systems]

### Employment — NYC Local Law 144 (Automated Employment Decision Tools)

NYC LL 144 requires bias audits and candidate notice for AEDTs used in hiring or promotion within New York City. CADRE-built cadres used for AEDT functions trigger:

- **Annual bias audit.** Operator must retain an independent auditor; CADRE's eval harness can produce the data, but the audit itself is performed by an external party.
- **Candidate notice.** Operator's HR/legal team owns the disclosure; CADRE does not generate consumer notices.
- **Audit summary publication.** Operator publishes; CADRE supplies the underlying metrics. [VERIFIED — NYC Local Law 144 in effect since July 5, 2023]

### Colorado — SB24-205 (Colorado AI Act)

Colorado's SB24-205 (effective February 1, 2026) imposes duties on developers and deployers of high-risk AI systems used in consequential decisions. [CORROBORATED — multiple legal-tracking sources reported the February 1, 2026 effective date during 2025; operators should confirm any subsequent amendments before relying on dates]. CADRE substrates relevant to Colorado obligations:

- **Risk management policy.** Operator publishes; CADRE's governance documents inform.
- **Impact assessment.** SP-09 readiness diagnostic plus per-engagement assessment artifacts.
- **Consumer notice and right to appeal.** Operator-owned consumer-facing flow; cadre supplies the decision record and rationale.

### General — GDPR Article 22

GDPR Article 22 grants data subjects the right not to be subject to solely automated decisions producing legal or similarly significant effects, with limited exceptions. Where the cadre produces such decisions, the operator must:

- **Identify Article 22 trigger.** Operator's privacy counsel determines whether automated decisions meet the threshold.
- **Implement safeguards.** Human review (Tier 2 or 3 in CADRE language), explanation capability, and contest mechanism. A17 (HITL router) plus the audit chain are the substrate.

[VERIFIED — GDPR Regulation (EU) 2016/679, Article 22]

---

## What this map does not do

This map does not:

- Determine whether a specific cadre deployment falls under a specific regime; that is operator counsel's job.
- Provide legal advice; CADRE supplies substrates, not legal conclusions.
- Cover all jurisdictions; operators outside the EU/US/UK perimeter must extend the map.
- Stay current automatically; regulatory regimes evolve. A20 (compliance mapper) is responsible for keeping the operational maps fresh per engagement; this document is a starting reference.

---

## Cross-references

- `governance/hitl-policy.md` — tier model invoked by Article 14, Article 22, SR 11-7
- `governance/case-law-precedents.md` — concrete enforcement examples
- `governance/audit-chain-spec.md` — log retention substrate for Article 26, ISO 42001, NIST RMF
- `governance/evidence-classification.md` — labelling discipline applied to claims in this file
- `cadre/squad-pulse-governance/A20-compliance-mapper.md` — operational counterpart per engagement
