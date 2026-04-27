# Memory Architecture

*The CADRE Framework uses Anthropic's **Managed Agents Memory** (public beta, April 23, 2026) as the substrate for agent memory, with a strict path-validation discipline that prevents engagement-to-engagement data bleed and enforces operator control over cross-engagement learnings.*

---

## Three memory scopes

Every CADRE agent declares one of three memory scopes:

### `none`
The agent maintains no persistent memory. Each invocation starts fresh from input. This is the default for stateless utility agents.

### `per-engagement`
The agent maintains memory scoped to a single engagement. Memory is stored under `engagements/<engagement_id>/memory/<agent_id>/` and is automatically scoped to the engagement context. When the engagement closes, per-engagement memory is archived per `../governance/memory-policy.md` retention rules.

Most CADRE agents use `per-engagement` memory. It accumulates working state within an engagement (search history, decisions made, references collected) without leaking across engagement boundaries.

### `cross-engagement`
The agent has access to operator-level memory that persists across engagements. This is essential for:

- A16 Policy Gatekeeper's rulebook (the operator's regulations don't change per engagement)
- A18 PII Redactor's pattern library (HIPAA Safe Harbor identifiers are the same for every healthcare engagement)
- A19 Audit Logger's chain infrastructure (one chain per engagement, but the infrastructure is operator-shared)
- A20 Compliance Mapper's obligations catalog and templates

Cross-engagement memory is **read freely**, but **writes require the "promote learnings" workflow** (see below). This is a deliberate asymmetry: agents can benefit from accumulated operator knowledge without being able to silently propagate engagement-specific data to the operator's shared layer.

---

## Path validation pattern

Every memory access in CADRE passes through path validation, implemented in `../tools/scripts/validate-handoff.py`:

```python
def validate_per_engagement_path(agent_id: str, engagement_id: str, path: str) -> bool:
    """
    A per-engagement memory operation is valid iff:
      - the path is under engagements/<engagement_id>/memory/<agent_id>/
      - the engagement_id matches the orchestrator's current engagement context
      - the agent_id matches the calling agent
    Any path that escapes the engagement_id boundary is rejected.
    """
    expected_prefix = f"engagements/{engagement_id}/memory/{agent_id}/"
    normalized = os.path.normpath(path)
    if not normalized.startswith(expected_prefix):
        raise PathValidationError(f"Path {path} escapes engagement boundary")
    if ".." in path.split("/"):
        raise PathValidationError(f"Path {path} contains parent traversal")
    return True


def validate_cross_engagement_path(agent_id: str, path: str, mode: str) -> bool:
    """
    A cross-engagement operation is valid iff:
      - the path is under cross-engagement/<agent_id>/
      - reads are allowed for any agent declared cross-engagement scope
      - writes require an active 'promote learnings' workflow context
    """
    expected_prefix = f"cross-engagement/{agent_id}/"
    normalized = os.path.normpath(path)
    if not normalized.startswith(expected_prefix):
        raise PathValidationError(f"Path {path} escapes agent boundary")
    if mode == "write" and not promote_learnings_active():
        raise PathValidationError("Cross-engagement writes require promote-learnings context")
    return True
```

These validators are not optional. They run in front of every memory operation, regardless of which agent is calling. A misbehaving agent that attempts to read another engagement's memory or write directly to cross-engagement memory is stopped at the validator boundary — the violation is logged through A19 as an incident.

---

## The "promote learnings" workflow

Cross-engagement writes happen only inside an explicit human-supervised workflow:

1. An agent (most often A16, A18, or A20) emits a **promotion candidate** as a per-engagement artifact: e.g., "this redaction pattern caught a previously-unseen PII variant; propose adding to the cross-engagement library"
2. The candidate is reviewed by a named human (per `../governance/hitl-policy.md` Tier 2)
3. On approval, the workflow runs with `promote_learnings_active() == True`, which is the only context in which `validate_cross_engagement_path(mode="write")` returns True
4. The promotion is logged through A19 as an event of type `memory_promotion` with the human reviewer's identity, the candidate's source engagement, and a hash of the promoted content

The workflow's existence makes cross-engagement memory auditable and reversible. If a promotion turns out to be incorrect (or worse, leaks engagement-specific content into the operator-shared layer), it can be rolled back, and the audit chain shows exactly when, by whom, and from where.

---

## Retention and rollback

### Retention
- **Per-engagement memory** is retained while the engagement is active. On engagement close, memory is archived to cold storage per the engagement's contractual retention period (typically 7 years for regulatory matters, longer for healthcare per HIPAA).
- **Cross-engagement memory** is retained indefinitely but versioned. Every promotion is a new version; old versions are not deleted.
- **Audit chain entries** are retained per the operator's regulatory obligations, which is typically the longest retention requirement that applies.

### Rollback
- **Per-engagement memory** rollback is per-agent-per-engagement: the agent can be re-run from a checkpoint without affecting other engagements. The operator's checkpoint cadence is configurable; default is one checkpoint per major workflow stage.
- **Cross-engagement memory** rollback reverts the cross-engagement layer to a prior version. This is a high-impact operation: it requires a documented rationale, named human approval, and an audit chain entry of type `memory_rollback`.

---

## Failure modes and mitigations

| Failure mode | Mitigation |
|---|---|
| Engagement-to-engagement data bleed | Path validation rejects cross-boundary access; violations logged as incidents |
| Silent cross-engagement writes | `validate_cross_engagement_path(mode="write")` requires explicit workflow context; otherwise rejects |
| Stale cross-engagement memory | Versioning by date; A20 Compliance Mapper monitors aging entries |
| Memory exhaustion | A14 Cost Meter monitors memory tier capacity; pressure triggers incident, not silent drop |
| Path-traversal attack via crafted input | Validators reject any path containing `..` or escaping the expected prefix |
| Promote-learnings workflow bypass | Workflow context is set by the orchestrator under HITL supervision; agents cannot self-set the context |

---

## What CADRE deliberately does *not* do with memory

- **No implicit memory sharing across engagements.** If two engagements would benefit from the same finding, the path is the promote-learnings workflow, not silent cross-engagement reads.
- **No memory-mediated communication between agents.** Inter-agent communication happens through the handoff-contracts layer (`handoff-contracts.md`), not through memory side channels.
- **No long-context-window-as-memory.** Even with Opus 4.6's 1M context, CADRE uses the Managed Agents Memory tools for state persistence, not in-context accumulation. This is a robustness choice: long-context models drift; memory tools don't.
- **No client data in cross-engagement memory.** Cross-engagement memory is for operator infrastructure (rulebooks, patterns, templates). Client data stays in `engagements/<id>/`. Violations are incidents.

---

## Citations

- Anthropic. *Managed Agents Memory* — public beta announcement, April 23, 2026. [VERIFIED]
- BHIL LOCUS Framework — `governance/memory-policy.md` benchmark for path-validation discipline. [INTERNAL — versioned at github.com/camalus/BHIL-LOCUS-Framework]
- HIPAA Privacy Rule retention guidance, 45 CFR 164.530(j). [VERIFIED]
- ISO/IEC 27001:2022, Annex A.5.33 — Protection of records.

---

*BHIL CADRE Framework — architecture/memory-architecture.md — v1.0.0*
