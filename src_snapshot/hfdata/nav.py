"""Independent slot NAV accounting and event-driven H–L path (plan §8.2 / §4.5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence

import numpy as np


@dataclass
class SlotState:
    cash: float
    long_shares: dict[str, float] = field(default_factory=dict)  # instrument -> n
    short_shares: dict[str, float] = field(default_factory=dict)  # instrument -> m >= 0
    occupied_until_exit: bool = False
    exit_session_id: int | None = None

    def long_mtm(self, prices: dict[str, float]) -> float:
        return sum(n * prices[i] for i, n in self.long_shares.items() if i in prices)

    def short_liability(self, prices: dict[str, float]) -> float:
        return sum(m * prices[i] for i, m in self.short_shares.items() if i in prices)

    def nav(self, prices: dict[str, float]) -> float:
        return self.cash + self.long_mtm(prices) - self.short_liability(prices)


def planned_k_r(entry_exit_pairs: list[tuple[int, int]]) -> int:
    """K_R from planned [entry, exit) intervals; exit-before-entry at same t."""
    if not entry_exit_pairs:
        return 1
    events: list[tuple[int, int, int]] = []  # (t, order, delta) order 0=exit first
    for i, (entry, exit_) in enumerate(entry_exit_pairs):
        if exit_ <= entry:
            raise ValueError(f"invalid interval [{entry}, {exit_})")
        events.append((exit_, 0, -1))  # exit first
        events.append((entry, 1, +1))
    events.sort()
    active = 0
    peak = 0
    for _t, _ord, delta in events:
        active += delta
        peak = max(peak, active)
    return max(peak, 1)


def gross_pnl_fixed_shares(
    long_shares: dict[str, float],
    short_shares: dict[str, float],
    prices_prev: dict[str, float],
    prices_now: dict[str, float],
) -> float:
    pnl = 0.0
    for i, n in long_shares.items():
        if i in prices_prev and i in prices_now:
            pnl += n * (prices_now[i] - prices_prev[i])
    for i, m in short_shares.items():
        if i in prices_prev and i in prices_now:
            pnl -= m * (prices_now[i] - prices_prev[i])
    return pnl


def apply_cost(nav_prev: float, gross_pnl: float, traded_notional: float, cost_bps: float) -> tuple[float, float, float]:
    """Return (nav_now, cost_dollars, net_return)."""
    c = cost_bps * 1e-4
    cost = c * traded_notional
    nav_now = nav_prev + gross_pnl - cost
    if nav_prev <= 0:
        raise ValueError("non-positive prior NAV")
    r_gross = gross_pnl / nav_prev
    cost_rate = cost / nav_prev
    return nav_now, cost, r_gross - cost_rate


def leg_open_open_return(
    entry_open: float,
    exit_price: float,
    *,
    side: str,
    cost_bps: float,
) -> float:
    """One-leg net return with one-way cost on entry and exit notional.

    Short-leg convention: return on entry notional, ``-(exit/entry - 1)``.
    (A previous revision used ``entry/exit - 1``, which is convex in the price
    move and by AM-GM never smaller than the standard convention — it
    systematically overstated short-leg profits and understated short-leg
    losses, inflating H-L returns. Fixed 2026-07; see docs/ERRATA.md.)
    """
    if entry_open <= 0 or exit_price <= 0 or not np.isfinite(entry_open) or not np.isfinite(exit_price):
        return float("nan")
    c = cost_bps * 1e-4
    if side == "long":
        gross = exit_price / entry_open - 1.0
    elif side == "short":
        gross = -(exit_price / entry_open - 1.0)
    else:
        raise ValueError(side)
    # two one-way costs (entry + exit) on unit notional
    return float(gross - 2.0 * c)


@dataclass
class ExitProxyStats:
    n_attempted_entries: int = 0
    n_exact_entry: int = 0
    n_entry_unfilled: int = 0
    n_exact_exit: int = 0
    n_proxy_exit: int = 0
    n_leg_empty: int = 0
    n_cohorts: int = 0
    n_formable: int = 0

    def as_dict(self) -> dict:
        att = max(self.n_attempted_entries, 1)
        return {
            "n_cohorts": self.n_cohorts,
            "n_formable": self.n_formable,
            "n_leg_empty": self.n_leg_empty,
            "n_attempted_entries": self.n_attempted_entries,
            "exact_entry_fill_rate": self.n_exact_entry / att,
            "entry_unfilled_rate": self.n_entry_unfilled / att,
            "n_exact_exit": self.n_exact_exit,
            "n_proxy_exit": self.n_proxy_exit,
            "proxy_exit_share": self.n_proxy_exit / max(self.n_exact_exit + self.n_proxy_exit, 1),
            "endpoint": "next_open_exec_with_frozen_exit_proxy",
            "primary_cost_bps": 10,
        }


def decile_hl_masks(scores: np.ndarray, min_cross: int = 100) -> tuple[np.ndarray | None, np.ndarray | None]:
    """Return boolean masks for high (Q10) and low (Q1) deciles; None if not formable."""
    n = int(scores.size)
    if n < min_cross:
        return None, None
    order = np.argsort(scores, kind="mergesort")
    n_bucket = n // 10
    if n_bucket < 1:
        return None, None
    low_idx = order[:n_bucket]
    high_idx = order[-n_bucket:]
    low = np.zeros(n, dtype=bool)
    high = np.zeros(n, dtype=bool)
    low[low_idx] = True
    high[high_idx] = True
    return high, low


def event_driven_hl_cohort_returns(
    *,
    formation_rows: Sequence[dict],
    open_px: Mapping[tuple[str, int], float],
    close_px: Mapping[tuple[str, int], float],
    horizon_R: int,
    cost_bps: float = 10.0,
    min_cross: int = 100,
) -> tuple[list[tuple[int, int, float]], ExitProxyStats, int]:
    """Per-cohort EW H–L net returns for the next-open path.

    formation_rows: each dict has chart session_idx, list of (instrument, score)
    open_px/close_px: (instrument, session_idx) -> price

    Returns (cohorts, stats, k_r); each cohort is (entry_session, exit_session,
    net_return) for the holding window [entry, exit). Formable cohorts with an
    empty leg contribute 0.0 (cash slot). On the non-overlapping formation grid
    these period returns are the primary quantity for performance statistics:
    annualise Sharpe with ``sharpe_from_period_returns`` (factor sqrt(252/R)),
    not from the flat-spread daily series (docs/ERRATA.md).
    """
    stats = ExitProxyStats()
    if not formation_rows:
        return [], stats, 1

    # planned K_R
    pairs = []
    for fr in formation_rows:
        sidx = int(fr["session_idx"])
        pairs.append((sidx + 1, sidx + horizon_R + 1))
    k_r = planned_k_r(pairs)

    # cohort net returns keyed by (entry, exit)
    cohorts: list[tuple[int, int, float]] = []
    for fr in formation_rows:
        stats.n_cohorts += 1
        sidx = int(fr["session_idx"])
        entry = sidx + 1
        exit_ = sidx + horizon_R + 1
        inst_scores: list[tuple[str, float]] = fr["items"]
        if len(inst_scores) < min_cross:
            continue
        insts = [x[0] for x in inst_scores]
        scores = np.array([x[1] for x in inst_scores], dtype=float)
        hi, lo = decile_hl_masks(scores, min_cross=min_cross)
        if hi is None:
            continue
        stats.n_formable += 1

        def leg_returns(mask: np.ndarray, side: str) -> list[float]:
            rets = []
            for i, flag in enumerate(mask):
                if not flag:
                    continue
                inst = insts[i]
                stats.n_attempted_entries += 1
                eo = open_px.get((inst, entry))
                if eo is None or not np.isfinite(eo) or eo <= 0:
                    stats.n_entry_unfilled += 1
                    continue
                stats.n_exact_entry += 1
                xo = open_px.get((inst, exit_))
                if xo is not None and np.isfinite(xo) and xo > 0:
                    stats.n_exact_exit += 1
                    xp = float(xo)
                else:
                    # frozen exit proxy: last verifiable close in [entry, exit_].
                    # Never look back past the entry session: a close taken
                    # before entry would mark the leg over a window it never
                    # held (fabricated return). If no close exists at or after
                    # entry, the leg is treated as unfilled instead.
                    xp = None
                    for t in range(exit_, entry - 1, -1):
                        c = close_px.get((inst, t))
                        if c is not None and np.isfinite(c) and c > 0:
                            xp = float(c)
                            break
                    if xp is None:
                        stats.n_entry_unfilled += 1  # cannot mark; treat as failed leg
                        continue
                    stats.n_proxy_exit += 1
                r = leg_open_open_return(float(eo), xp, side=side, cost_bps=cost_bps)
                if np.isfinite(r):
                    rets.append(r)
            return rets

        h_rets = leg_returns(hi, "long")
        l_rets = leg_returns(lo, "short")
        if not h_rets or not l_rets:
            stats.n_leg_empty += 1
            # entry_leg_empty: cash slot still occupies [entry, exit) with 0 return
            cohorts.append((entry, exit_, 0.0))
            continue
        # Long 50% H / short 50% L; short-leg returns already side-signed.
        cohort_r = 0.5 * float(np.mean(h_rets)) + 0.5 * float(np.mean(l_rets))
        cohorts.append((entry, exit_, cohort_r))

    return cohorts, stats, k_r


def event_driven_hl_daily_returns(
    *,
    formation_rows: Sequence[dict],
    open_px: Mapping[tuple[str, int], float],
    close_px: Mapping[tuple[str, int], float],
    session_idx_list: Sequence[int],
    horizon_R: int,
    cost_bps: float = 10.0,
    min_cross: int = 100,
) -> tuple[dict[int, float], ExitProxyStats, int]:
    """Flat-spread session series for NAV-style paths — NOT a Sharpe input.

    session_idx_list: sorted full calendar session indices covering OOS.
    Each formable cohort contributes its whole-period net return spread evenly
    over sessions in [entry, exit), stacked with weight 1/K_R where K_R is from
    planned intervals (plan §8.2).

    WARNING (docs/ERRATA.md): on the non-overlapping formation grid (K_R = 1)
    this series is piecewise constant over R-session blocks. Its per-session
    volatility understates mark-to-market volatility by roughly sqrt(R), so
    feeding it to ``sharpe_from_daily`` with ann_factor=252 overstates the
    annualised Sharpe by roughly sqrt(R) (≈4.5x at R=20, ≈7.7x at R=60). Use
    ``event_driven_hl_cohort_returns`` + ``sharpe_from_period_returns`` for
    Sharpe statistics; keep this series for NAV plotting and slot accounting.
    """
    if not formation_rows:
        return {}, ExitProxyStats(), 1
    cohorts, stats, k_r = event_driven_hl_cohort_returns(
        formation_rows=formation_rows,
        open_px=open_px,
        close_px=close_px,
        horizon_R=horizon_R,
        cost_bps=cost_bps,
        min_cross=min_cross,
    )
    # Spread each cohort return evenly over holding sessions; stack with 1/K_R
    daily: dict[int, float] = {int(t): 0.0 for t in session_idx_list}
    hold = max(horizon_R, 1)
    for entry, exit_, cohort_r in cohorts:
        per_day = cohort_r / hold
        w = 1.0 / float(k_r)
        for t in range(entry, exit_):
            if t in daily:
                daily[t] = daily[t] + w * per_day
    return daily, stats, k_r


def sharpe_from_daily(returns: Iterable[float], ann_factor: float = 252.0) -> float:
    """Sharpe = sqrt(ann_factor) * mean/std of the series passed in.

    ``ann_factor`` must equal the number of observations per year for that
    series: 252 for genuine daily marks, 252/R for non-overlapping R-session
    period returns. Do NOT pass the flat-spread series from
    ``event_driven_hl_daily_returns`` with ann_factor=252 — that combination
    overstates Sharpe by ~sqrt(R) (docs/ERRATA.md).
    """
    x = np.asarray(list(returns), dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 3:
        return float("nan")
    sd = float(x.std(ddof=1))
    if sd <= 0:
        return float("nan")
    return float(np.sqrt(ann_factor) * x.mean() / sd)


def sharpe_from_period_returns(
    returns: Iterable[float],
    horizon_R: int,
    *,
    trading_days_per_year: float = 252.0,
) -> float:
    """Annualised Sharpe from non-overlapping R-session period returns.

    Uses ann_factor = trading_days_per_year / R, i.e. sqrt(252/R) annualisation
    on the equity calendar — the period-return analogue of the crypto path in
    ``src_snapshot/crypto/metrics_oos.py`` (sqrt(365/R)). This is the corrected
    headline estimator for the Study A economic path (docs/ERRATA.md).
    """
    if horizon_R <= 0:
        raise ValueError("horizon_R must be positive")
    return sharpe_from_daily(returns, ann_factor=trading_days_per_year / float(horizon_R))
