"""Daily bar aggregation: raw OHLC and volume- / dollar-volume-weighted H/L."""

from __future__ import annotations

import numpy as np

# Weight modes for quantile band construction
WEIGHT_SHARE = "share"  # w = V (share volume)
WEIGHT_DOLLAR = "dollar"  # w = p * V (dollar volume)


def weighted_quantile(prices: np.ndarray, weights: np.ndarray, q: float) -> float:
    """Smallest price with cumulative normalized weight >= q; stable by (p, index)."""
    if prices.size == 0:
        raise ValueError("empty prices")
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0, 1]")
    order = np.lexsort((np.arange(prices.size), prices))
    p = prices[order]
    w = weights[order].astype(np.float64)
    total = w.sum()
    if total <= 0 or not np.isfinite(total):
        raise ValueError("non-positive total weight")
    cum = np.cumsum(w) / total
    idx = int(np.searchsorted(cum, q, side="left"))
    idx = min(max(idx, 0), p.size - 1)
    return float(p[idx])


def aggregate_raw_session(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
) -> dict[str, float]:
    """RTH 1-min bars -> raw daily OHLCV."""
    if open_.size == 0:
        raise ValueError("empty session")
    o = float(open_[0])
    h = float(np.max(high))
    l = float(np.min(low))
    c = float(close[-1])
    v = float(np.sum(volume))
    if not (l <= min(o, c) <= max(o, c) <= h):
        raise ValueError(f"raw OHLC inequality failed: O={o} H={h} L={l} C={c}")
    return {"open": o, "high": h, "low": l, "close": c, "volume": v}


def session_typical_prices(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    return (high.astype(np.float64) + low.astype(np.float64) + close.astype(np.float64)) / 3.0


def session_weights(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    *,
    weight_mode: str = WEIGHT_SHARE,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (typical_prices, weights) for share- or dollar-volume weighting."""
    p = session_typical_prices(high, low, close)
    v = volume.astype(np.float64)
    if weight_mode == WEIGHT_SHARE:
        w = v
    elif weight_mode == WEIGHT_DOLLAR:
        w = p * v
    else:
        raise ValueError(f"unknown weight_mode={weight_mode!r}")
    return p, w


def _vw_quantile_band(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    *,
    min_bars: int,
    q_low: float,
    q_high: float,
    weight_mode: str = WEIGHT_SHARE,
) -> tuple[dict[str, float], float, float] | None:
    """Return (raw_bar, q_low_price, q_high_price) or None if invalid/zero volume."""
    raw = aggregate_raw_session(open_, high, low, close, volume)
    n = open_.size
    if n < min_bars or float(np.sum(volume)) <= 0:
        return None
    p, w = session_weights(high, low, close, volume, weight_mode=weight_mode)
    if float(np.sum(w)) <= 0 or not np.isfinite(np.sum(w)):
        return None
    try:
        q_lo = weighted_quantile(p, w, q_low)
        q_hi = weighted_quantile(p, w, q_high)
    except ValueError:
        return None
    if q_lo > q_hi:
        q_lo, q_hi = q_hi, q_lo
    return raw, float(q_lo), float(q_hi)


def _clip_price_to_band(price: float, lo: float, hi: float) -> float:
    if price < lo:
        return float(lo)
    if price > hi:
        return float(hi)
    return float(price)


def _expand_from_band(
    raw: dict[str, float],
    q05: float,
    q95: float,
    *,
    protocol: str,
    weight_mode: str,
) -> dict[str, float | bool | str]:
    o, c = raw["open"], raw["close"]
    l_v = min(q05, o, c)
    h_v = max(q95, o, c)
    if not (l_v <= min(o, c) <= max(o, c) <= h_v):
        raise ValueError(f"{protocol} expand failed OHLC inequality")
    return {
        "open": o,
        "high": h_v,
        "low": l_v,
        "close": c,
        "volume": raw["volume"],
        "vwpq_valid": True,
        "q05": q05,
        "q95": q95,
        "protocol": protocol,
        "weight_mode": weight_mode,
    }


def _clip_from_band(
    raw: dict[str, float],
    q05: float,
    q95: float,
    *,
    protocol: str,
    weight_mode: str,
) -> dict[str, float | bool | str]:
    l_v = float(q05)
    h_v = float(q95)
    o_raw, c_raw = float(raw["open"]), float(raw["close"])
    o_c = _clip_price_to_band(o_raw, l_v, h_v)
    c_c = _clip_price_to_band(c_raw, l_v, h_v)
    if not (l_v <= min(o_c, c_c) <= max(o_c, c_c) <= h_v):
        raise ValueError(f"{protocol} clip failed OHLC inequality: O={o_c} H={h_v} L={l_v} C={c_c}")
    return {
        "open": o_c,
        "high": h_v,
        "low": l_v,
        "close": c_c,
        "volume": raw["volume"],
        "vwpq_valid": True,
        "q05": q05,
        "q95": q95,
        "protocol": protocol,
        "weight_mode": weight_mode,
        "open_raw": o_raw,
        "close_raw": c_raw,
        "clipped_open": bool(o_c != o_raw),
        "clipped_close": bool(c_c != c_raw),
    }


def _invalid_bar(raw: dict[str, float], protocol: str, weight_mode: str, clip: bool) -> dict:
    base = {
        "open": raw["open"],
        "high": raw["high"],
        "low": raw["low"],
        "close": raw["close"],
        "volume": raw["volume"],
        "vwpq_valid": False,
        "protocol": protocol,
        "weight_mode": weight_mode,
    }
    if clip:
        base["clipped_open"] = False
        base["clipped_close"] = False
    return base


# ---- Share-volume arms (legacy path ids: vwpq / vwpq_clip) ----


def aggregate_vwpq_session(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    *,
    min_bars: int = 1,
    q_low: float = 0.05,
    q_high: float = 0.95,
) -> dict[str, float | bool | str]:
    """Share-volume expand: O/C/V = raw; H/L from volume-weighted quantiles expanded to O/C."""
    band = _vw_quantile_band(
        open_,
        high,
        low,
        close,
        volume,
        min_bars=min_bars,
        q_low=q_low,
        q_high=q_high,
        weight_mode=WEIGHT_SHARE,
    )
    raw = aggregate_raw_session(open_, high, low, close, volume)
    if band is None:
        return _invalid_bar(raw, "vwpq_expand", WEIGHT_SHARE, clip=False)
    raw, q05, q95 = band
    return _expand_from_band(raw, q05, q95, protocol="vwpq_expand", weight_mode=WEIGHT_SHARE)


def aggregate_vwpq_clip_oc_session(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    *,
    min_bars: int = 1,
    q_low: float = 0.05,
    q_high: float = 0.95,
) -> dict[str, float | bool | str]:
    """Share-volume clip-OC: H/L = volume quantile band; O/C clipped into [L,H]."""
    band = _vw_quantile_band(
        open_,
        high,
        low,
        close,
        volume,
        min_bars=min_bars,
        q_low=q_low,
        q_high=q_high,
        weight_mode=WEIGHT_SHARE,
    )
    raw = aggregate_raw_session(open_, high, low, close, volume)
    if band is None:
        return _invalid_bar(raw, "vwpq_clip_oc", WEIGHT_SHARE, clip=True)
    raw, q05, q95 = band
    return _clip_from_band(raw, q05, q95, protocol="vwpq_clip_oc", weight_mode=WEIGHT_SHARE)


# ---- Dollar-volume arms (path ids: vwpq_d / vwpq_d_clip) ----


def aggregate_vwpq_dollar_expand_session(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    *,
    min_bars: int = 1,
    q_low: float = 0.05,
    q_high: float = 0.95,
) -> dict[str, float | bool | str]:
    """Dollar-volume expand: weights = p*V; O/C/V = raw; H/L expand to cover O/C.

    Protocol id: ``vwpq_dollar_expand`` / path arm ``vwpq_d``.
    """
    band = _vw_quantile_band(
        open_,
        high,
        low,
        close,
        volume,
        min_bars=min_bars,
        q_low=q_low,
        q_high=q_high,
        weight_mode=WEIGHT_DOLLAR,
    )
    raw = aggregate_raw_session(open_, high, low, close, volume)
    if band is None:
        return _invalid_bar(raw, "vwpq_dollar_expand", WEIGHT_DOLLAR, clip=False)
    raw, q05, q95 = band
    return _expand_from_band(
        raw, q05, q95, protocol="vwpq_dollar_expand", weight_mode=WEIGHT_DOLLAR
    )


def aggregate_vwpq_dollar_clip_session(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    *,
    min_bars: int = 1,
    q_low: float = 0.05,
    q_high: float = 0.95,
) -> dict[str, float | bool | str]:
    """Dollar-volume clip-OC: weights = p*V; H/L = band; O/C clipped into [L,H].

    Protocol id: ``vwpq_dollar_clip`` / path arm ``vwpq_d_clip``.
    """
    band = _vw_quantile_band(
        open_,
        high,
        low,
        close,
        volume,
        min_bars=min_bars,
        q_low=q_low,
        q_high=q_high,
        weight_mode=WEIGHT_DOLLAR,
    )
    raw = aggregate_raw_session(open_, high, low, close, volume)
    if band is None:
        return _invalid_bar(raw, "vwpq_dollar_clip", WEIGHT_DOLLAR, clip=True)
    raw, q05, q95 = band
    return _clip_from_band(
        raw, q05, q95, protocol="vwpq_dollar_clip", weight_mode=WEIGHT_DOLLAR
    )


def assert_ocv_identical(raw: dict, vwpq: dict, atol: float = 0.0) -> None:
    """Assert O/C/V match — only valid for expand arms, not clip."""
    for k in ("open", "close", "volume"):
        if abs(float(raw[k]) - float(vwpq[k])) > atol:
            raise AssertionError(f"O/C/V mismatch on {k}: {raw[k]} vs {vwpq[k]}")


def assert_clip_oc_in_band(bar: dict, atol: float = 1e-12) -> None:
    """Assert clip bar satisfies L <= min(O,C) <= max(O,C) <= H."""
    o, h, l, c = float(bar["open"]), float(bar["high"]), float(bar["low"]), float(bar["close"])
    if not (l - atol <= min(o, c) and max(o, c) <= h + atol):
        raise AssertionError(f"clip band violation O={o} H={h} L={l} C={c}")
