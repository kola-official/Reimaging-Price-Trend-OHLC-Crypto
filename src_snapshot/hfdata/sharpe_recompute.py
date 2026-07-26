#!/usr/bin/env python3
"""Compare Sharpe annualisation paths on cohort period returns (docs/ERRATA.md).

Reads non-overlapping per-cohort net returns and reports, side by side:

1. published-style estimator: each cohort return spread flat over its R
   holding sessions, Sharpe on the resulting series with sqrt(252);
2. corrected estimator: Sharpe on the period returns with sqrt(252/R);
3. the implied inflation ratio (~sqrt(R * coverage) on the grid).

Input CSV needs a ``net_return`` column; ``entry``/``exit`` session columns are
optional (used only for coverage/K_R accounting). Example:

    python sharpe_recompute.py cohorts_i20_r20.csv --horizon 20 --sessions 5796

Export the cohort returns on the experiment host via
``nav.event_driven_hl_cohort_returns`` — one row per cohort.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from nav import sharpe_from_daily, sharpe_from_period_returns


def load_cohorts(path: Path) -> tuple[list[float], list[tuple[int, int]]]:
    rets: list[float] = []
    spans: list[tuple[int, int]] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "net_return" not in reader.fieldnames:
            raise SystemExit("input CSV must have a net_return column")
        has_span = {"entry", "exit"}.issubset(set(reader.fieldnames))
        for row in reader:
            rets.append(float(row["net_return"]))
            if has_span:
                spans.append((int(row["entry"]), int(row["exit"])))
    if not rets:
        raise SystemExit("no cohort rows found")
    return rets, spans


def flat_spread_series(rets: list[float], horizon_r: int) -> np.ndarray:
    """Reconstruct the published-style daily series (contiguous blocks)."""
    return np.repeat(np.asarray(rets, dtype=float) / horizon_r, horizon_r)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cohort_csv", type=Path)
    parser.add_argument("--horizon", type=int, required=True, help="holding horizon R in sessions")
    parser.add_argument(
        "--trading-days",
        type=float,
        default=252.0,
        help="trading days per year (252 equities, 365 crypto calendar)",
    )
    parser.add_argument(
        "--sessions",
        type=int,
        default=None,
        help="total OOS sessions, for coverage fraction f = n_cohorts*R/sessions",
    )
    args = parser.parse_args()

    rets, spans = load_cohorts(args.cohort_csv)
    r_ = args.horizon
    flat = flat_spread_series(rets, r_)
    if args.sessions and args.sessions > flat.size:
        # replicate the published pipeline's zero (cash) sessions outside cohorts
        flat = np.concatenate([flat, np.zeros(args.sessions - flat.size)])

    published_style = sharpe_from_daily(flat, ann_factor=args.trading_days)
    corrected = sharpe_from_period_returns(rets, r_, trading_days_per_year=args.trading_days)
    nonzero = [x for x in rets if x != 0.0]
    corrected_ex_cash = (
        sharpe_from_period_returns(nonzero, r_, trading_days_per_year=args.trading_days)
        if len(nonzero) >= 3
        else float("nan")
    )

    print(f"cohorts:                {len(rets)} (zero/cash: {len(rets) - len(nonzero)})")
    print(f"horizon R:              {r_}")
    if args.sessions:
        f = len(rets) * r_ / args.sessions
        print(f"coverage f:             {f:.3f} (n*R/sessions)")
        print(f"sqrt(R*f) prediction:   {math.sqrt(r_ * f):.3f}")
    print(f"published-style Sharpe: {published_style:.4f}   [flat-spread daily, sqrt({args.trading_days:.0f})]")
    print(f"corrected Sharpe:       {corrected:.4f}   [period returns, sqrt({args.trading_days:.0f}/R)]")
    print(f"corrected ex-cash:      {corrected_ex_cash:.4f}   [zero-return cohorts dropped]")
    if corrected not in (0.0,) and math.isfinite(corrected) and corrected != 0:
        print(f"inflation ratio:        {published_style / corrected:.3f}")
    if spans:
        holds = [b - a for a, b in spans]
        if any(h != r_ for h in holds):
            print(f"WARNING: {sum(1 for h in holds if h != r_)} cohorts have span != R")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
