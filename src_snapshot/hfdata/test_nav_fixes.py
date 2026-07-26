"""Regression tests for the 2026-07 nav.py corrections (docs/ERRATA.md).

Covers: standard short-leg convention, exit-proxy entry floor, cohort-level
API consistency, and the sqrt(R) inflation of the flat-spread daily Sharpe.
Pure numpy; runnable from the published snapshot:

    python -m unittest src_snapshot/hfdata/test_nav_fixes.py  (from repo root)
    python test_nav_fixes.py                                  (from this dir)
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from nav import (
    event_driven_hl_cohort_returns,
    event_driven_hl_daily_returns,
    leg_open_open_return,
    planned_k_r,
    sharpe_from_daily,
    sharpe_from_period_returns,
)


class ShortLegConventionTests(unittest.TestCase):
    def test_short_gain_on_entry_notional(self) -> None:
        # price halves: standard short return on entry notional is +50%
        r = leg_open_open_return(100.0, 50.0, side="short", cost_bps=0.0)
        self.assertAlmostEqual(r, 0.5, places=12)

    def test_short_loss_full_wipeout(self) -> None:
        # price doubles: standard short return is -100% (old convex form gave -50%)
        r = leg_open_open_return(100.0, 200.0, side="short", cost_bps=0.0)
        self.assertAlmostEqual(r, -1.0, places=12)

    def test_short_is_negated_long(self) -> None:
        for exit_px in (37.5, 91.0, 100.0, 104.2, 260.0):
            long_r = leg_open_open_return(100.0, exit_px, side="long", cost_bps=0.0)
            short_r = leg_open_open_return(100.0, exit_px, side="short", cost_bps=0.0)
            self.assertAlmostEqual(short_r, -long_r, places=12)

    def test_costs_two_one_way_charges(self) -> None:
        r = leg_open_open_return(100.0, 110.0, side="long", cost_bps=10.0)
        self.assertAlmostEqual(r, 0.10 - 2.0 * 0.0010, places=12)
        r = leg_open_open_return(100.0, 90.0, side="short", cost_bps=10.0)
        self.assertAlmostEqual(r, 0.10 - 2.0 * 0.0010, places=12)

    def test_invalid_prices_are_nan(self) -> None:
        self.assertTrue(math.isnan(leg_open_open_return(0.0, 10.0, side="long", cost_bps=0.0)))
        self.assertTrue(math.isnan(leg_open_open_return(10.0, float("nan"), side="short", cost_bps=0.0)))


def _formation(sidx: int, n_names: int, scores: list[float] | None = None) -> dict:
    names = [f"S{i:02d}" for i in range(n_names)]
    sc = scores if scores is not None else [float(i) for i in range(n_names)]
    return {"session_idx": sidx, "items": list(zip(names, sc))}


def _full_price_maps(
    n_names: int,
    sessions: range,
    *,
    price: float = 100.0,
) -> tuple[dict, dict]:
    open_px: dict[tuple[str, int], float] = {}
    close_px: dict[tuple[str, int], float] = {}
    for i in range(n_names):
        for t in sessions:
            open_px[(f"S{i:02d}", t)] = price
            close_px[(f"S{i:02d}", t)] = price
    return open_px, close_px


class ExitProxyFloorTests(unittest.TestCase):
    R = 5
    SIDX = 10  # entry 11, exit 16

    def _run(self, open_px: dict, close_px: dict):
        return event_driven_hl_cohort_returns(
            formation_rows=[_formation(self.SIDX, 10)],
            open_px=open_px,
            close_px=close_px,
            horizon_R=self.R,
            cost_bps=0.0,
            min_cross=10,
        )

    def test_proxy_never_reads_before_entry(self) -> None:
        open_px, close_px = _full_price_maps(10, range(9, 17))
        top = "S09"  # highest score -> long leg (single-name decile)
        # top name: entry open exists, but no exit open and no closes at/after entry
        del open_px[(top, 16)]
        for t in range(11, 17):
            close_px.pop((top, t), None)
        # a tempting pre-entry close that the old code could have used
        close_px[(top, 10)] = 42.0
        cohorts, stats, _ = self._run(open_px, close_px)
        # leg must be unfilled -> long leg empty -> cash cohort at 0.0
        self.assertEqual(stats.n_proxy_exit, 0)
        self.assertEqual(stats.n_leg_empty, 1)
        self.assertEqual(cohorts, [(11, 16, 0.0)])

    def test_proxy_at_or_after_entry_is_used(self) -> None:
        open_px, close_px = _full_price_maps(10, range(9, 17))
        top = "S09"
        del open_px[(top, 16)]          # no exit open -> proxy path
        for t in range(12, 17):
            close_px.pop((top, t), None)
        close_px[(top, 11)] = 110.0     # last verifiable close, at entry session
        cohorts, stats, _ = self._run(open_px, close_px)
        self.assertEqual(stats.n_proxy_exit, 1)
        self.assertEqual(stats.n_leg_empty, 0)
        # long leg = 110/100-1 = +10%; short leg flat -> cohort = 0.5*10% + 0.5*0
        self.assertAlmostEqual(cohorts[0][2], 0.05, places=12)


class CohortDailyConsistencyTests(unittest.TestCase):
    def test_daily_wrapper_matches_cohorts(self) -> None:
        n, R = 10, 5
        rows = [_formation(s, n) for s in (0, R, 2 * R)]  # non-overlapping grid
        sessions = range(0, 3 * R + 2)
        open_px, close_px = _full_price_maps(n, sessions)
        # give the top name a 10% gain in cohort 2 only
        open_px[("S09", 2 * R + 1)] = 100.0
        open_px[("S09", 3 * R + 1)] = 110.0
        cohorts, _, k_r = event_driven_hl_cohort_returns(
            formation_rows=rows, open_px=open_px, close_px=close_px,
            horizon_R=R, cost_bps=0.0, min_cross=n,
        )
        daily, _, k_r2 = event_driven_hl_daily_returns(
            formation_rows=rows, open_px=open_px, close_px=close_px,
            session_idx_list=list(sessions), horizon_R=R, cost_bps=0.0, min_cross=n,
        )
        self.assertEqual(k_r, 1)
        self.assertEqual(k_r2, 1)
        self.assertEqual(len(cohorts), 3)
        self.assertAlmostEqual(sum(c[2] for c in cohorts), sum(daily.values()), places=12)

    def test_planned_kr_nonoverlapping_is_one(self) -> None:
        pairs = [(s + 1, s + 21) for s in range(0, 200, 20)]
        self.assertEqual(planned_k_r(pairs), 1)
        self.assertEqual(planned_k_r([(1, 21), (2, 22)]), 2)  # overlapping


class SharpeAnnualisationTests(unittest.TestCase):
    def test_flat_spread_inflates_by_sqrt_R(self) -> None:
        """Documents the estimator defect behind the published Study A levels."""
        rng = np.random.default_rng(7)
        R = 20
        period = rng.normal(0.01, 0.05, size=400)          # non-overlapping R-day returns
        flat = np.repeat(period / R, R)                     # the daily-spread series
        inflated = sharpe_from_daily(flat, ann_factor=252.0)
        corrected = sharpe_from_period_returns(period, R)
        self.assertGreater(corrected, 0.0)
        self.assertAlmostEqual(inflated / corrected, math.sqrt(R), delta=0.05 * math.sqrt(R))

    def test_period_sharpe_matches_direct_formula(self) -> None:
        period = [0.02, -0.01, 0.03, 0.00, 0.015, -0.005]
        R = 20
        x = np.asarray(period)
        expect = math.sqrt(252.0 / R) * x.mean() / x.std(ddof=1)
        self.assertAlmostEqual(sharpe_from_period_returns(period, R), expect, places=12)

    def test_crypto_calendar_variant(self) -> None:
        period = [0.02, -0.01, 0.03, 0.00, 0.015, -0.005]
        x = np.asarray(period)
        expect = math.sqrt(365.0 / 20.0) * x.mean() / x.std(ddof=1)
        got = sharpe_from_period_returns(period, 20, trading_days_per_year=365.0)
        self.assertAlmostEqual(got, expect, places=12)

    def test_rejects_bad_horizon(self) -> None:
        with self.assertRaises(ValueError):
            sharpe_from_period_returns([0.01, 0.02, 0.03], 0)


if __name__ == "__main__":
    unittest.main()
