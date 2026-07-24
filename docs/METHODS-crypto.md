# Methods for Study B: cryptocurrency asset-class transfer

Scientific overview: [SCIENTIFIC-OVERVIEW.md](SCIENTIFIC-OVERVIEW.md).  
Study A: [METHODS.md](METHODS.md). Study C: [METHODS-us-to-crypto-transfer.md](METHODS-us-to-crypto-transfer.md).

## Citations

Primary reference: Jiang, Kelly and Xiu (2023), *The Journal of Finance*, [doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268).  
Full register: [CITATIONS.md](../CITATIONS.md).  
Machine-readable design: [configs/crypto_daily_reimaging_v1.yaml](../configs/crypto_daily_reimaging_v1.yaml).

This study retains the image, convolutional network and cross-sectional ranking design of Jiang et al. (2023) and changes only the asset class from US equities to single-exchange cryptocurrency spot markets.

---

## 1. Research question

Jiang et al. (2023) show that greyscale OHLC images with moving averages and volume support out-of-sample equity trend signals and can transfer across international equities and time scales. They do not examine transfer from equities to cryptocurrencies.

The confirmatory question is whether local retrain of a frozen Jiang-style daily image CNN on Binance USDT spot produces positive out-of-sample cross-sectional ranking skill on the grid \(I,R\in\{5,20,60\}\). Metrics published in this package concern cryptocurrency retrain only. Protocol-level secondary arms such as frozen US-to-crypto weight transfer and fine-tuning are outside the reported headline tables.

---

## 2. Market and universe

| Element | Specification |
|---------|---------------|
| Exchange and market | Binance USDT spot; perpetual futures excluded |
| Calendar | UTC natural day on the half-open interval from 00:00 to 24:00 |
| Source | One-minute klines aggregated to daily OHLCV |
| Content snapshot | 23,674 files, approximately 128.9 GB; content-set SHA-256 `bdf6acc4…c3fc558` on the host manifest |
| Point-in-time eligibility | Listing age at least 120 days; at least 27 valid days in the last 30; median thirty-day quote volume at least one million USDT; top 200 by lagged average daily volume; formation days with fewer than 50 names dropped for decile sorts |
| Exclusions | Stablecoins and fiat proxies, leveraged tokens, index and ETF-like tokens, unresolved identity breaks |
| Identity freeze | Seven redenomination or ticker-reuse candidates induce series splits at the break; OHLC is not rescaled across the break |

Historical symbols are drawn from exchange state files and the full kline inventory rather than from a survivor list observed in 2026.

---

## 3. Daily bars, images and labels

### 3.1 Aggregation

From coverage-valid one-minute bars, open, high, low and close follow standard daily OHLC rules; base and quote volumes are summed. A day is invalid if minute coverage is below 95 percent; prices are not forward-filled.

The image volume panel uses base volume to preserve the closest analogy to share volume in equities. Liquidity filters use quote volume.

### 3.2 Image specification

| \(I\) | Tensor shape | Moving average | CNN parameters |
|------:|-------------:|---------------:|---------------:|
| 5 | \(1\times32\times15\) | 5 | 155,138 |
| 20 | \(1\times64\times60\) | 20 | 708,866 |
| 60 | \(1\times96\times180\) | 60 | 2,952,962 |

Images are greyscale OHLC bars with equal-length moving averages and a bottom volume strip. Missing history slots appear as blank columns without interpolation. Pixel parity against the pinned author DrawOHLC path was required for I5, I20 and I60 before formal datasets were accepted.

### 3.3 Labels

\[
r_{t\to t+R} = \frac{C_{t+R}}{C_t}-1,\qquad y=\mathbf{1}\{r>0\}.
\]

Primary ranking metrics use continuous returns \(r\), not only the binary label.

---

## 4. Sample split and formation grid

| Segment | Calendar | Role |
|---------|----------|------|
| In-sample | 2018-01-01 to 2021-12-31 | Training and purged validation |
| Out-of-sample | 2022-01-01 to 2025-12-31 | Frozen evaluation window |
| Excluded | 2026 | Outside the design |

Chart dates lie on an anchor-aligned grid with step equal to horizon \(R\), yielding non-overlapping holds analogous to weekly, monthly and quarterly formation in the equity bootstrap:

| \(R\) | Step | Out-of-sample formation dates |
|------:|-----:|------------------------------:|
| 5 | 5 days | 291 |
| 20 | 20 days | 72 |
| 60 | 60 days | 23 |

Validation indices must satisfy \(\mathrm{index} > \mathrm{train\_max} + R + (2I-2)\). Out-of-sample datasets reuse in-sample train-only normalisation statistics and never re-estimate them on the evaluation window. After the identity freeze, one in-sample validation sample that crossed a break was removed, reducing the I20/R20 in-sample count from 3514 to 3513.

Implementation of the formation grid is in [`src_snapshot/crypto/formation.py`](../src_snapshot/crypto/formation.py).

---

## 5. Model training

Architecture follows the Jiang-style two-dimensional CNN family with five seeds in \(\{0,1,2,3,4\}\). Training minimises unweighted binary cross-entropy without class weights. Checkpoints correspond to minimum validation loss under early stopping. Hardware is NVIDIA GeForce RTX 3090. Out-of-sample scores are mean predicted probabilities across the five seeds. Training checkpoints are not redistributed in this repository.

---

## 6. Evaluation

Results are reported in [results/crypto/](../results/crypto/).

| Metric | Definition |
|--------|------------|
| Rank IC | Mean over formation dates of the Spearman correlation between ensemble up-probability and forward close-to-close return |
| ICIR | Mean Rank IC divided by its standard deviation |
| AUC and Brier | Pooled classification diagnostics |
| Long–short Sharpe | Equal-weight top-minus-bottom decile period return, annualised by \(\sqrt{365/R}\), with zero transaction costs and close-to-close fills |

The long–short Sharpe path is an economic illustration only. Delayed entry on a 00:05–00:10 UTC window and ten-basis-point costs are specified as primitives in `execution.py` but are not the headline freeze of the published matrix.

---

## 7. Relation to Study A

|  | Study A | Study B |
|--|---------|---------|
| Scientific lever | Bar representation under raw, expand and clip rules | Asset class under cryptocurrency spot |
| Data | hfdata US one-minute equities | Binance USDT spot one-minute |
| Sample | 1993–2002 in-sample; 2003–2025 out-of-sample | 2018–2021 in-sample; 2022–2025 out-of-sample |
| Principal table | Net Sharpe gaps across representation arms | Nine-cell Rank IC matrix |

Both studies share the Jiang et al. (2023) image-CNN agenda and the grid \(I,R\in\{5,20,60\}\).
