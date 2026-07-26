"""Descriptive OOS metrics used in the crypto nine-cell audit.

Rank IC = mean cross-sectional Spearman between ensemble up-probability and
forward close-to-close return. LS Sharpe is a **proxy** from equal-weight
top-minus-bottom decile period returns, annualised with sqrt(365/R), **without**
delayed-VWAP fills or transaction costs. Prefer Rank IC / ICIR for ranking skill;
treat LS Sharpe as economic illustration only.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Iterable

import numpy as np


def _rankdata(a: np.ndarray) -> np.ndarray:
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=np.float64)
    ranks[order] = np.arange(1, len(a) + 1, dtype=np.float64)
    sorted_a = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sorted_a[j + 1] == sorted_a[i]:
            j += 1
        if j > i:
            avg = 0.5 * (i + 1 + j + 1)
            ranks[order[i : j + 1]] = avg
        i = j + 1
    return ranks


def spearman_ic(scores: np.ndarray, rets: np.ndarray) -> float:
    """Spearman correlation; NaN when either side is constant.

    (Previously a +1e-12 fudge made constant inputs yield ~0.0 while the pure
    implementation in ``transfer_metrics.spearman_ic`` yields NaN; the two
    now share NaN semantics. Degenerate dates are skipped and counted by
    ``summarise_by_date``.)
    """
    if len(scores) < 3:
        return float("nan")
    rs = _rankdata(scores)
    rr = _rankdata(rets)
    ss = float(rs.std(ddof=0))
    sr = float(rr.std(ddof=0))
    if ss <= 0.0 or sr <= 0.0:
        return float("nan")
    rs = (rs - rs.mean()) / ss
    rr = (rr - rr.mean()) / sr
    return float(np.mean(rs * rr))


def decile_long_short(scores: np.ndarray, rets: np.ndarray, n: int = 10) -> float:
    if len(scores) < n:
        return float("nan")
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores), dtype=np.int64)
    ranks[order] = np.arange(len(scores))
    qs = np.clip(np.floor(ranks * n / len(scores)).astype(int), 0, n - 1)
    high = rets[qs == n - 1].mean() if np.any(qs == n - 1) else float("nan")
    low = rets[qs == 0].mean() if np.any(qs == 0) else float("nan")
    return float(high - low)


def summarise_by_date(
    scores: np.ndarray,
    rets: np.ndarray,
    dates: Iterable[str],
    horizon_r: int,
    min_names: int = 10,
) -> dict[str, float]:
    by_date: dict[str, list[int]] = defaultdict(list)
    for i, d in enumerate(dates):
        by_date[d].append(i)
    ics: list[float] = []
    ls: list[float] = []
    n_skipped_nan = 0
    for d, idxs in sorted(by_date.items()):
        idxs_a = np.asarray(idxs)
        if len(idxs_a) < min_names:
            continue
        ic = spearman_ic(scores[idxs_a], rets[idxs_a])
        if math.isnan(ic):
            # degenerate cross-section (e.g. constant scores) — skip, but count
            n_skipped_nan += 1
            continue
        ics.append(ic)
        ls.append(decile_long_short(scores[idxs_a], rets[idxs_a]))
    ics_a = np.asarray(ics, dtype=np.float64)
    ls_a = np.asarray(ls, dtype=np.float64)
    mean_ic = float(np.nanmean(ics_a)) if len(ics_a) else float("nan")
    std_ic = float(np.nanstd(ics_a, ddof=1)) if len(ics_a) > 1 else float("nan")
    icir = mean_ic / std_ic if std_ic and not math.isnan(std_ic) and std_ic > 0 else float("nan")
    mean_ls = float(np.nanmean(ls_a)) if len(ls_a) else float("nan")
    std_ls = float(np.nanstd(ls_a, ddof=1)) if len(ls_a) > 1 else float("nan")
    sharpe = (
        (mean_ls / std_ls) * math.sqrt(365.0 / horizon_r)
        if std_ls and std_ls > 0
        else float("nan")
    )
    # NAV/MaxDD proxy: NaN LS periods are compounded as 0 (cash), consistent
    # with the ls_sharpe proxy framing in the module docstring.
    nav = np.cumprod(1.0 + np.nan_to_num(ls_a, nan=0.0))
    peak = np.maximum.accumulate(nav) if len(nav) else np.array([1.0])
    dd = (nav / peak - 1.0) if len(nav) else np.array([0.0])
    return {
        "n_ic_dates": float(len(ics)),
        "n_ic_dates_skipped_nan": float(n_skipped_nan),
        "rank_ic_mean": mean_ic,
        "rank_ic_std": std_ic,
        "icir": icir,
        "ls_mean": mean_ls,
        "ls_std": std_ls,
        "ls_sharpe_ann_proxy": sharpe,
        "ls_maxdd": float(dd.min()) if len(dd) else float("nan"),
    }
