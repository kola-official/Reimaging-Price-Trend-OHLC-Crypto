# Interpretation — crypto image CNNs vs equities

This note is **interpretive**. It organises the nine-cell crypto out-of-sample audit into a working scientific account. Numbers come from the RTX 3090 audit of 2026-07-24 ([results/crypto/](../results/crypto/)). Causal claims about market microstructure are **hypotheses**, not identified mechanisms.

---

## 1. Empirical pattern to explain

### 1.1 Headline facts

1. **Primary design cell I20/R20 fails.**  
   Rank IC \(= -0.0495\), AUC \(= 0.450\) (below coin-flip). This is the natural equity-style monthly panel and the usual focal cell in local equity replications.

2. **Best medium-horizon ranking is not I20.**  
   For **20-day** forecasts, the strongest Rank ICs are approximately:
   - **I5/R20** ≈ \(+0.034\)  
   - **I60/R20** ≈ \(+0.032\)  
   With a **portfolio-style** (decile LS Sharpe proxy, 0 cost) reading, **I60/R20 is the standout** (~1.36) while I5/R20 is milder (~0.72).

3. **The full grid is heterogeneous, not uniformly positive.**  
   Several cells are near zero or negative (I20/R20, I60/R60). There is **no** clean “all cells positive and increasing in \(R\)” story.

4. **Magnitudes stay far below equity benchmarks under related pipelines.**  
   Local US equity I20 ensembles report monthly Rank IC on the order of **~0.05** with economically large H–L Sharpes after costs on multi-decade samples (Study A / equity bootstrap). Crypto’s *best* Rank ICs are ~0.03 on a short OOS window, and the **primary cell is negative**.

### 1.2 Compact matrix (Rank IC)

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| **I5** | +0.014 | **+0.034** | +0.026 |
| **I20** | +0.018 | **−0.049** | +0.002 |
| **I60** | +0.009 | **+0.032** | −0.009 |

---

## 2. Working reading: “longer lookback helps medium-horizon ranking—when anything helps”

### 2.1 Why highlight **I60 → R20**?

A natural equity intuition is that **I20/R20** (roughly a month of image context for a month-ahead label) should be the workhorse. In crypto retrain it is the **worst** cell.

By contrast, feeding a **60-day** image when forecasting **20-day** returns (I60/R20):

- ranks among the **top Rank IC** cells,  
- delivers the **highest LS Sharpe proxy** in the audit,  
- still uses a horizon with **72** OOS formation dates (unlike R60’s 23 dates).

**Interpretation (descriptive).**  
When any stable cross-sectional structure exists, the network appears to need a **longer visual history** than the forecast horizon—consistent with slow, path-level features (multi-week drift / range regimes) mattering more than a short local motif. That echoes Study A’s finding that **long visual windows** are where representation choices move portfolio outcomes most, but here the message is weaker: even the best crypto cell remains a **modest ranking edge**, not an equity-scale signal.

We deliberately do **not** promote I60/R20 as a trading recommendation: costs, delayed VWAP, and multiple testing across nine cells are not closed.

### 2.2 Why I20/R20 can reverse

Possible, non-exclusive accounts:

| Account | What it would imply |
|---------|---------------------|
| **Weak monthly visual regularity** | Crypto daily charts over ~20 days may be dominated by high co-movement and regime noise; the CNN overfits IS idiosyncrasies and ranks the wrong names OOS. |
| **Horizon mismatch** | Medium labels may require either shorter motifs (I5) or longer context (I60); “I equals R” is not privileged outside equities. |
| **Sample fragility** | IS is only four calendar years; early stopping often fires within 3–5 epochs with near-zero validation MCC—signals may be thin even before OOS. |

---

## 3. Comparison with equities: transfer fails at the asset-class boundary

Jiang et al. (2023) document **international equity** and **time-scale** transfer for image CNNs. Our confirmatory change is harder: **equity → crypto spot**.

| Dimension | US equities (related pipelines) | Crypto spot (this study) |
|-----------|----------------------------------|---------------------------|
| Cross-section depth | Thousands of names over decades | Top-200 eligible; effective \(N\) often ~50–200 |
| History | Multi-decade daily panels | Liquid history mostly post-2017; IS 2018–2021 |
| Session structure | Shared RTH calendar | 24×7 UTC days |
| Primary I20/R20 | Positive Rank IC / large H–L in local replications | **Negative** Rank IC in this audit |
| Best cells | Strong diagonal economics in Study A | Weak, scattered; best Rank IC ~0.03 |

**Scientific conclusion (bounded).**  
We **do not** obtain a confirmatory replication of Jiang-style image predictability on crypto spot. The failure of the primary cell, and the gap versus equity Rank IC levels, support a **negative transfer** result: the equity image recipe is **not automatically portable** to this market.

---

## 4. Why “the crypto book is too small” is a useful working hypothesis

The phrase is informal. More precise components:

1. **Thin cross-section.**  
   Decile sorts need \(N \ge 50\); many formation days sit near that floor. Equity studies sort far deeper books. Estimation noise in rank correlations and decile means is therefore larger.

2. **Short effective sample.**  
   Non-overlapping R20 formation yields **72** OOS dates; R60 only **23**. Equity OOS spans decades of monthly/weekly points. Detecting a 0.02–0.03 Rank IC with high confidence is intrinsically hard.

3. **High commonality.**  
   Spot USDT names share exchange, quote asset, and macro-crypto shocks. If residual idiosyncratic variation is small, **cross-sectional** image features have less ranking work to do—even if time-series trends exist in BTC alone.

4. **Identity and microstructure dirt.**  
   Redenominations, delistings, and 24×7 gaps force splits and blank columns. That is handled, but it further reduces clean panel mass relative to CRSP-like equities.

Under that reading, “盘太小” means: **the tradable, clean, point-in-time cross-section is too small and too short for Jiang-style image CNNs to recover equity-like predictability**—not that no crypto signal can ever exist under any model or horizon.

---

## 5. What we are *not* claiming

- Crypto is information-efficient in the strong sense.  
- Every machine-learning method fails on crypto.  
- I60/R20 is a deployable strategy (0 cost, close-to-close, multi-cell search).  
- Numerical equality with Jiang et al.’s CRSP tables (different data, years, and implementation).

---

## 6. One-paragraph synthesis

Keeping the Jiang–Kelly–Xiu image CNN fixed and swapping only the universe to Binance USDT spot, we find **no reliable primary-cell predictability**: I20/R20 ranks **inversely** out of sample. Among medium-horizon forecasts, **longer 60-day image context (I60/R20)** is the most coherent positive cell on portfolio-style metrics and near-best on Rank IC, yet still **far weaker than equity replications**. The pattern is consistent with a **small, short, highly co-moving cross-section** that does not support equity-scale visual trend extraction. The scientific contribution of Study B is therefore primarily a **bounded negative result on asset-class transfer**, plus a descriptive map of which \((I,R)\) cells remain least fragile.
