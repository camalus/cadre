# Engagement Charter Template

*The authoritative engagement-level document. Copy to `engagements/<id>/charter.md`, fill in, and route through the new-engagement-startup workflow's Phase 2 review.*

---

## Template body

```markdown
# Engagement Charter — <Operator Name> / <Engagement Slug>

**Engagement ID:** <opaque ID assigned by operator>
**Charter version:** v1
**Effective date:** <ISO date>
**Termination date (planned):** <ISO date or "open-ended">

## 1. Parties

- **Operator:** <legal entity name>
- **Engagement lead (operator-side):** <name, role, contact>
- **Engagement sponsor (operator-side):** <name, role>
- **Compliance officer (operator-side):** <name, role>
- **Cadre vendor:** <BHIL or operator's internal cadre owner>
- **Tier 3 signatories:** <list, when sector triggers apply>

## 2. Scope

### 2.1 In scope
<Concrete deliverables, cadence, success criteria.>

### 2.2 Out of scope
<Explicit exclusions to prevent scope creep.>

### 2.3 Use cases
<Specific use cases, including any consequential decisions in scope.>

## 3. Sector and jurisdiction

- **Sector classification:** <e.g., healthcare, banking, employment, general-business>
- **Jurisdictions:** <EU member states, US states, UK, other>
- **Regulatory triggers identified:** <HIPAA, GDPR, EU AI Act category, NYC LL 144, Colorado SB24-205, sector-specific>
- **Operator policies that bind this engagement:** <reference operator's policy library>

## 4. Cadre composition

- **Activated agents:** <list of A0X IDs activated for this engagement>
- **Deactivated agents:** <list with rationale>
- **Augmenting agents (operator-supplied):** <if any, with their own specs referenced>
- **Squad ownership:** <which squads are operational; any modifications to default squad structure>

## 5. HITL configuration

- **Tier defaults per action class:** <table referencing or extending `governance/hitl-policy.md` defaults>
- **Reviewer roster (mapped to tiers and to sector/jurisdiction/role attributes):**
  | Reviewer | Role | Jurisdiction | Sector | Tier authority | Load capacity |
  |---|---|---|---|---|---|
  | <name> | <role> | <list> | <list> | <0-3> | <decisions/week> |
- **SLO commitments:** <Tier 2 SLO, Tier 3 SLO; expedited paths>
- **Escalation paths:** <SLO-breach handling, Tier-3 escalation>

## 6. Memory configuration

- **Per-engagement memory location:** `engagements/<id>/memory/`
- **Cross-engagement learnings access policy:** <read access scope, promote-learnings authorization>
- **Sanitization policy for promotions:** <reference `governance/memory-policy.md`; engagement-specific addenda>
- **Provider-side memory (Managed Agents Memory or equivalent):** <not enabled by default; if enabled, the policy posture is documented here>

## 7. Allowlists

### 7.1 MCP servers
<List of approved servers with trust tier per server, per-tool allowlist, audit emission requirements. References `integration/mcp-server-onboarding.md`.>

### 7.2 External tools (non-MCP)
<List with adapter references, trust tier, side-effect classification. References `integration/external-tool-allowlist.md`.>

### 7.3 Model variants
<Per-agent model assignment; deviations from framework defaults with rationale.>

## 8. Audit configuration

- **Chain storage location:** <operator-side path>
- **Retention horizon:** <absolute and per-sector overrides>
- **Verification cadence:** <weekly minimum; tighter for sector triggers>
- **External anchoring:** <if any; details>

## 9. Cost ceiling

- **Engagement-level ceiling:** <amount, period (monthly / quarterly / total)>
- **A14 escalation thresholds:** <e.g., 75% triggers warning; 90% triggers Tier 2 review>
- **Emergency-stop authority:** <named individual or role with authority to halt cadre on cost grounds>

## 10. Termination conditions

- **Planned end:** <date or condition>
- **Operator-initiated termination:** <notice period; obligations on termination>
- **Cadre-initiated triggers:** <repeated incidents, regulatory finding, charter violations>
- **Wind-down obligations:** <reference `workflows/engagement-closeout.md`>

## 11. Signatures

- **Engagement lead:** <name, date, signature reference>
- **Engagement sponsor:** <name, date, signature reference>
- **Compliance officer:** <name, date, signature reference>
- **Tier 3 signatories (when applicable):** <names, dates, signature references>

## 12. Charter amendments

Charter changes follow the framework's standard change discipline plus engagement-specific Tier 2 (or Tier 3 for sector-triggered changes) review. Amendments are versioned (v2, v3, ...); the chain preserves all prior versions.

---

## Cross-references

- `workflows/new-engagement-startup.md`
- `governance/hitl-policy.md`
- `governance/memory-policy.md`
- `governance/audit-chain-spec.md`
- `integration/mcp-server-onboarding.md`
```

---

## Conventions

- The charter is the single authoritative document for the engagement; any conflict between the charter and other engagement artifacts resolves to the charter
- Charter changes after go-live are amendments, not edits; the chain preserves the original
- Reviewer roster discipline (jurisdiction, sector, role, load match) is operator-side; the charter's role is to make the matching auditable
- Termination conditions in section 10 are the only basis for engagement closeout; ad-hoc closeout requires charter amendment first

## Cross-references

- `workflows/new-engagement-startup.md` — Phase 2 invokes this template
- `workflows/engagement-closeout.md` — termination conditions defined here are the trigger
- `governance/hitl-policy.md`
- `governance/memory-policy.md`
- `integration/mcp-server-onboarding.md`
