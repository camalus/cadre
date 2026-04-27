# Diagnostic Rubric

*The 7-dimension rubric for the BHIL Readiness Diagnostic. Each dimension is scored 0–4 with anchored descriptors. The composite score determines the Sprint Quote scope.*

---

## The seven dimensions

The rubric assesses readiness across the dimensions where AI agent deployments most often fail:

| # | Dimension | What it measures |
|---|---|---|
| 1 | **Use-case clarity** | Whether the operator has identified specific, scoped use cases (vs. "we should do AI") |
| 2 | **Data substrate** | Whether the data agents would consume is accessible, structured, and rights-cleared |
| 3 | **Integration readiness** | Whether MCP-compatible enterprise integrations exist or are achievable |
| 4 | **Governance posture** | HITL workflows, audit infrastructure, regulatory mapping |
| 5 | **Evaluation discipline** | Whether the operator can measure agent quality, not just availability |
| 6 | **Operational readiness** | Incident response, cost monitoring, change management |
| 7 | **Organizational readiness** | Executive sponsorship, named owners, change management capacity |

These map to the cadre's squad structure: dimensions 1, 2, 3 are intelligence/research-related (VANTA-adjacent); dimensions 1 and 5 also touch product (ATLAS); dimensions 5, 6 are operational (KEEL); dimensions 4 and 7 are governance (PULSE).

---

## Scoring scale

Each dimension is scored on a 0–4 scale:

- **0 — Absent.** No work done; no awareness; no plan.
- **1 — Nascent.** Awareness exists; no concrete work or artifacts.
- **2 — Emerging.** Some work done; gaps significant; no production-grade discipline.
- **3 — Mature.** Production-grade in scope; refinement opportunities remain.
- **4 — Exemplary.** Production-grade and refined; the operator is a positive example for peers.

Composite score is the simple sum (max 28). The composite drives Sprint Quote scope — see `pricing-packaging.md`.

---

## Dimension 1 — Use-case clarity

| Score | Descriptor |
|---|---|
| 0 | "We should do AI" with no specific use case |
| 1 | One or more general areas identified (e.g., "customer support") but no specific scoped task |
| 2 | One scoped use case with measurable success criteria; no second use case identified |
| 3 | 2–3 scoped use cases with success criteria, prioritized; rationale documented |
| 4 | Portfolio of scoped use cases; explicit "yes/no/later" decisions on candidate use cases; tied to operator strategy |

**Why this matters.** Agent deployments without specific use cases produce demos, not value. Anthropic's published research successes are on specific tasks (research, coding); the operator must be on a specific task too.

---

## Dimension 2 — Data substrate

| Score | Descriptor |
|---|---|
| 0 | Required data is unidentified or inaccessible |
| 1 | Data identified; access requires significant work; quality unknown |
| 2 | Data accessible; quality known to be uneven; cleanup needed |
| 3 | Data accessible, quality acceptable for production, IP/rights questions resolved |
| 4 | Data substrate is a competitive advantage; structured, current, rights-clean, with versioning |

**Why this matters.** The cadre needs something to consume. Operators with clean data substrates get value from agents quickly; operators without them spend the engagement on data work.

---

## Dimension 3 — Integration readiness

| Score | Descriptor |
|---|---|
| 0 | Critical systems are siloed; no API access; no plan for MCP |
| 1 | Some APIs exist; OAuth 2.1 baseline not met; no MCP servers |
| 2 | OAuth 2.1 baseline met for primary systems; MCP integration achievable but not built |
| 3 | One or more MCP servers running against operator infrastructure; trust tier classified |
| 4 | MCP integration is operator infrastructure; multiple servers, RFC 8707 scoping, async Tasks supported |

**Why this matters.** A cadre that can't talk to operator systems is decorative. Per `../architecture/mcp-integration.md`, OAuth 2.1 + RFC 8707 scoping is the integration baseline.

---

## Dimension 4 — Governance posture

| Score | Descriptor |
|---|---|
| 0 | No HITL discipline; no audit trail; no regulatory mapping |
| 1 | Awareness of governance need; no concrete artifacts |
| 2 | Some HITL workflows; ad-hoc audit logging; partial regulatory mapping |
| 3 | Tier 0–3 HITL discipline; immutable audit trail; current regulatory cross-walk |
| 4 | Governance is a competitive advantage; named compliance officer; quarterly review cadence; regulator-tested |

**Why this matters.** Per `../governance/case-law-precedents.md` (Air Canada, iTutor, Klarna), operators are held liable for agent output regardless of awareness. Governance posture determines whether deployment is defensible.

---

## Dimension 5 — Evaluation discipline

| Score | Descriptor |
|---|---|
| 0 | No evaluation; "it seemed to work" is the standard |
| 1 | Manual spot-checking; no eval suite |
| 2 | Eval suite exists; coverage uneven; no continuous integration |
| 3 | Eval suite covers all production agents; CI integration; quality bar enforced before deployment |
| 4 | Eval suite is operator infrastructure; per-agent suites; latency/cost/HITL-compliance tracked alongside quality |

**Why this matters.** The 90.2% / 15× figure from Anthropic was measured on internal evals. Without evals, the operator has no measurement of whether the agent deployment is achieving the lift. SP-07 (`prompts/SP-07-eval-harness.md`) is the framework's response.

---

## Dimension 6 — Operational readiness

| Score | Descriptor |
|---|---|
| 0 | No incident response; no cost monitoring; no change management |
| 1 | Awareness of operational needs; no concrete plays |
| 2 | Incident playbook exists; cost monitoring partial; change management ad-hoc |
| 3 | Incident playbook tested; cost meter (A14-equivalent) live; documented change management |
| 4 | Operational discipline is portable; cross-engagement playbooks; SLOs measured against |

**Why this matters.** The cadre's ongoing operation requires the operator to monitor cost (A14), run incidents (A13), and manage change. Without this discipline, the cadre runs once and falls into disrepair.

---

## Dimension 7 — Organizational readiness

| Score | Descriptor |
|---|---|
| 0 | No executive sponsor; no named owner; no change-management plan |
| 1 | Executive interest; no concrete sponsorship; no named owner |
| 2 | Sponsor identified; owner identified; change-management plan partial |
| 3 | Sponsor active; owner empowered; change-management plan executed for at least one team |
| 4 | Multiple teams successfully changed; institutional learning compounding; talent retained |

**Why this matters.** The technically-best cadre still fails without organizational adoption. The Klarna reversal is partly a story of organizational mismatch — the AI deployed without parallel organizational change. [UNCORROBORATED — public reporting of Klarna reversal varies in detail]

---

## Composite score interpretation

| Composite (max 28) | Interpretation | Recommended Sprint scope |
|---|---|---|
| 0–7 | Not ready for cadre deployment; foundational work first | Foundational — close one critical dimension before agent work |
| 8–13 | Limited readiness; scoped pilot only | Full SKU — single scoped use case, one squad |
| 14–20 | Sufficient readiness for production pilot | Full or Complete SKU |
| 21–25 | Strong readiness; portfolio deployment viable | Complete SKU |
| 26–28 | Exemplary readiness; consider Enterprise retainer | Enterprise |

---

## Honesty discipline

The diagnostic's value is its honesty. Two rules:

1. **Score the operator on what they have, not what they're planning.** A planned MCP integration scores 1, not 3, regardless of how confident the plan sounds.
2. **A diagnostic that always recommends a follow-on engagement is not a diagnostic.** Some operators score below 8 and the right recommendation is "close foundational gaps before re-assessing." This is the right call. The diagnostic's credibility — and BHIL's — depends on making it.

---

## Citations

- BHIL ADR Blueprint — readiness benchmarking pattern.
- Anthropic. *How we built our multi-agent research system.* June 13, 2025. [UNCORROBORATED]
- Public reporting of Klarna AI deployment reversal, 2025. [UNCORROBORATED — public sources vary]

---

*BHIL CADRE Framework — readiness/diagnostic-rubric.md — v1.0.0*
