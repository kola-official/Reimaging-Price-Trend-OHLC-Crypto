"""Pure metrics and freeze constants for US→crypto direct transfer."""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Iterable

# Optional numpy — pure arithmetic fallback keeps tests runnable without deps.
try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:  # pragma: no cover
    np = None  # type: ignore
    HAS_NUMPY = False

ARM_ALIASES = {
    "raw": "raw",
    "expand": "vwpq",
    "vwpq": "vwpq",
    "clip": "vwpq_clip",
    "vwpq_clip": "vwpq_clip",
}

ARM_DISPLAY = {
    "raw": "raw",
    "vwpq": "expand",
    "vwpq_clip": "clip",
}

TRANSFER_MODE = "direct_frozen_us_weights"


def rankdata(values: list[float]) -> list[float]:
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = 0.5 * (i + 1 + j + 1)
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman_ic(scores: list[float] | "np.ndarray", rets: list[float] | "np.ndarray") -> float:
    scores_l = [float(x) for x in scores]
    rets_l = [float(x) for x in rets]
    if len(scores_l) < 3 or len(scores_l) != len(rets_l):
        return float("nan")
    rs = rankdata(scores_l)
    rr = rankdata(rets_l)
    mean_s = sum(rs) / len(rs)
    mean_r = sum(rr) / len(rr)
    ds = [x - mean_s for x in rs]
    dr = [x - mean_r for x in rr]
    var_s = sum(x * x for x in ds) / len(ds)
    var_r = sum(x * x for x in dr) / len(dr)
    if var_s <= 0 or var_r <= 0:
        return float("nan")
    std_s = math.sqrt(var_s)
    std_r = math.sqrt(var_r)
    return sum((a / std_s) * (b / std_r) for a, b in zip(ds, dr)) / len(ds)


def decile_long_short(scores: list[float], rets: list[float], n: int = 10) -> float:
    if len(scores) < n or len(scores) != len(rets):
        return float("nan")
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0] * len(scores)
    for r, i in enumerate(order):
        ranks[i] = r
    qs = [min(n - 1, int(ranks[i] * n / len(scores))) for i in range(len(scores))]
    high = [rets[i] for i in range(len(scores)) if qs[i] == n - 1]
    low = [rets[i] for i in range(len(scores)) if qs[i] == 0]
    if not high or not low:
        return float("nan")
    return sum(high) / len(high) - sum(low) / len(low)


def summarise_rank_ic_by_date(
    scores: list[float],
    rets: list[float],
    dates: Iterable[str],
    horizon_r: int,
    min_names: int = 10,
) -> dict[str, float]:
    by_date: dict[str, list[int]] = defaultdict(list)
    for i, d in enumerate(dates):
        by_date[d].append(i)
    ics: list[float] = []
    ls_vals: list[float] = []
    for d, idxs in sorted(by_date.items()):
        if len(idxs) < min_names:
            continue
        s = [scores[i] for i in idxs]
        r = [rets[i] for i in idxs]
        ics.append(spearman_ic(s, r))
        ls_vals.append(decile_long_short(s, r))
    if not ics:
        return {
            "n_ic_dates": 0.0,
            "rank_ic_mean": float("nan"),
            "rank_ic_std": float("nan"),
            "icir": float("nan"),
            "ls_mean": float("nan"),
            "ls_std": float("nan"),
            "ls_sharpe_ann_proxy": float("nan"),
        }
    mean_ic = sum(ics) / len(ics)
    if len(ics) > 1:
        var = sum((x - mean_ic) ** 2 for x in ics) / (len(ics) - 1)
        std_ic = math.sqrt(var)
    else:
        std_ic = float("nan")
    icir = mean_ic / std_ic if std_ic and std_ic > 0 else float("nan")
    mean_ls = sum(ls_vals) / len(ls_vals) if ls_vals else float("nan")
    if len(ls_vals) > 1:
        var_ls = sum((x - mean_ls) ** 2 for x in ls_vals) / (len(ls_vals) - 1)
        std_ls = math.sqrt(var_ls)
    else:
        std_ls = float("nan")
    sharpe = (
        (mean_ls / std_ls) * math.sqrt(365.0 / horizon_r)
        if std_ls and std_ls > 0
        else float("nan")
    )
    return {
        "n_ic_dates": float(len(ics)),
        "rank_ic_mean": mean_ic,
        "rank_ic_std": std_ic,
        "icir": icir,
        "ls_mean": mean_ls,
        "ls_std": std_ls,
        "ls_sharpe_ann_proxy": sharpe,
    }


def assert_freeze_payload(payload: dict) -> list[str]:
    """Return list of freeze-schema errors; empty means pass."""
    errors: list[str] = []
    for key in (
        "retrain",
        "fine_tune",
        "us_weights_updated_on_crypto",
        "us_normalization_refit_on_crypto",
    ):
        if payload.get(key) is not False:
            errors.append(f"top_level_{key}_must_be_false")
    if payload.get("transfer_mode") != TRANSFER_MODE:
        errors.append("transfer_mode")
    cells = payload.get("cells")
    if not isinstance(cells, list) or not cells:
        errors.append("cells_missing")
        return errors
    arms = {c.get("arm") for c in cells}
    if not {"raw", "expand", "clip"}.issubset(arms):
        errors.append("missing_arms")
    for cell in cells:
        if cell.get("retrain") is not False or cell.get("fine_tune") is not False:
            errors.append(f"{cell.get('arm')}_retrain_or_finetune")
        if cell.get("gradient_updates") != 0:
            errors.append(f"{cell.get('arm')}_gradient_updates")
        if cell.get("us_normalization_refit_on_crypto") is not False:
            errors.append(f"{cell.get('arm')}_norm_refit")
        if not isinstance(cell.get("rank_ic_mean"), (int, float)):
            errors.append(f"{cell.get('arm')}_rank_ic")
        if int(cell.get("n_pred_rows") or 0) <= 0:
            errors.append(f"{cell.get('arm')}_n_pred_rows")
        seeds = cell.get("seeds") or []
        if len(seeds) != 5:
            errors.append(f"{cell.get('arm')}_seeds")
        for seed in seeds:
            if seed.get("gradient_updates") != 0 or seed.get("optimizer_steps") != 0:
                errors.append(f"{cell.get('arm')}_seed_updates")
            if seed.get("us_normalization_refit_on_crypto") is not False:
                errors.append(f"{cell.get('arm')}_seed_norm")
    return errors
