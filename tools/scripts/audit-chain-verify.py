#!/usr/bin/env python3
"""
audit-chain-verify.py — Verify integrity of a CADRE engagement audit chain.

Usage:
    python3 audit-chain-verify.py <chain-path>

The chain is JSONL: one entry per line. Each entry has:
    - timestamp (ISO-8601)
    - agent_id
    - action
    - target
    - metadata (optional)
    - prev_hash (sha256 hex of previous entry; "0"*64 for first entry)
    - hash (sha256 hex of canonicalized entry minus this field)

Verification checks:
    1. Each line is valid JSON.
    2. Each entry has all required fields.
    3. Each prev_hash matches the previous entry's hash.
    4. Each entry's hash matches the canonicalized recompute.
    5. Timestamps are non-decreasing.

Exit codes:
    0  Chain valid.
    1  Chain invalid (one or more checks failed).
    2  Internal error (file not found, etc.).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED = {"timestamp", "agent_id", "action", "target", "prev_hash", "hash"}
GENESIS_PREV = "0" * 64


def canonical_hash(entry: dict[str, Any]) -> str:
    """SHA-256 over canonicalized entry minus the hash field."""
    payload = {k: v for k, v in entry.items() if k != "hash"}
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def parse_iso(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def verify_chain(path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    prev_hash = GENESIS_PREV
    prev_ts: datetime | None = None
    line_count = 0

    with path.open() as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            line_count += 1

            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {line_no}: invalid JSON: {e}")
                return False, errors

            missing = REQUIRED - set(entry.keys())
            if missing:
                errors.append(f"line {line_no}: missing fields {missing}")
                return False, errors

            if entry["prev_hash"] != prev_hash:
                errors.append(
                    f"line {line_no}: prev_hash mismatch "
                    f"(expected {prev_hash}, got {entry['prev_hash']})"
                )
                return False, errors

            recomputed = canonical_hash(entry)
            if recomputed != entry["hash"]:
                errors.append(
                    f"line {line_no}: hash mismatch "
                    f"(stored {entry['hash']}, recomputed {recomputed})"
                )
                return False, errors

            ts = parse_iso(entry["timestamp"])
            if ts is None:
                errors.append(f"line {line_no}: invalid timestamp '{entry['timestamp']}'")
                return False, errors
            if prev_ts is not None and ts < prev_ts:
                errors.append(
                    f"line {line_no}: timestamp regressed "
                    f"(prev {prev_ts.isoformat()}, this {ts.isoformat()})"
                )
                return False, errors

            prev_hash = entry["hash"]
            prev_ts = ts

    if line_count == 0:
        errors.append("chain is empty")
        return False, errors

    return True, [f"OK: {line_count} entries, chain head {prev_hash[:12]}..."]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to audit-chain.jsonl")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 2

    ok, messages = verify_chain(args.path)
    for m in messages:
        print(m, file=sys.stderr if not ok else sys.stdout)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
