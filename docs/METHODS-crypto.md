# Methods — Study B: crypto asset-class transfer

## Citations (read first)

- Primary method paper: Jiang, Kelly & Xiu (2023), *The Journal of Finance*, [doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)
- Full citation register: [CITATIONS.md](../CITATIONS.md)
- Machine-readable design freeze: [configs/crypto_daily_reimaging_v1.yaml](../configs/crypto_daily_reimaging_v1.yaml)
- Protocol narrative (engineering workspace origin): crypto `plan/experiment-protocol.md` (summarised here)

This study keeps the **image + CNN + cross-sectional ranking** design language of Jiang et al. (2023) and changes only the **asset class**: US equities → **single-exchange crypto spot**.

---

## 1. Research question

Jiang et al. (2023) show that greyscale OHLC(+MA/volume) images support out-of-sample equity trend signals and can transfer across international equities and time scales. They do **not** test transfer from equities to **cryptocurrencies**.

**Question (confirmatory).**  
Under a frozen Jiang-style daily image CNN, does **local retrain** on Binance USDT spot produce positive out-of-sample cross-sectional ranking skill for \(I,R\in\{5,20,60\}\)?

Secondary arms designed in the protocol (US→crypto freeze-weight transfer; fine-tune) are **not** the headline of this results package; the published metrics here are **crypto retrain** only.

---

## 2. Market and universe

| Item | Choice |
|------|--------|
| Exchange / market | **Binance USDT spot** only (no perpetual futures in v1) |
| Calendar | UTC natural day \([00{:}00,24{:}00)\) |
| Source | 1-minute klines → daily OHLCV aggregation |
| Content snapshot | 23,674 files / ~128.9 GB; content-set SHA-256 `bdf6acc4…c3fc558` (host manifest) |
| Point-in-time eligibility | Listing age ≥ 120 days; ≥27/30 valid days; median 30-day quote volume ≥ 1e6 USDT; top 200 by **lagged** ADV; drop days with \(N<50\) for deciles |
| Exclusions | Stablecoins / fiat proxies, leveraged tokens, index/ETF-like tokens, unresolved identity breaks |
| Identity freeze v1 | Seven redenomination / ticker-reuse candidates → **split series at break** (no OHLC rescale) |

Survivorship: historical symbols come from exchange state + full kline inventory, not a 2026 survivor list.

---

## 3. Daily bars, images, labels

### 3.1 Aggregation

From coverage-valid 1m bars:

- open / high / low / close as standard daily OHLC  
- base and quote volume summed  
- day invalid if minute coverage &lt; 95% (no price forward-fill)

Image volume panel uses **base volume** (closest stock-share analogy). Liquidity filters use **quote volume**.

### 3.2 Image specification (author-exact renderer)

| \(I\) | Tensor shape | MA | CNN parameter count |
|------:|-------------:|---:|--------------------:|
| 5 | \(1\times32\times15\) | 5 | 155,138 |
| 20 | \(1\times64\times60\) | 20 | 708,866 |
| 60 | \(1\times96\times180\) | 60 | 2,952,962 |

Greyscale OHLC bars + equal-length MA + bottom volume strip; missing history slots are **blank columns** (no interpolation). Pixel parity against the pinned author `DrawOHLC` path was required for I5/I20/I60 before formal datasets.

### 3.3 Labels

\[
r_{t\to t+R} = \frac{C_{t+R}}{C_t}-1,\qquad y=\mathbf{1}\{r>0\}.
\]

Primary ranking metric uses continuous \(r\), not only the binary label.

---

## 4. Sample split and formation grid

| Segment | Calendar | Role |
|---------|----------|------|
| In-sample (IS) | **2018-01-01 → 2021-12-31** | Train + purged validation |
| Out-of-sample (OOS) | **2022-01-01 → 2025-12-31** | Frozen evaluation window |
| Excluded | 2026 | Not in design |

**Formation frequency.** Chart dates lie on an anchor-aligned grid with **step = \(R\)** (non-overlapping holds), matching the equity bootstrap’s weekly/monthly/quarterly style formation:

| \(R\) | Step | OOS formation dates (approx.) |
|------:|-----:|-------------------------------:|
| 5 | 5 days | 291 |
| 20 | 20 days | 72 |
| 60 | 60 days | 23 |

**Purge.** Validation indices must satisfy  
\(\mathrm{index} > \mathrm{train\_max} + R + (2I-2)\).  
OOS datasets **reuse IS train-only normalisation** (never re-fit on OOS).

**Identity filter.** After formal freeze, one IS validation sample crossing a break was dropped (3514 → 3513 on I20/R20).

Code: [`src_snapshot/crypto/formation.py`](../src_snapshot/crypto/formation.py).

---

## 5. Model training

- Architecture: Jiang-style 2D CNN family (`build_model(I)`), five seeds \(\{0,1,2,3,4\}\)
- Loss: unweighted binary cross-entropy (no class weights)
- Checkpoint: minimum validation loss with early stopping
- Device: NVIDIA GeForce RTX 3090
- OOS score: **mean probability** across five seeds

Training produces engineering checkpoints; they are **not** redistributed in this repository.

---

## 6. Evaluation (what this package reports)

Reported in [results/crypto/](../results/crypto/):

1. **Rank IC** — mean over formation dates of Spearman(\(\hat p\), \(r\))  
2. **ICIR** — mean IC / std IC  
3. **AUC / Brier** — pooled classification diagnostics  
4. **LS Sharpe proxy** — equal-weight top−bottom decile period return, annualised \(\sqrt{365/R}\), **0 bps cost**, **close-to-close** fills  

**Explicitly not claimed as tradable alpha:** delayed 00:05–00:10 UTC VWAP execution + 10 bp costs (primitives exist in `execution.py` but bulk economic tables are not the headline freeze of this package).

---

## 7. What differs from Study A (equity OHLC representations)

| | Study A (equity) | Study B (crypto) |
|--|------------------|------------------|
| Scientific lever | Bar **representation** (raw / expand / clip) | **Asset class** (spot crypto vs equity design) |
| Data | hfdata US 1-minute equities | Binance USDT spot 1-minute |
| IS / OOS | 1993–2002 / 2003–2025 | 2018–2021 / 2022–2025 |
| Main table | Net Sharpe gaps across arms | Nine-cell Rank IC matrix |

Both studies share the Jiang et al. (2023) image-CNN agenda and the same \(I,R\in\{5,20,60\}\) grid language.
