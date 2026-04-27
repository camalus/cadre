---
engagement_id: NL-2026-0341
client: NorthlineCo (fictional)
sku: Express
sku_price_usd: 6500
credit_window_days: 60
charter_signed_date: 2026-04-08
diagnostic_date: 2026-04-15
operator_lead: J. Hurd
client_sponsor: VP Operations (fictional, "Marcus Chen")
jurisdictions: [US]
sector: logistics-services
sector_regulated: false
reviewer_roster_path: engagements/NL-2026-0341/reviewer-roster.json
---

# Engagement Charter — NorthlineCo Express Diagnostic

## 1. Purpose

NorthlineCo has engaged BHIL for a one-day AI Readiness Diagnostic to
evaluate their preparedness for deploying an AI assistant on their
internal Tier-1 support desk. The diagnostic produces a 7-dimension
scorecard and a Sprint Quote for any follow-on build engagement.

## 2. Scope

### In scope

- Use case: internal support assistant for field operations team
- Channels: existing Slack-based support workflow
- Audience: ~120 field operations staff who currently file Tier-1
  tickets
- Knowledge base: existing internal Confluence pages and Zendesk macros

### Out of scope

- Customer-facing AI features (deferred to potential later engagement)
- Procurement of model providers (NorthlineCo has Anthropic API access)
- Implementation of any recommendations (this is diagnostic only)
- Vendor contract review (separate legal workstream)

## 3. SKU and pricing

| Item                          | Value                       |
|-------------------------------|-----------------------------|
| SKU                           | Express Diagnostic          |
| Price                         | $6,500 USD                  |
| Duration                      | 1 day on-site (8 hours)     |
| Deliverables                  | Scorecard + Sprint Quote    |
| Credit-toward-Full window     | 60 days from diagnostic date|
| Credit amount if converted    | 100% of $6,500              |

## 4. Reviewer roster

Loaded into `engagements/NL-2026-0341/reviewer-roster.json`. Summary:

| Tier | Reviewer                     | Role           | Capacity |
|------|------------------------------|----------------|----------|
| 1    | A. Patel (BHIL)              | Domain SME     | 4 hrs/wk |
| 2    | J. Hurd (BHIL)               | Operator       | 8 hrs/wk |
| 3    | J. Hurd (BHIL)               | Operator-prime | as needed|

For the Express engagement only Tier 1 and Tier 3 are likely to fire.

## 5. Cost envelope

| Stage                | Token budget (M) |
|----------------------|------------------|
| Diagnostic intake    | 0.4              |
| 7-dimension scoring  | 1.5              |
| Synthesis            | 0.4              |
| Sprint Quote drafting| 0.2              |
| Total Express        | 2.5              |

## 6. Jurisdictions and sector

US-only operation. Logistics services — not subject to HIPAA, EU AI
Act high-risk classifications, or NYC AEDT (no employment decisions
involved). General data-protection discipline applies. No specific
sector overlay.

## 7. Confidentiality and data handling

- All NorthlineCo material remains under
  `engagements/NL-2026-0341/` (gitignored).
- No NorthlineCo data is promoted to the cross-engagement knowledge
  base without separate operator review and PII redaction (see
  `workflows/promote-learnings.md`).
- Audit chain at `engagements/NL-2026-0341/audit-chain.jsonl`.

## 8. Acceptance criteria

The diagnostic is accepted when:

1. The 7-dimension scorecard is delivered as a branded `.docx`.
2. The Sprint Quote is delivered as a branded `.docx`.
3. Both documents have passed Tier-3 HITL review.
4. The audit chain verifies cleanly via
   `tools/scripts/audit-chain-verify.py`.

## 9. Sign-off

| Party          | Name           | Date       |
|----------------|----------------|------------|
| BHIL operator  | J. Hurd        | 2026-04-08 |
| Client sponsor | M. Chen (fict.)| 2026-04-08 |
