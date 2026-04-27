# `tools/scripts/` — CADRE operational scripts

Five scripts that support the CADRE Framework outside the agent runtime.
Each is a single-file Python 3.10+ utility with `argparse`, explicit exit
codes, and no third-party dependencies beyond what's already in the
framework's environment (`jsonschema` for handoff validation).

| Script | Purpose | When it runs |
|---|---|---|
| `path-guard.py` | PreToolUse hook that blocks framework-path edits unless `BHIL_CADRE_FRAMEWORK_EDIT=1` is set. | Every Claude Code tool call, automatically (registered in `.claude/settings.json`). |
| `validate-handoff-schemas.py` | Strict JSON Schema 2020-12 validation of handoff contracts (citations, HITL decisions, audit entries). | CI on PR; locally before merging engagement artifacts. |
| `audit-chain-verify.py` | Verifies SHA-256 hash chain integrity across `audit-log.jsonl`. Catches tampering or missing entries. | Engagement closeout; periodic spot checks; incident review. |
| `cost-calculator.py` | Quick token-cost projection across SKUs (Express / Full / Complete / Enterprise). Planning tool. | Engagement scoping; quote preparation. **Not** an authoritative meter — that's A14. |
| `generate-readiness-scorecard.py` | Populates the 7-dimension readiness scorecard markdown skeleton from CLI args or a JSON file. | After the readiness diagnostic; before the engagement charter is signed. |

---

## `path-guard.py`

Blocks edits to framework-canonical paths (`prompts/`, `cadre/`,
`architecture/`, `governance/`, etc.) unless an explicit env override is
present. Allows edits inside `engagements/<id>/` always.

```bash
# Normal engagement work — no env var needed
python3 tools/scripts/path-guard.py --tool Edit --path engagements/NL-2026-0341/handoffs/atlas-keel.json
# exit 0

# Framework edit attempt — blocked
python3 tools/scripts/path-guard.py --tool Edit --path prompts/SP-03.md
# exit 2, prints reason

# Authorized framework edit — allowed
BHIL_CADRE_FRAMEWORK_EDIT=1 python3 tools/scripts/path-guard.py --tool Edit --path prompts/SP-03.md
# exit 0
```

Registered as a `PreToolUse` hook in `.claude/settings.json`. See
`.claude/rules/00-framework-vs-engagement.md` for the policy this enforces.

---

## `validate-handoff-schemas.py`

Validates handoff JSON files against the embedded JSON Schema 2020-12
fragments for `citation`, `hitl_decision`, and `audit_entry`. Use `--all`
to walk a directory.

```bash
# Single file
python3 tools/scripts/validate-handoff-schemas.py engagements/NL-2026-0341/handoffs/vanta-atlas.json

# All handoffs in an engagement
python3 tools/scripts/validate-handoff-schemas.py --all engagements/NL-2026-0341/handoffs/
```

Exit codes:
- `0` — all valid
- `1` — at least one validation failure (full report on stderr)
- `2` — I/O or schema error

---

## `audit-chain-verify.py`

Walks `audit-log.jsonl` and verifies that every entry's `prev_hash` matches
the SHA-256 of the previous entry's canonicalized payload, and that
timestamps are monotonically non-decreasing.

```bash
python3 tools/scripts/audit-chain-verify.py engagements/NL-2026-0341/audit-log.jsonl
```

If the chain is intact, prints `OK — N entries verified` and exits 0.
If broken, prints the first failure with line numbers and exits 1.

This is the integrity check behind the audit trail described in
`governance/audit-chain-spec.md`.

---

## `cost-calculator.py`

Quick token-cost projection. Reads the SKU mix (Express / Full / Complete /
Enterprise) and returns expected cost in USD using current Anthropic
pricing. Update prices in the `PRICING` dict when rates change.

```bash
# Project Full SKU at default mix
python3 tools/scripts/cost-calculator.py --sku full

# Override actual measured tokens (M tokens)
python3 tools/scripts/cost-calculator.py --sku express --tokens-actual 2.1

# Custom split: opus_in opus_out sonnet_in sonnet_out (M tokens each)
python3 tools/scripts/cost-calculator.py --custom 5.0 3.0 2.0 1.5
```

This is for **scoping**, not invoicing. The authoritative cost meter is
A14, which reads real usage from the provider's API in real time.

---

## `generate-readiness-scorecard.py`

Populates the readiness scorecard markdown from a 7-dimension score input.
Mirrors the layout in `readiness/scoring-template.md`. Output is plain
markdown ready to feed the `bhil-docx` skill for branded conversion.

```bash
# CLI form — seven ints in canonical dimension order
python3 tools/scripts/generate-readiness-scorecard.py \
    --client "NorthlineCo" \
    --engagement NL-2026-0341 \
    --scores 3 2 2 1 2 2 2 \
    --out engagements/NL-2026-0341/01-readiness-diagnostic.md

# JSON form — full payload with evidence per dimension
python3 tools/scripts/generate-readiness-scorecard.py \
    --input engagements/NL-2026-0341/readiness-scores.json \
    --out engagements/NL-2026-0341/01-readiness-diagnostic.md
```

Composite tier mapping (composite = sum of seven 0-4 scores):

| Composite | Tier | Path |
|---|---|---|
| 24–28 | Ready | Full or Complete SKU |
| 17–23 | Mostly Ready | Full SKU + targeted remediation |
| 10–16 | Approaching Ready | Express SKU first |
| 0–9 | Not Ready | Express + foundational engagement |

---

## Script conventions

- **Single-file, no install step.** Run with `python3 tools/scripts/<name>.py`.
- **Argparse with `--help`.** Every script self-documents.
- **Explicit exit codes.** `0` success, `1` validation failure, `2` I/O error.
- **Stderr for diagnostics, stdout for results.** Pipe-friendly.
- **No global state.** Each invocation reads inputs, writes outputs, exits.

If you add a script here, follow the same pattern and add a row to the table
above. Anything stateful or long-running belongs as an agent in `cadre/`,
not here.
