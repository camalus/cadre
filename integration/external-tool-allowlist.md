# External Tool Allowlist

*Non-MCP external tools and the controls that govern their use. Some operator stacks include tools that do not (yet) speak MCP. CADRE accommodates these but with deliberate friction so that they do not become a back-channel around MCP's controls.*

---

## What this covers

This document covers external capabilities reached through:

- Direct REST or GraphQL APIs (without MCP wrapping)
- gRPC or proprietary protocol services
- Filesystem-mounted resources (operator-side mounts that the cadre reads or writes)
- Command-line tools invoked through controlled execution wrappers
- Webhooks and event streams (where the cadre is a consumer or producer)

This document does not cover:

- MCP-wrapped tools (covered in `integration/mcp-server-onboarding.md`)
- Anthropic-stack tooling (covered in `integration/model-provider-integration.md`)
- Within-cadre filesystem handoffs (covered in `architecture/handoff-contracts.md`)

---

## Default posture

The default posture is: do not use a non-MCP tool when an MCP-wrapped equivalent exists. MCP wrapping provides the protocol-level controls (RFC 8707, OAuth 2.1, structured tool schemas) that direct integrations lack. The friction of MCP onboarding is itself a feature.

When an MCP equivalent does not exist, the operator may onboard a direct integration, but at a reduced trust posture and with documented compensating controls.

---

## Onboarding requirements

A non-MCP tool requires more, not less, scrutiny than an MCP server. The onboarding artifact (at `engagements/<id>/integration/external-tools/<tool-slug>.md`) covers everything the MCP onboarding intake covers, plus:

- **Authentication mechanism.** Specifically what replaces OAuth 2.1; how credentials are stored; how rotation works
- **Resource scoping.** Specifically what replaces RFC 8707; how the cadre prevents cross-resource confused-deputy
- **Schema validation.** Tool inputs and outputs do not have MCP's schema layer; the cadre wraps the tool with a validating adapter and the adapter's schema is reviewed at Tier 2
- **Audit instrumentation.** Direct integrations do not emit MCP-level audit signals; the wrapping adapter is responsible for emission; A19 confirms emissions match the structure required by `governance/audit-chain-spec.md`
- **Failure mode coverage.** Direct integrations often have richer and less-documented failure modes than MCP servers; the adapter must classify and handle each; failures that escape the adapter become incidents

---

## Trust tiers for non-MCP tools

The same Tier I–IV scheme used for MCP servers applies, but the framework-default tier is one step lower than the MCP equivalent would receive:

- A direct integration to a vendor that would be Tier II for MCP is Tier III for direct
- A direct integration to a vendor that would be Tier III for MCP is Tier IV for direct
- A direct integration to an operator-owned tool may be Tier I when the operator commits to building MCP-equivalent controls in the wrapping adapter and the wrapping is reviewed at Tier 3

The downward bias reflects the missing protocol-level guarantees and is intentional.

---

## Wrapping adapters

Every non-MCP tool is invoked through a wrapping adapter, not directly by an agent. The adapter:

- Validates input against a declared schema before invocation
- Applies authentication and scoping per engagement allowlist
- Validates output against a declared schema before returning to the agent
- Emits structured audit entries matching the audit chain spec
- Applies rate limiting and circuit-breaker behavior to prevent runaway use
- Translates tool-specific failure modes into structured error contracts the calling agent can handle

Adapters live in operator-side code, not in framework code. The framework specifies the contract the adapter must satisfy; operators implement to their stack.

---

## Side-effect-producing tools

Tools that produce external side effects (mutating systems of record, sending external messages, executing financial transactions, mutating infrastructure) require additional discipline regardless of trust tier:

- HITL Tier 3 by default; downgrade to Tier 2 only with documented engagement-specific justification
- Mandatory dry-run mode where feasible (the adapter runs the tool in a non-mutating mode first; the agent reviews; only after explicit approval does the mutating call proceed)
- Mandatory idempotency keys where the tool supports them; the adapter generates and tracks keys to prevent duplicate side effects on retry
- Mandatory rollback path or compensating action documentation; the cadre must know how to undo or compensate if the side effect proves incorrect

---

## Filesystem-mounted resources

When the cadre reads or writes operator-mounted filesystem paths beyond the engagement's own `engagements/<id>/` tree, the path validator (per `architecture/memory-architecture.md`) governs the access:

- The mounted path is registered as a resource with explicit scope rules
- Reads are permitted within scope; writes are governed by the same engagement-isolation rules as memory
- The audit emission requirements for filesystem operations match the audit chain spec
- Symbolic links and bind mounts are evaluated at the validator level; the validator does not honor links that escape the registered scope

---

## Webhook discipline

When the cadre is a webhook consumer (an external system POSTs events to the cadre):

- The webhook endpoint is operator-managed infrastructure; the cadre receives validated events from operator-side ingestion
- Events are not trusted on receipt; an A02 (evidence classifier) pass is applied before events influence cadre behavior
- Webhook authentication (signatures, mutual TLS) is operator-side; the cadre receives only post-validation events

When the cadre is a webhook producer (the cadre POSTs to an external endpoint):

- The endpoint is in the engagement's allowlist with explicit scope
- The POST is treated as a side-effect-producing tool call (Tier 2 minimum, often Tier 3)
- Retries and idempotency keys are required per side-effect discipline

---

## Failure modes

- **Adapter contract violation.** The adapter sent unstructured output past its schema; the agent received malformed data. Treated as a Sev-2 incident; the adapter is repaired and re-reviewed before resumed use.
- **Credential leakage.** A direct-integration credential leaks. Sev-1 incident; immediate credential rotation; scope of any potential exposure is investigated; affected engagement is paused while scope is bounded.
- **Side effect without compensating path.** A side-effect-producing tool was invoked without a documented rollback. Sev-2; the operator's recovery path is invoked; the documentation gap is closed before further use.
- **Rate limit cascade.** A non-MCP tool's rate limits trigger circuit breakers that propagate to dependent agents. A14 surfaces the cost; A13 considers whether the cascade was a single-event or structural; structural fixes go through framework change discipline.

---

## Cross-references

- `integration/mcp-server-onboarding.md` — preferred path
- `architecture/handoff-contracts.md` — schema discipline
- `architecture/memory-architecture.md` — path validation for filesystem-mounted resources
- `governance/audit-chain-spec.md` — emission requirements adapters must meet
- `governance/known-limitations.md` — when non-MCP integration is permitted at all
