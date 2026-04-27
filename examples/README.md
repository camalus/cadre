# Examples

This directory holds anonymized walkthroughs that demonstrate the CADRE
Framework end-to-end. Examples are reference material — they are read,
not run. Real engagements live under `engagements/` (gitignored) and
never appear here.

## What is in here

- `sample-engagement/` — a complete Express-to-Full SKU walkthrough for
  a fictional mid-market services firm. Demonstrates the readiness
  diagnostic, cadre activation decisions, handoff sequence, and final
  deliverable structure.

## What you will not find

- Real client names, sectors, or identifying details.
- Any handoff artifact containing PII or proprietary data.
- Working credentials, API keys, or MCP tokens.
- Engagement audit chains from real engagements.

## How to read an example

Each example folder is numbered to indicate reading order (`00-` first,
`05-` last). Read top to bottom. Each numbered file represents a
checkpoint in the engagement lifecycle.

## How to use an example

The most common uses:

1. **Onboarding a new operator** — read the sample top to bottom before
   running your first engagement.
2. **Reference during engagement** — when you are unsure what an
   artifact at stage N should look like, find the corresponding file
   in the sample.
3. **Sales conversations** — clients often ask "what does the deliverable
   look like?" The sample is the safe-to-share answer.

## Adding a new example

If you want to contribute a new example:

1. Anonymize ruthlessly — substitute names, sectors, and quantities.
2. Run `tools/scripts/audit-chain-verify.py` against the example chain
   if you include one — examples must demonstrate a valid chain.
3. Open a PR using the example template.
