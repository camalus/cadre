# Integration

*MCP servers, model providers, and external tools. The integration directory documents how CADRE connects to the world outside the cadre — what gets connected, with what trust posture, and under what compensating controls.*

---

## Layout

- `mcp-server-onboarding.md` — process for adding an MCP server to an engagement allowlist
- `mcp-server-catalog.md` — canonical catalog of vetted MCP servers and their trust tiers
- `external-tool-allowlist.md` — non-MCP external tools and their controls
- `model-provider-integration.md` — Anthropic-stack-specific configuration and operational considerations

## Reading order

If you are adding a new MCP server: start with `mcp-server-onboarding.md`. If you want to understand which servers are pre-vetted: `mcp-server-catalog.md`. If you have an external tool that does not speak MCP: `external-tool-allowlist.md`. If you are tuning the model stack: `model-provider-integration.md`.

The architectural counterpart to all of this is `architecture/mcp-integration.md`. The architecture document covers the protocol-level concerns (RFC 8707, OAuth 2.1, trust tiers as a concept). This directory covers operational concerns (which servers, which tools, how onboarded, how catalogued).

## Cross-references

- `architecture/mcp-integration.md` — protocol-level architecture
- `architecture/model-selection.md` — model assignment logic
- `governance/known-limitations.md` — RFC 8707 absent operators and other integration-level limitations
- `prompts/SP-04-mcp-integration.md` — the prompt that produces engagement-specific integration designs
