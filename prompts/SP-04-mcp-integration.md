---
id: CADRE-SP-04
title: "SP-04 — MCP Integration"
version: "1.0"
type: sub-prompt
sequence: 4
input_artifacts: ["agents/A##-*.md", "cadre-blueprint.md"]
output_artifact: "mcp-config.json"
hitl_tier: 2
---

# SP-04 — MCP Integration

*Selects the Model Context Protocol servers the cadre will use, configures OAuth 2.1 scopes, and assigns which agents can access which MCP tools. Outputs `mcp-config.json` for the engagement.*

---

## Purpose

CADRE agents reach external systems through MCP servers. The November 25, 2025 MCP specification revision (`2025-11-25`) formalized OAuth 2.1, OpenID Connect Discovery, async Tasks (call-now, fetch-later), URL Mode Elicitation for OAuth/payments, and Enterprise IdP Cross-App Access (SEP-990). MCP was donated to the Linux Foundation's Agentic AI Foundation in December 2025.

SP-04 is where the engagement chooses which MCP servers to wire in, what scopes they get, and how access is partitioned across the cadre.

---

## Inputs

- **`engagements/<id>/agents/A##-*.md`** — agent specs (each declares its tool needs)
- **`engagements/<id>/cadre-blueprint.md`** — for the sector and jurisdiction
- **`architecture/mcp-integration.md`** — the architectural pattern
- An external MCP registry — the operator provides the list of available MCP servers in the client environment

---

## Output

**`engagements/<id>/mcp-config.json`** — the canonical MCP configuration for the engagement. Schema:

```json
{
  "engagement_id": "CADRE-ENG-NNN",
  "mcp_spec_version": "2025-11-25",
  "servers": [
    {
      "server_name": "<n>",
      "server_url": "<https URL>",
      "auth": {
        "type": "oauth2.1",
        "discovery_url": "<.well-known/oauth-protected-resource>",
        "scopes_requested": ["<scope>", "<scope>"],
        "resource_indicator": "<RFC 8707 resource URI>"
      },
      "trust_tier": "<high | medium | low>",
      "agent_allowlist": ["A01", "A03", ...],
      "tool_allowlist": ["<tool name>", "<tool name>"],
      "rate_limits": {
        "requests_per_minute": <number>,
        "tokens_per_minute": <number>
      },
      "data_residency": "<US | EU | both | unspecified>",
      "audit_log_destination": "<path>"
    }
  ],
  "default_policy": {
    "deny_unlisted_servers": true,
    "deny_unlisted_tools": true,
    "require_explicit_consent_for_url_mode": true
  }
}
```

---

## Step-by-step

### Step 1 — Inventory candidate MCP servers

The operator provides a list of MCP servers available in the client environment. For each candidate, record:

- Server name and URL
- Tool inventory (what tools does it expose?)
- Authentication model (OAuth 2.1, API key, mTLS, etc.)
- Data residency (US/EU/both)
- Trust tier — based on the Nerq Q1 2026 census, only ~12.9% of public MCP servers are classified "high trust." Use the operator's internal review or established trust tiering.

### Step 2 — Map agent tool needs to MCP servers

For each in-scope agent, read its `tools_allowlist` from SP-02. Match each MCP-style tool requirement to a candidate server. If no server provides a needed tool, escalate — either find a server, build one, or remove the requirement.

### Step 3 — Determine OAuth scopes

OAuth 2.1 with RFC 8707 Resource Indicators is the floor for MCP server authentication as of `2025-11-25`. For each server, request the **minimum** scopes required for the agents that will use it. Over-broad scopes are an audit defect.

If a server uses incremental-scope consent via WWW-Authenticate (SEP-835), prefer that pattern: request the minimum at startup and request additional scopes only when agents reach for tools that need them.

### Step 4 — Apply trust-tier constraints

- **High-trust servers** (verified by Anthropic, Linux Foundation, or operator's own audit) — eligible for any agent
- **Medium-trust servers** — eligible only for parallel-safe read-only agents (VANTA, A11 Eval Runner, A12 Trace Auditor, A15 Handoff Validator)
- **Low-trust servers** — escalate to operator before inclusion; default deny

### Step 5 — Configure URL Mode Elicitation discipline

If any tool uses URL Mode Elicitation (SEP-1036, common for OAuth / payment flows), set `require_explicit_consent_for_url_mode: true`. The 2025-11-25 spec requires explicit user consent and full-URL display. The cadre's HITL Router (A17) treats URL Mode Elicitation as a Tier 2 gate by default.

### Step 6 — Configure async Tasks if used

If any agent uses async Tasks (call-now, fetch-later), document the polling pattern, the maximum task duration, and the failure handling. Async Tasks are useful for long-running MCP operations but require explicit timeout and retry logic.

### Step 7 — Set rate limits

For each server, set per-agent rate limits that respect the server's published limits and the cadre's parallelism. A VANTA squad fanning out 5 agents in parallel can DoS a poorly-rate-limited server. Conservative defaults:

- 60 requests/minute per agent for read-only servers
- 10 requests/minute per agent for mutating servers
- Lower limits for low-trust servers

### Step 8 — Write `mcp-config.json`

Validate against the schema in `templates/mcp-config-template.json`. Reference from each agent spec's `tools_allowlist` so the agent knows which MCP tools it can call.

---

## Quality criteria

- [ ] Every MCP-style tool requirement is satisfied by a configured server
- [ ] Every server uses OAuth 2.1 with explicit `discovery_url` and `resource_indicator`
- [ ] Every server has minimum scopes (no broad "read:*" or "write:*" without justification)
- [ ] Every server has a trust-tier classification
- [ ] Every server has an `agent_allowlist` (no implicit "all agents can use this")
- [ ] Every server has rate limits set
- [ ] No low-trust servers are included without operator escalation
- [ ] `default_policy.deny_unlisted_*` is set to `true`

---

## Common failure modes

- **Broad OAuth scopes for convenience.** "Just give it `read:*`" creates audit findings. Request the specific scopes the cadre actually needs.
- **No rate limits.** A 5-agent VANTA fan-out at 1000 RPM each will get the cadre rate-limited or banned.
- **Trusting public MCP servers without audit.** The 12.9% high-trust figure from the Nerq census is a real number. Most public MCP servers should be treated as low-trust.
- **Skipping URL Mode Elicitation consent.** The spec is explicit; failing to honor it is a security and compliance defect.
- **Implicit agent allowlists.** Every MCP server explicitly lists which agents can use it. No "all agents by default."

---

## Citations

- Model Context Protocol Specification, revision `2025-11-25`. Linux Foundation Agentic AI Foundation.
- IETF RFC 8707, *Resource Indicators for OAuth 2.0*.
- IETF OAuth 2.1 draft.
- Nerq Q1 2026 MCP census (17,468 servers indexed; 12.9% high-trust classification).
- Anthropic. *MCP first-anniversary post.* November 25, 2025. (>10,000 active public MCP servers.)
- MCP SEP-835 (incremental-scope consent), SEP-990 (Enterprise IdP Cross-App Access), SEP-1036 (URL Mode Elicitation), SEP PR #797 (OpenID Connect Discovery support).

---

*BHIL CADRE Framework — SP-04 — v1.0.0*
