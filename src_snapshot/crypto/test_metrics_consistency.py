"""Consistency tests for the two Rank IC implementations (docs/ERRATA.md).

The numpy path (metrics_oos) and the pure-Python path (transfer_metrics) must
agree numerically and share NaN semantics for degenerate cross-sections.
Runnable from the published snapshot:

    python -m unittest src_snapshot/crypto/test_metrics_consistency.py
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

import metrics_oos
import transfer_metrics


class SpearmanConsistencyTests(unittest.TestCase):
    def test_agreement_on_random_data(self) -> None:
        rng = np.random.default_rng(11)
        for n in (10, 50, 200):
            s = rng.normal(size=n)
            r = rng.normal(size=n)
            a = metrics_oos.spearman_ic(s, r)
            b = transfer_metrics.spearman_ic(list(s), list(r))
            self.assertAlmostEqual(a, b, places=10)

    def test_agreement_with_ties(self) -> None:
        s = np.array([1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0])
        r = np.array([0.1, -0.2, 0.1, 0.4, 0.4, -0.1, 0.0, 0.3])
        a = metrics_oos.spearman_ic(s, r)
        b = transfer_metrics.spearman_ic(list(s), list(r))
        self.assertAlmostEqual(a, b, places=10)

    def test_constant_scores_nan_in_both(self) -> None:
        s = [1.0] * 20
        r = list(np.random.default_rng(3).normal(size=20))
        self.assertTrue(math.isnan(metrics_oos.spearman_ic(np.asarray(s), np.asarray(r))))
        self.assertTrue(math.isnan(transfer_metrics.spearman_ic(s, r)))

    def test_perfect_and_inverse(self) -> None:
        s = np.arange(10.0)
        self.assertAlmostEqual(metrics_oos.spearman_ic(s, s), 1.0, places=10)
        self.assertAlmostEqual(metrics_oos.spearman_ic(s, -s), -1.0, places=10)


class DecileConsistencyTests(unittest.TestCase):
    def test_agreement_on_random_data(self) -> None:
        rng = np.random.default_rng(5)
        for n in (10, 53, 200):
            s = rng.normal(size=n)
            r = rng.normal(size=n)
            a = metrics_oos.decile_long_short(s, r)
            b = transfer_metrics.decile_long_short(list(s), list(r))
            self.assertAlmostEqual(a, b, places=10)


class SummariseNanHandlingTests(unittest.TestCase):
    def _mixed_dates(self):
        rng = np.random.default_rng(9)
        scores, rets, dates = [], [], []
        # date A: degenerate (constant scores) -> NaN IC, must be skipped+counted
        scores += [0.5] * 12
        rets += list(rng.normal(size=12))
        dates += ["2024-01-01"] * 12
        # dates B, C: informative
        for d in ("2024-01-21", "2024-02-10"):
            s = list(rng.normal(size=12))
            scores += s
            rets += [x + rng.normal(scale=0.1) for x in s]
            dates += [d] * 12
        return scores, rets, dates

    def test_pure_path_skips_and_counts_nan_dates(self) -> None:
        scores, rets, dates = self._mixed_dates()
        out = transfer_metrics.summarise_rank_ic_by_date(scores, rets, dates, 20, min_names=10)
        self.assertEqual(out["n_ic_dates"], 2.0)
        self.assertEqual(out["n_ic_dates_skipped_nan"], 1.0)
        self.assertFalse(math.isnan(out["rank_ic_mean"]))
        self.assertGreater(out["rank_ic_mean"], 0.0)

    def test_numpy_path_matches(self) -> None:
        scores, rets, dates = self._mixed_dates()
        out_np = metrics_oos.summarise_by_date(
            np.asarray(scores), np.asarray(rets), dates, 20, min_names=10
        )
        out_py = transfer_metrics.summarise_rank_ic_by_date(scores, rets, dates, 20, min_names=10)
        self.assertEqual(out_np["n_ic_dates"], out_py["n_ic_dates"])
        self.assertEqual(out_np["n_ic_dates_skipped_nan"], out_py["n_ic_dates_skipped_nan"])
        self.assertAlmostEqual(out_np["rank_ic_mean"], out_py["rank_ic_mean"], places=10)
        self.assertAlmostEqual(out_np["ls_sharpe_ann_proxy"], out_py["ls_sharpe_ann_proxy"], places=10)

    def test_all_degenerate_returns_empty_summary(self) -> None:
        scores = [1.0] * 15
        rets = list(np.random.default_rng(1).normal(size=15))
        dates = ["2024-03-01"] * 15
        out = transfer_metrics.summarise_rank_ic_by_date(scores, rets, dates, 20, min_names=10)
        self.assertEqual(out["n_ic_dates"], 0.0)
        self.assertEqual(out["n_ic_dates_skipped_nan"], 1.0)
        self.assertTrue(math.isnan(out["rank_ic_mean"]))

    def test_min_names_threshold_respected(self) -> None:
        rng = np.random.default_rng(2)
        s = list(rng.normal(size=30))
        r = list(rng.normal(size=30))
        d = ["2024-04-01"] * 30
        out_50 = transfer_metrics.summarise_rank_ic_by_date(s, r, d, 20, min_names=50)
        self.assertEqual(out_50["n_ic_dates"], 0.0)
        out_10 = transfer_metrics.summarise_rank_ic_by_date(s, r, d, 20, min_names=10)
        self.assertEqual(out_10["n_ic_dates"], 1.0)


if __name__ == "__main__":
    unittest.main()
