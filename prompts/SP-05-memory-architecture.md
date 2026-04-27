---
id: CADRE-SP-05
title: "SP-05 — Memory Architecture"
version: "1.0"
type: sub-prompt
sequence: 5
input_artifacts: ["agents/A##-*.md", "mcp-config.json"]
output_artifact: "memory-config.md"
hitl_tier: 2
---

# SP-05 — Memory Architecture

*Defines memory scope per agent, validates path-traversal protections, and sets retention policies. Outputs `memory-config.md` for the engagement.*

---

## Purpose

CADRE uses Anthropic's Managed Agents Memory (public beta April 23, 2026) as the procedural substrate. Managed Agents Memory mounts a filesystem into the sandbox with per-user, per-workspace, and org-wide scopes, audit logs, rollback, and differential read/write permissions for multi-agent concurrency.

Anthropic's documentation on the underlying Memory Tool (`memory_20250818`, beta since September 29, 2025) is explicit:

> *"Your implementation MUST validate all paths to prevent directory traversal attacks."*

SP-05 is the engagement-specific application of that rule. It assigns each agent a memory scope, defines the path-validation pattern, and sets retention/rollback policies.

---

## Inputs

- **`engagements/<id>/agents/A##-*.md`** — agent specs from SP-02
- **`engagements/<id>/mcp-config.json`** — MCP config from SP-04
- **`architecture/memory-architecture.md`** — the architectural pattern
- **`.claude/rules/memory-safety.md`** — the path-validation rule

---

## Output

**`engagements/<id>/memory-config.md`** — the memory configuration document. Contents:

1. **Engagement memory map** — per-agent scope and rationale
2. **Path-validation patterns** — concrete code/regex for each scope
3. **Retention policy** — how long memory persists; rollback windows
4. **Cross-engagement isolation** — confirmation that no client data leaks across engagements
5. **Audit configuration** — where memory operations are logged

---

## Step-by-step

### Step 1 — Classify each agent's memory scope

The three scopes:

- **`none`** — agent holds no persistent memory; every invocation is a clean slate
- **`per-engagement`** — memory persists across the engagement but is destroyed at engagement close
- **`cross-engagement`** — memory persists across engagements (rare; reserved for shared rulebooks and cross-engagement learning)

Defaults from SP-02:

- VANTA (A01–A05): `per-engagement` for accumulated research
- ATLAS (A06–A10): `per-engagement` for spec drafts and roadmap state
- KEEL eval/audit (A11, A12): `cross-engagement` for eval history; `per-engagement` for incident state
- KEEL cost/incident (A13, A14): `per-engagement` only
- KEEL handoff validator (A15): `none` (each handoff is independent)
- PULSE policy/HITL/audit (A16, A17, A19): `cross-engagement` for rulebooks and audit trails
- PULSE PII/compliance (A18, A20): `per-engagement` for client-specific data; `cross-engagement` for redaction rulebooks

Override defaults only with documented justification.

### Step 2 — Define path-validation patterns

Every memory operation must validate the path before reading or writing. The validation pattern depends on scope:

**For `per-engagement` memory**, the agent's working root is `engagements/<engagement_id>/memory/A##/`. Every path must satisfy:

```python
def validate_per_engagement_path(path: str, engagement_id: str, agent_id: str) -> bool:
    # Resolve the path to its absolute form
    resolved = os.path.realpath(path)
    expected_root = os.path.realpath(f"engagements/{engagement_id}/memory/{agent_id}")
    # Must be under expected root
    if not resolved.startswith(expected_root + os.sep):
        return False
    # No symlinks pointing outside
    if os.path.islink(path) and not os.path.realpath(path).startswith(expected_root):
        return False
    return True
```

**For `cross-engagement` memory**, the agent's working root is `cross-engagement/<agent_id>/`. Same validation pattern with the cross-engagement root.

The path-validation function lives in `tools/scripts/validate-handoff.py` and is called by every memory-using agent before any file operation. **No agent reads or writes memory without going through the validator.**

### Step 3 — Set retention policy

Per-engagement memory: deleted at engagement close (status = "complete" or "terminated"). Default retention 90 days post-close for audit purposes; configurable per SKU tier.

Cross-engagement memory: indefinite for rulebooks (PULSE A16, A17, A18); 7-year retention for audit trails (A19, sufficient for SR 11-7 / OCC and most regulatory frameworks); 2-year retention for eval history (A11) unless extended by client.

### Step 4 — Configure rollback

Managed Agents Memory supports rollback. Configure rollback windows per scope:

- `per-engagement`: 24-hour rollback window for accidental deletions
- `cross-engagement` rulebooks: 7-day rollback for accidental rule changes
- `cross-engagement` audit trails: NO rollback (audit trails are append-only and immutable by policy)

### Step 5 — Cross-engagement isolation check

For any agent with `cross-engagement` memory, document explicitly what data is and is NOT shared across engagements:

- Rulebooks (regulatory text, internal policy templates) — shared
- Eval criteria templates — shared
- Audit trail entries — append-only, retained per agent / per engagement, but the AGENT'S memory of having logged an entry is shared (so audits across engagements are possible)
- **Client data** — NEVER shared. PII, proprietary content, engagement-specific decisions stay in `per-engagement`.

If any agent's `cross-engagement` memory could plausibly leak client data, downgrade to `per-engagement` or escalate.

### Step 6 — Audit configuration

Every memory operation is logged:

- **Read** — `{timestamp, engagement_id, agent_id, scope, path, bytes_read}`
- **Write** — `{timestamp, engagement_id, agent_id, scope, path, bytes_written, hash_after}`
- **Delete** — `{timestamp, engagement_id, agent_id, scope, path, hash_before}`

Logs stream to A19 (Audit Logger) per the standard audit schema in SP-03.

### Step 7 — Write `memory-config.md`

Use `templates/memory-config-template.md` as the scaffold. Persist to `engagements/<id>/memory-config.md`.

---

## Quality criteria

- [ ] Every in-scope agent has a declared memory scope (none / per-engagement / cross-engagement)
- [ ] Every non-`none` scope has a path-validation function reference
- [ ] Every cross-engagement scope has explicit "what is and is not shared" documentation
- [ ] Retention policy is set per scope and aligns with SKU tier and regulatory obligations
- [ ] Rollback windows are configured (or explicitly disabled for audit trails)
- [ ] All memory operations route through A19 audit logging

---

## Common failure modes

- **Skipping path validation because "the agent is trusted."** No agent is trusted with raw file paths. The Anthropic docs are explicit: validation MUST happen.
- **Defaulting to cross-engagement memory for "convenience."** Cross-engagement is the exception, not the default. The blast radius of a compromised cross-engagement memory is enormous.
- **Allowing rollback on audit trails.** Audit trails are append-only by definition. Anything that allows rollback is not an audit trail.
- **Vague retention policies.** "Until no longer needed" is not a policy. Set days, weeks, or years with regulatory justification.
- **Storing client PII in cross-engagement memory.** This is a privacy and regulatory failure. Per-engagement only.

---

## Citations

- Anthropic. *Managed Agents Memory* documentation. Public beta announcement, April 23, 2026.
- Anthropic. *Memory Tool API* documentation. Beta since September 29, 2025 (`memory_20250818`).
- Anthropic. *Claude Memory* general availability for free users, March 2, 2026 (with Memory Import Tool).
- CVE-2025-54794 (Claude Code path-related issue).
- CVE-2025-53109, CVE-2025-53110 (Filesystem MCP Server path-related issues).
- The "Managed Agents Memory path traversal CVE" referenced by the Apr 24, 2026 research brief could not be located as of this writing — adjacent CVEs above exist; flag this for periodic re-check.

---

*BHIL CADRE Framework — SP-05 — v1.0.0*
