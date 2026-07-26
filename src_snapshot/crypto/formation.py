"""Formation calendar helpers used in the crypto image pipeline.

These pure functions match the research workspace implementation of non-overlapping
formation grids with step = horizon R (days). They do not load market data.
"""

from __future__ import annotations

from datetime import date, timedelta


def formation_dates(anchor: date, start: date, end: date, step_days: int) -> list[date]:
    """Return formation dates on an anchor-aligned grid with fixed step.

    Parameters
    ----------
    anchor:
        Protocol anchor (crypto design uses 2018-01-01).
    start, end:
        Inclusive calendar bounds for the sample window (IS or OOS).
    step_days:
        Grid step. In v1 this equals the label horizon R ∈ {5, 20, 60}.
    """
    if step_days <= 0:
        raise ValueError("step_days must be positive")
    if end < start:
        raise ValueError("end must not precede start")
    current = anchor
    if current < start:
        jumps = (start - current).days // step_days
        current += timedelta(days=jumps * step_days)
        while current < start:
            current += timedelta(days=step_days)
    values: list[date] = []
    while current <= end:
        values.append(current)
        current += timedelta(days=step_days)
    return values


def purge_validation_min_index(train_max_chart_index: int, horizon_r: int, image_window_i: int) -> int:
    """Purged validation cut: val index must be > train_max + R + (2I - 2).

    Exactly tight (zero slack) under the label convention r = C[t+R]/C[t] - 1,
    whose data window ends on day t+R, and an image dependency span of 2I-1
    days (window I plus MA(I) warm-up). If the label convention ever moves to
    the delayed-execution window (entry t+1, exit t+R+1), this cut becomes one
    day short — revisit before reuse.
    """
    return train_max_chart_index + horizon_r + (2 * image_window_i - 2)


def oos_tail_formation_valid(chart_date: date, horizon_r: int, oos_end: date) -> bool:
    """Drop formation if the label-or-execution exit day falls after OOS end.

    t + R + 1 is the delayed-execution exit day (entry t+1, exit t+R+1); the
    close-to-close label itself only needs data through t + R. Using the later
    of the two implements config rule
    ``drop_oos_rows_if_label_or_execution_crosses_oos_end``.
    """
    exit_day = chart_date + timedelta(days=horizon_r + 1)
    return exit_day <= oos_end
