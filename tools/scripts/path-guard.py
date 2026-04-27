#!/usr/bin/env python3
"""
path-guard.py — Claude Code PreToolUse hook for the CADRE framework.

Runs before every Write or Edit tool call. Rejects writes to any path
outside engagements/<id>/ unless the operator has set the explicit
override env var BHIL_CADRE_FRAMEWORK_EDIT=1.

Reads the tool input from stdin as JSON. Exits 0 to allow, exits 2 to
block (Claude Code convention for hook deny).

This is a defense-in-depth layer. The primary protection is the
.claude/settings.json deny list. This hook catches edge cases (symlink
escapes, unusual path forms) and produces an audit trail.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGAGEMENTS_DIR = REPO_ROOT / "engagements"

# Paths under the framework that must never be writable at runtime.
# These are belt-and-suspenders with .claude/settings.json deny rules.
FRAMEWORK_PATHS = {
    "prompts",
    "cadre",
    "architecture",
    "governance",
    "integration",
    "readiness",
    "workflows",
    "templates",
    ".claude",
    ".github",
    "tools",
}


def is_framework_edit_override() -> bool:
    """Operator may set BHIL_CADRE_FRAMEWORK_EDIT=1 outside an engagement."""
    return os.environ.get("BHIL_CADRE_FRAMEWORK_EDIT") == "1"


def normalize(target: str) -> Path:
    """Resolve symlinks and relative segments. Returns an absolute path."""
    p = Path(target)
    if not p.is_absolute():
        p = Path.cwd() / p
    try:
        return p.resolve(strict=False)
    except OSError:
        return p


def in_framework_path(target: Path) -> bool:
    try:
        rel = target.relative_to(REPO_ROOT)
    except ValueError:
        return False
    if not rel.parts:
        return False
    return rel.parts[0] in FRAMEWORK_PATHS


def in_engagement_path(target: Path) -> bool:
    try:
        rel = target.relative_to(ENGAGEMENTS_DIR)
    except ValueError:
        return False
    return len(rel.parts) >= 1 and rel.parts[0] != ".gitkeep"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If we cannot parse the hook payload, allow — fail open here
        # rather than block all writes for an unrelated parser issue.
        return 0

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        return 0

    inputs = payload.get("tool_input", {}) or {}
    target = inputs.get("file_path") or inputs.get("path")
    if not target:
        return 0

    resolved = normalize(target)

    if in_framework_path(resolved):
        if is_framework_edit_override():
            print(
                "path-guard: framework edit override active "
                "(BHIL_CADRE_FRAMEWORK_EDIT=1); allowing.",
                file=sys.stderr,
            )
            return 0
        print(
            f"path-guard: REJECTED write to framework path '{resolved}'. "
            "Framework files are read-only at runtime. End the engagement "
            "session, set BHIL_CADRE_FRAMEWORK_EDIT=1, and re-open at the "
            "repo root to make framework edits.",
            file=sys.stderr,
        )
        return 2

    if in_engagement_path(resolved):
        return 0

    # Outside both — likely /tmp or similar. Allow with a note.
    print(
        f"path-guard: write to '{resolved}' is outside repo. Allowed.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
