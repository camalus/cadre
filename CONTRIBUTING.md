# Contributing to BHIL CADRE Framework

CADRE is a BHIL commercial framework. External contributions are welcomed but evaluated against the same depth and citation standards we apply to ourselves. This document explains how to contribute and what we expect.

---

## Before you contribute

1. Read `README.md` for the framework overview and `CLAUDE.md` for the operating rules.
2. Read `architecture/parallel-vs-serial-rule.md` — that is the framework's central thesis. Every contribution should be coherent with it or explicitly engage with it.
3. Open an issue describing what you want to change before opening a pull request, especially for changes to the architectural thesis, agent roster, or governance taxonomy.

---

## What we accept

We accept contributions in five categories:

- **Bug fixes** — typos, broken links, incorrect citations, schema validation errors
- **Citation upgrades** — replacing UNCORROBORATED secondary sources with VERIFIED primary sources
- **Regulatory updates** — when a regulation in `governance/` changes (effective date, statutory language, enforcement guidance), update the file with the new citation and a dated change note
- **New worked examples** — additional engagements in `examples/` demonstrating the framework on different industries or scales
- **Companion framework bridges** — new files in `integration/` documenting how CADRE pairs with other frameworks

---

## What we are slow to accept

- **New top-level directories.** The folder structure is intentional. Convince us first.
- **Changes to the architectural thesis.** The read/write asymmetry rule is the framework's defensible position. Challenges welcomed but require primary-source evidence.
- **New squads or new agents.** The 20-agent / 4-squad structure is sized to be runnable by a solo founder. Adding to it raises the cost floor.
- **Vendor-published metrics presented as VERIFIED.** Vendor self-reports are UNCORROBORATED until independently audited. Do not upgrade their classification without an audit citation.

---

## Citation discipline

Every empirical claim in this repo must be citable to a named source with a date. Apply VERDICT-style classification:

- **VERIFIED** — primary source (peer-reviewed paper, official documentation, regulatory text, court ruling, vendor's own technical blog)
- **CORROBORATED** — multiple independent secondary sources confirm
- **UNCORROBORATED** — single secondary source, vendor self-report, trade press, LinkedIn thread
- **INFERENCE** — your own reasoning from the evidence; flag explicitly with "[INFERENCE]"

When you contribute new content, label your evidence. Reviewers will reject contributions that present UNCORROBORATED material as VERIFIED.

---

## Commit conventions

We use [Conventional Commits](https://www.conventionalcommits.org/) with a CADRE-specific scope vocabulary:

```
<type>(<scope>): <description>
```

**Types:**
- `feat` — new content (new agent, new prompt, new example)
- `fix` — bug fix or correction
- `docs` — documentation-only changes (README updates, README of a directory)
- `cite` — citation upgrade or correction
- `gov` — governance / regulatory update
- `arch` — change to architectural thesis or its support
- `chore` — tooling, CI, dependencies

**Scopes** correspond to top-level directories: `prompts`, `cadre`, `architecture`, `readiness`, `governance`, `workflows`, `integration`, `templates`, `examples`, `tools`, `claude` (for `.claude/`), `gh` (for `.github/`).

**Examples:**

```
feat(cadre): add A11 eval-runner agent specification
cite(governance): upgrade EU AI Act Article 14 citation to official OJ reference
fix(prompts): correct SP-9 SKU pricing range (was $4500-$5500, now $4500-$7500)
arch(architecture): add Cynefin-domain-specific autonomy constraints to read/write rule
```

---

## Pull request process

1. **Branch from `main`.** Use a descriptive branch name (`feat/cadre-a11-eval-runner`, `cite/eu-ai-act-article-14`).
2. **Write the PR description with the same depth as the change.** Trivial typo fixes can be one-line. Architectural changes require a position statement, citations, and an explicit list of which existing files this affects.
3. **Run the validation workflow locally** before opening the PR:
   ```
   tools/scripts/validate-handoff.py
   ```
4. **Pass CI.** The workflows in `.github/workflows/` enforce markdown linting, JSON Schema validation for handoff contracts, and link integrity. PRs that fail CI will not be merged.
5. **Address review comments.** Reviewers will ask for citations, request scope clarification, and push back on UNCORROBORATED claims presented as VERIFIED. This is the design.
6. **Update the CHANGELOG.** Add an entry under the appropriate version heading. Use the same vocabulary as commit types.

---

## What gets reviewed

Every PR is reviewed by a BHIL maintainer. Review covers:

- **Citation integrity** — do the sources support the claims?
- **Architectural coherence** — does this contribution honor the read/write asymmetry rule?
- **HITL discipline** — does any new agent or workflow specify the appropriate HITL tier?
- **Compliance alignment** — does this contribution introduce regulatory exposure that isn't already mapped in `governance/`?
- **Brand voice and depth** — does the writing match the existing repo's standard?

---

## Confidentiality

Do not include client data, client-identifiable information, or non-public engagement details in any contribution. Working engagement files belong in `engagements/<client-id>/` which is gitignored. If you find such material in a commit history, surface it to the repo owner immediately so it can be redacted.

---

## License

By contributing, you agree your contributions will be licensed under the repository's MIT license with the AI accuracy / HITL disclaimer attached.

---

## Contact

Repository owner: Barry Hurd, BHIL.
For substantive contributions, open an issue first. For sensitive disclosures (security, compliance, client data exposure), email directly rather than filing a public issue.

---

*BHIL CADRE Framework — Contributing — v1.0.0*
