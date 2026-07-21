"""Global shared monthly-block bootstrap stats (plan §9.5)."""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np


def null_centered_right_tail_p(theta_hat: float, theta_boot: Sequence[float]) -> float:
    """p_nc = (1 + #{b: theta_b >= 2*theta_hat}) / (B+1)."""
    arr = np.asarray(list(theta_boot), dtype=float)
    b = arr.size
    if b < 1:
        raise ValueError("empty bootstrap")
    count = int(np.sum(arr >= 2.0 * theta_hat))
    return float((1 + count) / (b + 1))


def percentile_ci(theta_boot: Sequence[float], alpha: float = 0.05) -> tuple[float, float]:
    arr = np.asarray(list(theta_boot), dtype=float)
    lo = float(np.quantile(arr, alpha / 2))
    hi = float(np.quantile(arr, 1 - alpha / 2))
    return lo, hi


def one_sided_95_lower_bound(theta_boot: Sequence[float]) -> float:
    arr = np.asarray(list(theta_boot), dtype=float)
    return float(np.quantile(arr, 0.05))


def supports_positive(theta_boot: Sequence[float]) -> bool:
    return one_sided_95_lower_bound(theta_boot) > 0.0


def mean_delta(values_a: Sequence[float], values_b: Sequence[float]) -> float:
    a = np.asarray(values_a, dtype=float)
    b = np.asarray(values_b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("shape mismatch")
    return float(np.mean(a - b))


def oos_month_sequence(start: str = "2003-01", end: str = "2025-12") -> list[str]:
    """Frozen natural-month atoms for shared block bootstrap (YYYY-MM)."""
    periods = pd_period_range(start, end)
    return periods


def pd_period_range(start: str, end: str) -> list[str]:
    # Avoid importing pandas at module import for unit tests that only need math helpers.
    import pandas as pd

    idx = pd.period_range(start=start, end=end, freq="M")
    return [str(p) for p in idx]


def stationary_month_blocks(
    months: Sequence[str],
    *,
    mean_block_length: int = 12,
    n_samples: int = 5000,
    max_attempts: int = 50000,
    rng: np.random.Generator | None = None,
    validate=None,
) -> tuple[list[list[str]], dict]:
    """Shared stationary bootstrap over the OOS month sequence.

    Each valid replication is a length-n list of months (with replacement via blocks).
    ``validate(month_list) -> (ok: bool, reason: str|None)`` rejects joint copies.
    """
    if mean_block_length < 1:
        raise ValueError("mean_block_length must be >= 1")
    months = list(months)
    n = len(months)
    if n < 1:
        raise ValueError("empty month sequence")
    if rng is None:
        rng = np.random.default_rng(42)
    p_end = 1.0 / float(mean_block_length)
    samples: list[list[str]] = []
    invalid_by_reason: dict[str, int] = {}
    attempts = 0
    while len(samples) < n_samples and attempts < max_attempts:
        attempts += 1
        idx: list[int] = []
        while len(idx) < n:
            start = int(rng.integers(0, n))
            while True:
                idx.append(start)
                if len(idx) >= n:
                    break
                if float(rng.random()) < p_end:
                    break
                start = (start + 1) % n
        idx = idx[:n]
        mseq = [months[i] for i in idx]
        if validate is not None:
            ok, reason = validate(mseq)
            if not ok:
                key = reason or "invalid"
                invalid_by_reason[key] = invalid_by_reason.get(key, 0) + 1
                continue
        samples.append(mseq)
    meta = {
        "attempts": attempts,
        "valid": len(samples),
        "requested": n_samples,
        "max_attempts": max_attempts,
        "invalid_replication_rate": float(1.0 - (len(samples) / attempts)) if attempts else 1.0,
        "invalid_by_reason": invalid_by_reason,
        "mean_block_length": mean_block_length,
        "algorithm": "stationary_bootstrap",
        "n_months": n,
    }
    return samples, meta


def moving_month_blocks(
    months: Sequence[str],
    *,
    block_length: int = 12,
    n_samples: int = 5000,
    max_attempts: int = 50000,
    rng: np.random.Generator | None = None,
    validate=None,
) -> tuple[list[list[str]], dict]:
    """Moving-block bootstrap with fixed block length (circular)."""
    months = list(months)
    n = len(months)
    if block_length < 1:
        raise ValueError("block_length must be >= 1")
    if rng is None:
        rng = np.random.default_rng(42)
    samples: list[list[str]] = []
    invalid_by_reason: dict[str, int] = {}
    attempts = 0
    while len(samples) < n_samples and attempts < max_attempts:
        attempts += 1
        idx: list[int] = []
        while len(idx) < n:
            start = int(rng.integers(0, n))
            for k in range(block_length):
                idx.append((start + k) % n)
                if len(idx) >= n:
                    break
        idx = idx[:n]
        mseq = [months[i] for i in idx]
        if validate is not None:
            ok, reason = validate(mseq)
            if not ok:
                key = reason or "invalid"
                invalid_by_reason[key] = invalid_by_reason.get(key, 0) + 1
                continue
        samples.append(mseq)
    meta = {
        "attempts": attempts,
        "valid": len(samples),
        "requested": n_samples,
        "max_attempts": max_attempts,
        "invalid_replication_rate": float(1.0 - (len(samples) / attempts)) if attempts else 1.0,
        "invalid_by_reason": invalid_by_reason,
        "block_length": block_length,
        "algorithm": "moving_block",
        "n_months": n,
    }
    return samples, meta


def pack_inference(
    name: str,
    theta_hat: float,
    theta_boot: Sequence[float],
    *,
    B: int,
    max_attempts: int,
    invalid_replication_rate: float,
    note: str,
    extra: dict | None = None,
) -> dict:
    boot = list(theta_boot)
    lo, hi = percentile_ci(boot) if boot else (float("nan"), float("nan"))
    lb = one_sided_95_lower_bound(boot) if boot else float("nan")
    out = {
        "name": name,
        "theta_hat": float(theta_hat) if np.isfinite(theta_hat) else None,
        "ci95_low": lo,
        "ci95_high": hi,
        "one_sided_95_lower_bound": lb,
        "supports_positive_5pct": bool(np.isfinite(lb) and lb > 0),
        "null_centered_p": (
            null_centered_right_tail_p(float(theta_hat), boot)
            if boot and np.isfinite(theta_hat)
            else None
        ),
        "B": B,
        "max_attempts": max_attempts,
        "invalid_replication_rate": float(invalid_replication_rate),
        "note": note,
    }
    if extra:
        out.update(extra)
    return out


def month_key_from_date(date_like) -> str:
    import pandas as pd

    ts = pd.Timestamp(date_like)
    return f"{ts.year:04d}-{ts.month:02d}"
