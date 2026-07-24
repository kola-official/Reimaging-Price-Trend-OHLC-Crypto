"""Delayed execution windows, tradability, costs, and decile helpers.

No formal OOS portfolio evaluation lives here. Functions are pure accounting
and leakage guards for D2 tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Iterable, Sequence


UTC = timezone.utc
DEFAULT_ENTRY_WINDOW = (time(0, 5), time(0, 10))


def parse_hhmm_window(spec: str) -> tuple[time, time]:
    """Parse 'HH:MM-HH:MM' in UTC clock minutes."""
    left, right = spec.split("-")
    sh, sm = (int(part) for part in left.split(":"))
    eh, em = (int(part) for part in right.split(":"))
    start = time(sh, sm)
    end = time(eh, em)
    if (eh, em) <= (sh, sm):
        raise ValueError(f"execution window must be forward within one day: {spec}")
    return start, end


def chart_day_interval_utc(chart_date: date) -> tuple[datetime, datetime]:
    """Image day t is [00:00, 24:00) UTC — half-open."""
    start = datetime(chart_date.year, chart_date.month, chart_date.day, tzinfo=UTC)
    end = start + timedelta(days=1)
    return start, end


def entry_exit_dates(chart_date: date, horizon_r: int) -> tuple[date, date]:
    if horizon_r <= 0:
        raise ValueError("horizon_r must be positive")
    entry = chart_date + timedelta(days=1)
    exit_ = chart_date + timedelta(days=horizon_r + 1)
    return entry, exit_


def holding_hours(horizon_r: int) -> int:
    if horizon_r <= 0:
        raise ValueError("horizon_r must be positive")
    return horizon_r * 24


def execution_window_bounds(
    day: date,
    window: tuple[time, time] = DEFAULT_ENTRY_WINDOW,
) -> tuple[datetime, datetime]:
    start_t, end_t = window
    start = datetime(day.year, day.month, day.day, start_t.hour, start_t.minute, tzinfo=UTC)
    end = datetime(day.year, day.month, day.day, end_t.hour, end_t.minute, tzinfo=UTC)
    return start, end


def entry_window_after_chart_close(
    chart_date: date,
    window: tuple[time, time] = DEFAULT_ENTRY_WINDOW,
) -> bool:
    """Primary leakage guard: entry window must start strictly after chart day end."""
    _, chart_end = chart_day_interval_utc(chart_date)
    entry_day, _ = entry_exit_dates(chart_date, horizon_r=1)
    entry_start, _ = execution_window_bounds(entry_day, window)
    return entry_start >= chart_end


def exact_holding_respected(chart_date: date, horizon_r: int) -> bool:
    entry, exit_ = entry_exit_dates(chart_date, horizon_r)
    entry_start, _ = execution_window_bounds(entry)
    exit_start, _ = execution_window_bounds(exit_)
    return (exit_start - entry_start) == timedelta(hours=holding_hours(horizon_r))


def oos_tail_formation_valid(
    chart_date: date,
    horizon_r: int,
    oos_end: date,
) -> bool:
    """Drop formation if exit date is after inclusive OOS end calendar day."""
    _, exit_day = entry_exit_dates(chart_date, horizon_r)
    return exit_day <= oos_end


@dataclass(frozen=True)
class MinuteBar:
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    quote_volume: float = 0.0


def minute_in_window(open_time_ms: int, window_start: datetime, window_end: datetime) -> bool:
    ts = datetime.fromtimestamp(open_time_ms / 1000.0, tz=UTC)
    return window_start <= ts < window_end


def vwap_from_minute_bars(
    bars: Sequence[MinuteBar],
    window_start: datetime,
    window_end: datetime,
    *,
    use_quote_volume: bool = True,
) -> float | None:
    """Return VWAP over bars in [start, end). None if not tradable."""
    notional = 0.0
    base = 0.0
    for bar in bars:
        if not minute_in_window(bar.open_time_ms, window_start, window_end):
            continue
        if bar.volume <= 0:
            continue
        if use_quote_volume and bar.quote_volume > 0:
            notional += bar.quote_volume
            base += bar.volume
        else:
            # typical quote_vol proxy = typical price * base volume
            typical = (bar.high + bar.low + bar.close) / 3.0
            notional += typical * bar.volume
            base += bar.volume
    if base <= 0 or notional <= 0:
        return None
    return notional / base


def is_tradable_execution_price(price: float | None) -> bool:
    return price is not None and price > 0 and price == price  # not NaN


def reject_close_fill_when_missing(
    execution_price: float | None,
    close_price: float,
) -> float | None:
    """Protocol: never fall back to close when the execution window is empty."""
    if is_tradable_execution_price(execution_price):
        return execution_price
    _ = close_price  # explicitly unused
    return None


def turnover_cost(
    previous_weights: dict[str, float],
    target_weights: dict[str, float],
    *,
    one_way_cost_bps: float,
) -> float:
    """Cost = one_way_bps * sum |Δw| over instruments (absolute traded notional fraction)."""
    keys = set(previous_weights) | set(target_weights)
    traded = 0.0
    for key in keys:
        traded += abs(target_weights.get(key, 0.0) - previous_weights.get(key, 0.0))
    return traded * (one_way_cost_bps / 10_000.0)


def apply_costs_to_gross_return(gross_return: float, cost_fraction: float) -> float:
    return gross_return - cost_fraction


def factor_spread(r_high: float, r_low: float) -> float:
    return r_high - r_low


def gross1_execution_return(r_high: float, r_low: float) -> float:
    """Total gross exposure 1, net 0: 0.5 long high, 0.5 short low."""
    return 0.5 * r_high - 0.5 * r_low


def assign_deciles(
    scores: Sequence[float],
    instrument_ids: Sequence[str],
    *,
    n_quantiles: int = 10,
) -> list[int]:
    """Return 1..n_quantiles labels; 10 = highest score.

    Stable order: score ascending, then instrument_id ascending. Ties broken by id
    so groups are deterministic. Uses as-equal-as-possible counts.
    """
    if len(scores) != len(instrument_ids):
        raise ValueError("scores and instrument_ids length mismatch")
    if n_quantiles <= 0:
        raise ValueError("n_quantiles must be positive")
    if len(scores) < n_quantiles:
        raise ValueError("need at least n_quantiles names for deciles")

    order = sorted(
        range(len(scores)),
        key=lambda index: (float(scores[index]), str(instrument_ids[index])),
    )
    labels = [0] * len(scores)
    count = len(scores)
    for rank, index in enumerate(order):
        # floor division into n groups by rank position
        quantile = min(n_quantiles, rank * n_quantiles // count + 1)
        labels[index] = quantile
    return labels


def decile_mean_returns(
    labels: Sequence[int],
    returns: Sequence[float],
    *,
    n_quantiles: int = 10,
) -> dict[int, float]:
    buckets: dict[int, list[float]] = {q: [] for q in range(1, n_quantiles + 1)}
    for label, ret in zip(labels, returns, strict=True):
        buckets[int(label)].append(float(ret))
    means: dict[int, float] = {}
    for q, values in buckets.items():
        if not values:
            raise ValueError(f"empty decile {q}")
        means[q] = sum(values) / len(values)
    return means


def synthetic_deciles_are_monotonic(n_names: int = 50) -> bool:
    """Negative control helper: monotone scores must map to monotone decile means."""
    scores = [float(i) for i in range(n_names)]
    ids = [f"S{i:03d}" for i in range(n_names)]
    # realized return equals score so ranking quality is perfect
    returns = list(scores)
    labels = assign_deciles(scores, ids, n_quantiles=10)
    means = decile_mean_returns(labels, returns, n_quantiles=10)
    ordered = [means[q] for q in range(1, 11)]
    return all(ordered[i] < ordered[i + 1] for i in range(9))


def build_execution_audit_payload() -> dict[str, Any]:
    """Deterministic self-audit used by scripts/audit_execution_leakage.py."""
    chart = date(2021, 6, 1)
    horizon = 20
    entry, exit_ = entry_exit_dates(chart, horizon)
    window = DEFAULT_ENTRY_WINDOW
    chart_start, chart_end = chart_day_interval_utc(chart)
    entry_start, entry_end = execution_window_bounds(entry, window)
    exit_start, exit_end = execution_window_bounds(exit_, window)

    # synthetic minutes: one bar with volume, one empty window case
    entry_ms = int(entry_start.timestamp() * 1000)
    good_bars = [
        MinuteBar(entry_ms, 10, 11, 9, 10.5, volume=2.0, quote_volume=21.0),
        MinuteBar(entry_ms + 60_000, 10.5, 10.6, 10.4, 10.55, volume=3.0, quote_volume=31.5),
    ]
    vwap_ok = vwap_from_minute_bars(good_bars, entry_start, entry_end)
    vwap_empty = vwap_from_minute_bars([], entry_start, entry_end)
    close_fill = reject_close_fill_when_missing(vwap_empty, close_price=10.0)

    prev_w = {"A": 0.5, "B": 0.5}
    next_w = {"A": 0.0, "B": 1.0}
    cost = turnover_cost(prev_w, next_w, one_way_cost_bps=10)

    checks = {
        "entry_after_chart_close": entry_window_after_chart_close(chart, window),
        "exact_holding_hours": exact_holding_respected(chart, horizon),
        "holding_hours_formula": holding_hours(horizon) == 20 * 24,
        "entry_exit_dates": entry == date(2021, 6, 2) and exit_ == date(2021, 6, 22),
        "chart_end_equals_next_midnight": chart_end == datetime(2021, 6, 2, tzinfo=UTC),
        "entry_start_is_00_05": entry_start.time() == time(0, 5),
        "entry_end_is_00_10": entry_end.time() == time(0, 10),
        "exit_window_aligned": exit_start.time() == time(0, 5) and exit_end.time() == time(0, 10),
        "vwap_tradable_when_volume": is_tradable_execution_price(vwap_ok),
        "empty_window_not_tradable": not is_tradable_execution_price(vwap_empty),
        "no_close_fill_fallback": close_fill is None,
        "turnover_cost_10bps_full_rebalance": abs(cost - 0.001) < 1e-12,
        "factor_vs_gross1": abs(factor_spread(0.1, -0.05) - 0.15) < 1e-12
        and abs(gross1_execution_return(0.1, -0.05) - 0.075) < 1e-12,
        "oos_tail_drop": oos_tail_formation_valid(date(2025, 12, 20), 20, date(2025, 12, 31))
        is False,
        "oos_tail_keep": oos_tail_formation_valid(date(2025, 12, 10), 20, date(2025, 12, 31))
        is True,
        "decile_monotonic_synthetic": synthetic_deciles_are_monotonic(50),
        "entry_not_overlapping_chart_interval": entry_start >= chart_end
        and not (chart_start <= entry_start < chart_end),
    }
    failed = [name for name, ok in checks.items() if not ok]
    return {
        "schema_version": 1,
        "status": (
            "execution_leakage_audit_pass" if not failed else "execution_leakage_audit_fail"
        ),
        "purpose": "d2_execution_timeline_tradability_cost_and_decile_guards_no_formal_oos",
        "protocol_reference": {
            "entry_date_formula": "t+1",
            "exit_date_formula": "t+R+1",
            "entry_window_utc": "00:05-00:10",
            "exact_holding_hours_formula": "R*24",
            "missing_or_zero_volume_execution_window": "not_tradable_no_close_fill",
            "one_way_cost_bps_primary": 10,
        },
        "example": {
            "chart_date": chart.isoformat(),
            "horizon_r": horizon,
            "entry_date": entry.isoformat(),
            "exit_date": exit_.isoformat(),
            "vwap_ok": vwap_ok,
            "turnover_cost_fraction": cost,
        },
        "checks": checks,
        "failed_checks": failed,
        "formal_oos_accessed": False,
        "formal_portfolio_returns_computed": False,
    }
