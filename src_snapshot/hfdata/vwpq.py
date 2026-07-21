"""Daily bar aggregation: raw OHLC and volume-weighted percentile H/L (plan §5)."""

from __future__ import annotations

import numpy as np


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


def _session_typical_prices_and_weights(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    p = (high.astype(np.float64) + low.astype(np.float64) + close.astype(np.float64)) / 3.0
    w = volume.astype(np.float64)
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
) -> tuple[dict[str, float], float, float] | None:
    """Return (raw_bar, q_low_price, q_high_price) or None if invalid/zero volume."""
    raw = aggregate_raw_session(open_, high, low, close, volume)
    n = open_.size
    if n < min_bars or float(np.sum(volume)) <= 0:
        return None
    p, w = _session_typical_prices_and_weights(high, low, close, volume)
    try:
        q_lo = weighted_quantile(p, w, q_low)
        q_hi = weighted_quantile(p, w, q_high)
    except ValueError:
        return None
    if q_lo > q_hi:
        q_lo, q_hi = q_hi, q_lo
    return raw, float(q_lo), float(q_hi)


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
) -> dict[str, float | bool]:
    """VWPQ-expand (plan v3.6): O/C/V identical to raw; H/L = VW quantiles expanded to cover O/C.

    Protocol id: ``vwpq`` / ``vwpq_expand``. Does **not** clip open/close.
    """
    band = _vw_quantile_band(
        open_, high, low, close, volume, min_bars=min_bars, q_low=q_low, q_high=q_high
    )
    raw = aggregate_raw_session(open_, high, low, close, volume)
    if band is None:
        return {
            **raw,
            "high": raw["high"],
            "low": raw["low"],
            "vwpq_valid": False,
            "protocol": "vwpq_expand",
        }
    raw, q05, q95 = band
    o, c = raw["open"], raw["close"]
    l_v = min(q05, o, c)
    h_v = max(q95, o, c)
    if not (l_v <= min(o, c) <= max(o, c) <= h_v):
        raise ValueError("vwpq expand failed OHLC inequality")
    return {
        "open": o,
        "high": h_v,
        "low": l_v,
        "close": c,
        "volume": raw["volume"],
        "vwpq_valid": True,
        "q05": q05,
        "q95": q95,
        "protocol": "vwpq_expand",
    }


def _clip_price_to_band(price: float, lo: float, hi: float) -> float:
    """Clip price into [lo, hi]."""
    if price < lo:
        return float(lo)
    if price > hi:
        return float(hi)
    return float(price)


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
) -> dict[str, float | bool]:
    """VWPQ-clip-OC: H/L = VW quantile band; O/C clipped into [L,H] when outside.

    Protocol id: ``vwpq_clip`` / ``vwpq_clip_oc``.

    - Volume always equals raw volume.
    - H = q_high, L = q_low (no expand to cover raw O/C).
    - O' = clip(raw O, L, H), C' = clip(raw C, L, H).
    - Zero-volume / invalid sessions: ``vwpq_valid=False`` and do **not** fall back
      to raw OHLC or to the expand rule (high/low left as raw only for schema
      continuity; callers must not treat invalid days as clip representation).

    Labels and execution prices remain raw by pipeline freeze; this transform is
    representation-only for image rendering.
    """
    band = _vw_quantile_band(
        open_, high, low, close, volume, min_bars=min_bars, q_low=q_low, q_high=q_high
    )
    raw = aggregate_raw_session(open_, high, low, close, volume)
    if band is None:
        return {
            "open": raw["open"],
            "high": raw["high"],
            "low": raw["low"],
            "close": raw["close"],
            "volume": raw["volume"],
            "vwpq_valid": False,
            "protocol": "vwpq_clip_oc",
            "clipped_open": False,
            "clipped_close": False,
        }
    raw, q05, q95 = band
    l_v = float(q05)
    h_v = float(q95)
    o_raw, c_raw = float(raw["open"]), float(raw["close"])
    o_c = _clip_price_to_band(o_raw, l_v, h_v)
    c_c = _clip_price_to_band(c_raw, l_v, h_v)
    if not (l_v <= min(o_c, c_c) <= max(o_c, c_c) <= h_v):
        raise ValueError(
            f"vwpq clip-OC failed OHLC inequality: O={o_c} H={h_v} L={l_v} C={c_c}"
        )
    return {
        "open": o_c,
        "high": h_v,
        "low": l_v,
        "close": c_c,
        "volume": raw["volume"],
        "vwpq_valid": True,
        "q05": q05,
        "q95": q95,
        "protocol": "vwpq_clip_oc",
        "open_raw": o_raw,
        "close_raw": c_raw,
        "clipped_open": bool(o_c != o_raw),
        "clipped_close": bool(c_c != c_raw),
    }


def assert_ocv_identical(raw: dict, vwpq: dict, atol: float = 0.0) -> None:
    """Assert O/C/V match — only valid for expand arm, not clip-OC."""
    for k in ("open", "close", "volume"):
        if abs(float(raw[k]) - float(vwpq[k])) > atol:
            raise AssertionError(f"O/C/V mismatch on {k}: {raw[k]} vs {vwpq[k]}")


def assert_clip_oc_in_band(bar: dict, atol: float = 1e-12) -> None:
    """Assert clip-OC bar satisfies L <= min(O,C) <= max(O,C) <= H."""
    o, h, l, c = float(bar["open"]), float(bar["high"]), float(bar["low"]), float(bar["close"])
    if not (l - atol <= min(o, c) and max(o, c) <= h + atol):
        raise AssertionError(f"clip band violation O={o} H={h} L={l} C={c}")
