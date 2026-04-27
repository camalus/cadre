# MCP Integration

*The CADRE Framework integrates with operator infrastructure through Model Context Protocol (MCP) servers per spec revision **2025-11-25**. This document specifies how CADRE handles authentication, scoping, async tasks, elicitation, and trust tiers.*

---

## Spec version

CADRE v1.0.0 targets MCP spec revision **2025-11-25**, which introduced:

- **OAuth 2.1** as the authentication baseline (replacing earlier ad-hoc patterns)
- **RFC 8707 resource indicators** for scoping bearer tokens to specific MCP resources
- **Async Tasks** for long-running tool calls that exceed synchronous response budgets
- **URL Mode Elicitation** for prompting users in-flow without breaking the session

CADRE will track future MCP spec revisions; spec-version drift is a maintainer concern documented under `../CHANGELOG.md`.

---

## Trust tiers

CADRE classifies MCP servers into three trust tiers, and routes tools accordingly:

### High-trust
- Operator-controlled infrastructure: the audit chain, the reviewer roster, the regulatory obligations catalog, the redaction pattern library, the engagement state machine
- Hosted on operator-owned infrastructure or on Anthropic's first-party offerings
- Authenticated with OAuth 2.1 + RFC 8707 resource indicators scoped to specific resource paths
- Tools from these servers can be in any agent's allowlist subject to the agent's role

### Medium-trust
- Vendor-provided enterprise integrations: the operator's CRM, ticketing system, document management, identity provider
- Authenticated with OAuth 2.1; RFC 8707 scoping where the vendor supports it (otherwise scoped via tenant boundaries)
- Tools from these servers are allowed only for the specific agent role that needs them; never broadly distributed

### Low-trust
- Public web sources, third-party SaaS APIs without enterprise contracts, experimental MCP servers
- May not have OAuth 2.1; if not, must be sandboxed and read-only
- Restricted to A01 Market Scout (read-only web access) and similar research-tier roles
- Outputs from low-trust servers must pass through A02 Evidence Classifier before any downstream agent treats their content as anything above UNCORROBORATED

The Nerq survey reported only 12.9% of organizations operate at the highest enterprise-trust tier for AI integrations [UNCORROBORATED]. CADRE assumes most operators start in the medium-trust tier and progress as audit infrastructure matures.

---

## OAuth 2.1 baseline

Every CADRE MCP integration uses OAuth 2.1 with these defaults:

- **Authorization Code with PKCE** for interactive flows (used during cadre setup, when a human is configuring the integration)
- **Client Credentials grant** for agent-to-server flows (used at runtime, when an agent calls a tool)
- **Refresh tokens** with bounded lifetime; expiry is a normal incident, not an exception
- **No implicit grant**, **no resource owner password credentials grant** — both removed in OAuth 2.1
- **Bearer token transmission over TLS 1.3** only

Token storage at the agent layer follows the principle that **agents do not hold tokens**. Tokens live in the operator's secrets infrastructure (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, or operator-equivalent). The MCP client SDK fetches tokens at call time and discards them after use. This means a leaked agent context window does not leak credentials.

---

## RFC 8707 resource indicators

RFC 8707 lets a single OAuth authorization server issue tokens scoped to specific MCP resources rather than broadly to "the entire MCP server." CADRE uses this to enforce agent-level least-privilege:

```
agent: A18 PII Redactor
needs: read access to redaction-patterns and jurisdiction-definitions
token resource scope:
  - mcp://operator-infra/redaction-patterns/*
  - mcp://operator-infra/jurisdiction-definitions/*
not granted:
  - mcp://operator-infra/audit-chain/*
  - mcp://operator-infra/engagement-deliverables/*
```

This means even if A18's invocation is somehow compromised (prompt injection from a poisoned input payload), the bearer token A18 holds cannot be used to read or write resources outside A18's declared scope.

Operators whose MCP servers do not support RFC 8707 should treat this as a known gap and document it in `../governance/known-limitations.md`. The mitigation is coarser-grained tenant boundaries.

---

## Async Tasks

The 2025-11-25 spec revision formalized **async Tasks**: long-running tool calls that exceed synchronous response budgets (e.g., a regulatory database query that takes 90 seconds, or a file-conversion job that takes 5 minutes). Async Tasks return a task handle immediately; the agent polls or subscribes for completion.

CADRE uses async Tasks for:

- A04 Source Archivist's bulk-fetch operations on long source lists
- A11 Eval Runner's large eval-suite executions
- A19 Audit Logger's bulk export operations (for regulator filings)
- A20 Compliance Mapper's full cross-walk runs over multi-engagement portfolios

Async Tasks have governance implications: a task that started under one policy verdict (A16) may complete after the policy has changed. CADRE's discipline is to **bind a task to its originating policy_check_id** — if the policy changes between dispatch and completion, the orchestrator re-evaluates against the new policy before consuming the task result.

---

## URL Mode Elicitation

URL Mode Elicitation lets an agent prompt the user (or the operator's reviewer) for input mid-flow without breaking the session. CADRE uses this for:

- A17 HITL Router prompting a reviewer for a routing decision when the rubric is ambiguous
- A20 Compliance Mapper requesting clarification on regulatory scope from the operator's compliance officer
- The orchestrator requesting human override of a `block` verdict (the override itself is logged through A19 with full rationale)

URL Mode Elicitation **does not bypass HITL governance**. The elicitation is logged through A19, the response from the human is subject to the same reviewer-decision discipline as any HITL response, and the elicitation is itself a Tier-2 action — the elicitation message must be A18-redacted before display to the human.

---

## Failure modes and mitigations

| Failure mode | Mitigation |
|---|---|
| Token leak via agent context window | Tokens not held by agents; fetched at call time, discarded after |
| Over-broad bearer scopes | RFC 8707 resource indicators; per-agent declared scopes |
| Policy drift during async task | Task bound to originating policy_check_id; re-evaluated on completion |
| Low-trust source contaminating downstream | A02 Evidence Classifier required before any UNCORROBORATED-or-better classification |
| URL Mode Elicitation as governance bypass | Elicitation logged through A19; subject to standard HITL discipline |
| MCP server compromise | Per-tenant boundaries; A12 Trace Auditor sample-audits tool call patterns for anomalies |

---

## Citations

- *Model Context Protocol*, specification revision 2025-11-25. [VERIFIED — primary source]
- IETF RFC 6749 (OAuth 2.0), RFC 8707 (Resource Indicators for OAuth 2.0), and the OAuth 2.1 draft. [VERIFIED]
- Nerq enterprise AI trust-tier survey, 2025. [UNCORROBORATED — single-source vendor survey, 12.9% high-trust figure]
- BHIL ADR Blueprint — depth and citation-discipline benchmark, github.com/camalus/BHIL-AI-First-Development-Toolkit.

---

*BHIL CADRE Framework — architecture/mcp-integration.md — v1.0.0*
