#!/usr/bin/env python3
"""
cost-calculator.py — Estimate engagement token cost across SKUs.

Usage:
    python3 cost-calculator.py --sku full
    python3 cost-calculator.py --sku express --tokens-actual 2.1
    python3 cost-calculator.py --custom 5.0 3.0 2.0 1.5

This is a planning tool, not an authoritative meter. The authoritative
meter is A14 Cost Meter, which reads real-time usage from the model
provider's API. This script gives operators a quick projection during
engagement scoping.

Pricing (per million tokens, USD; current as of Apr 2026):
    Opus 4.7 input:    $5.00
    Opus 4.7 output:   $25.00
    Sonnet 4.6 input:  $3.00
    Sonnet 4.6 output: $15.00
    Haiku 4.5 input:   $0.80
    Haiku 4.5 output:  $4.00

Default mix (orchestrator / subagent / audit) per cadre design:
    - 12% Opus 4.7 (orchestrator)
    - 80% Sonnet 4.6 (subagents)
    - 8%  Haiku 4.5 (A14 Cost Meter, A19 Audit Logger, frequent narrow ops)

Default I/O ratio: 70% input, 30% output.

Update prices in PRICING dict when model providers change rates. The
constants below are the single source of truth — do not duplicate
elsewhere in the framework.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Iterable

# Per-million-token prices, USD.
PRICING: dict[str, dict[str, float]] = {
    "opus-4-7":   {"input": 5.00, "output": 25.00},
    "sonnet-4-6": {"input": 3.00, "output": 15.00},
    "haiku-4-5":  {"input": 0.80, "output":  4.00},
}

DEFAULT_MIX: dict[str, float] = {
    "opus-4-7":   0.12,
    "sonnet-4-6": 0.80,
    "haiku-4-5":  0.08,
}

DEFAULT_IO_SPLIT = (0.70, 0.30)  # (input, output)

SKU_ENVELOPES_M_TOKENS: dict[str, float] = {
    "express":    2.5,
    "full":      12.0,
    "complete":  50.0,
}


@dataclass
class CostBreakdown:
    sku: str
    total_m_tokens: float
    by_model: dict[str, float]
    cost_usd: float

    def render(self) -> str:
        lines = [
            f"SKU:            {self.sku}",
            f"Total tokens:   {self.total_m_tokens:.2f}M",
            "By model:",
        ]
        for model, m_tokens in self.by_model.items():
            lines.append(f"  {model:12s} {m_tokens:5.2f}M")
        lines.append(f"Estimated cost: ${self.cost_usd:,.2f} USD")
        return "\n".join(lines)


def estimate(
    total_m_tokens: float,
    mix: dict[str, float] = None,
    io_split: tuple[float, float] = DEFAULT_IO_SPLIT,
    sku_label: str = "custom",
) -> CostBreakdown:
    mix = mix or DEFAULT_MIX
    in_share, out_share = io_split

    if abs(sum(mix.values()) - 1.0) > 0.001:
        raise ValueError(f"mix must sum to 1.0, got {sum(mix.values())}")
    if abs(in_share + out_share - 1.0) > 0.001:
        raise ValueError("io_split must sum to 1.0")

    by_model_m: dict[str, float] = {}
    total_cost = 0.0

    for model, share in mix.items():
        if model not in PRICING:
            raise ValueError(f"unknown model: {model}")
        m = total_m_tokens * share
        in_m = m * in_share
        out_m = m * out_share
        cost = in_m * PRICING[model]["input"] + out_m * PRICING[model]["output"]
        by_model_m[model] = m
        total_cost += cost

    return CostBreakdown(
        sku=sku_label,
        total_m_tokens=total_m_tokens,
        by_model=by_model_m,
        cost_usd=total_cost,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--sku", choices=list(SKU_ENVELOPES_M_TOKENS.keys()),
                   help="Use the SKU's envelope as total tokens.")
    g.add_argument("--tokens", type=float, metavar="M",
                   help="Custom total tokens in millions.")

    parser.add_argument(
        "--io-split",
        type=float, nargs=2, default=DEFAULT_IO_SPLIT,
        metavar=("INPUT", "OUTPUT"),
        help="Input/output share. Default: 0.70 0.30",
    )
    args = parser.parse_args()

    if args.sku:
        total = SKU_ENVELOPES_M_TOKENS[args.sku]
        label = args.sku
    else:
        total = args.tokens
        label = "custom"

    try:
        result = estimate(total, io_split=tuple(args.io_split), sku_label=label)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    print(result.render())
    return 0


if __name__ == "__main__":
    sys.exit(main())
