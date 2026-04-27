#!/usr/bin/env python3
"""
validate-handoff-schemas.py — Strict JSON Schema 2020-12 validator for
CADRE inter-agent handoff artifacts.

Usage:
    python3 validate-handoff-schemas.py <artifact-path>
    python3 validate-handoff-schemas.py --all <engagement-dir>

Exit codes:
    0  All artifacts valid.
    1  One or more artifacts invalid.
    2  Internal error (missing schema, bad input, etc.).

This script is invoked by:
    - A15 Handoff Validator (the canonical implementation)
    - CI in .github/workflows/validate-templates.yml
    - Operators ad-hoc

The script does not load schemas from a separate registry. Schemas are
embedded below — keep them in sync with architecture/handoff-contracts.md.
When that document changes, this script changes in the same PR.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print(
        "ERROR: jsonschema package is required. "
        "Install with: pip install jsonschema>=4.21",
        file=sys.stderr,
    )
    sys.exit(2)


# --- Embedded schema fragments ----------------------------------------------

CITATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["url", "retrieved_at", "evidence_class"],
    "properties": {
        "url": {"type": "string", "format": "uri"},
        "retrieved_at": {"type": "string", "format": "date-time"},
        "evidence_class": {
            "type": "string",
            "enum": ["VERIFIED", "CORROBORATED", "UNCORROBORATED", "INFERENCE"],
        },
        "snippet": {"type": "string", "maxLength": 1000},
        "archive_path": {"type": "string"},
    },
}

HITL_DECISION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["tier", "reviewer_id", "decision", "decided_at"],
    "properties": {
        "tier": {"type": "integer", "enum": [0, 1, 2, 3]},
        "reviewer_id": {"type": "string"},
        "decision": {"type": "string", "enum": ["approve", "revise", "reject"]},
        "decided_at": {"type": "string", "format": "date-time"},
        "rationale": {"type": "string"},
        "override": {
            "type": "object",
            "required": ["original_decision", "operator_id", "co_approver_id"],
            "properties": {
                "original_decision": {
                    "type": "string",
                    "enum": ["approve", "revise", "reject"],
                },
                "operator_id": {"type": "string"},
                "co_approver_id": {"type": "string"},
            },
        },
    },
}

AUDIT_ENTRY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["timestamp", "agent_id", "action", "target", "hash", "prev_hash"],
    "properties": {
        "timestamp": {"type": "string", "format": "date-time"},
        "agent_id": {"type": "string"},
        "action": {"type": "string"},
        "target": {"type": "string"},
        "metadata": {"type": "object"},
        "hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "prev_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
    },
}


def schema_for_artifact(artifact_type: str) -> dict[str, Any]:
    """
    Returns the JSON Schema for a given artifact_type. The base schema
    is the same across types; specific artifact types extend with their
    own required fields.
    """
    base = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["artifact_type", "artifact_version", "engagement_id", "produced_by", "produced_at"],
        "properties": {
            "artifact_type": {"type": "string"},
            "artifact_version": {"type": "string"},
            "engagement_id": {"type": "string"},
            "produced_by": {"type": "string"},
            "produced_at": {"type": "string", "format": "date-time"},
            "citations": {
                "type": "array",
                "items": CITATION_SCHEMA,
            },
            "hitl_decision": HITL_DECISION_SCHEMA,
        },
    }
    return base


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"{path}: invalid JSON: {e}"]

    artifact_type = data.get("artifact_type")
    if not artifact_type:
        return [f"{path}: missing artifact_type field"]

    schema = schema_for_artifact(artifact_type)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in validator.iter_errors(data):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"{path}: {loc}: {err.message}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Artifact path or engagement dir")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Treat path as a directory; validate all .json artifacts within.",
    )
    args = parser.parse_args()

    if args.all:
        if not args.path.is_dir():
            print(f"ERROR: --all requires a directory: {args.path}", file=sys.stderr)
            return 2
        targets = sorted(args.path.rglob("*.json"))
    else:
        targets = [args.path]

    if not targets:
        print("No artifacts to validate.", file=sys.stderr)
        return 0

    all_errors: list[str] = []
    for target in targets:
        errs = validate_file(target)
        all_errors.extend(errs)

    if all_errors:
        for e in all_errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print(f"OK: validated {len(targets)} artifact(s).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
