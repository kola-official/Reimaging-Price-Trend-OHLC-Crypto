"""purged_primary train/validation date split (plan §3.5)."""

from __future__ import annotations

from typing import Sequence


def purge_cut_index(train_max_idx: int, image_window: int, horizon: int) -> int:
    """Return cut such that val indices must be > cut.

    cut = train_max_idx + R + (2*I - 2)
    so val_first > train_max + R + (2I-2)
    """
    if image_window < 1 or horizon < 0:
        raise ValueError("invalid I or R")
    return int(train_max_idx + horizon + (2 * image_window - 2))


def split_chart_dates_purged(
    chart_date_indices: Sequence[int],
    *,
    image_window: int,
    horizon: int,
    train_fraction: float = 0.70,
) -> tuple[list[int], list[int]]:
    """Split sorted unique chart session indices into train/val with purge cut.

    chart_date_indices must be unique and sorted ascending (session indices).
    Same chart date must not be split across folds (caller assigns rows by date).
    """
    d = list(chart_date_indices)
    if len(d) != len(set(d)):
        raise ValueError("chart dates must be unique")
    if d != sorted(d):
        raise ValueError("chart dates must be sorted")
    m = len(d)
    if m < 2:
        raise ValueError("need at least two distinct chart dates")
    m_train = int(m * train_fraction)
    m_train = min(max(m_train, 1), m - 1)
    train = d[:m_train]
    val0 = d[m_train:]
    t_max = train[-1]
    cut = purge_cut_index(t_max, image_window, horizon)
    val = [x for x in val0 if x > cut]
    if not train or not val:
        raise RuntimeError(
            f"purge emptied a fold: train={len(train)} val={len(val)} "
            f"cut={cut} t_max={t_max} I={image_window} R={horizon}"
        )
    # assertions for all pairs (tightest is enough but full check)
    for dt in train:
        for dv in val:
            if not (dv > dt + horizon + (2 * image_window - 2)):
                raise RuntimeError(f"purge assertion failed: train={dt} val={dv}")
    return train, val


def assert_no_forbidden_overlap(
    train_idx: int, val_idx: int, image_window: int, horizon: int
) -> None:
    if val_idx <= train_idx + horizon + (2 * image_window - 2):
        raise AssertionError(
            f"forbidden overlap: train={train_idx} val={val_idx} I={image_window} R={horizon}"
        )
