# Scientific overview

## Core claim

Image-based convolutional networks of the form introduced by Jiang, Kelly and Xiu (2023) are sensitive both to how daily bars are drawn and to which asset universe they observe. Under a fixed learning protocol, **daily OHLC representation choices move United States equity portfolio performance**. Under the same image and model family, **cryptocurrency spot markets do not recover equity-like out-of-sample ranking skill**, whether models are retrained locally or imported as frozen equity weights.

## Evidence base

| Study | Intervention | Principal evidence | Claim strength |
|-------|--------------|--------------------|----------------|
| A | Change bar geometry on US equities | Diagonal net Sharpe gaps under a shared ten-basis-point path; Rank IC gaps remain small | Shows representation-dependent portfolio movement |
| B | Retrain on Binance USDT spot | Nine-cell out-of-sample Rank IC matrix; primary cell I20/R20 negative | Indicates failure of confirmatory asset-class transfer under retrain |
| C | Freeze US raw, expand and clip weights; score crypto OOS images | Three-arm Rank IC on shared I20/R20 keys; all negative | Indicates that equity-trained weights do not rescue crypto ranking failure |

Primary reference: Jiang, J., Kelly, B. and Xiu, D. (2023). (Re-)Imag(in)ing price trends. *The Journal of Finance* 78, 3193–3249. [doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268).

## Argument in three steps

1. **Representation matters in equities.**  
   Relative to raw bars, dollar-volume clip raises mean diagonal net Sharpe by about 0.18. Share- and dollar-volume expand dominate I60/R60 yet deteriorate I20/R20. Ranking metrics change little; economic paths change more.

2. **The same recipe does not transfer to cryptocurrency spot under retrain.**  
   On Binance USDT spot with in-sample years 2018–2021 and out-of-sample years 2022–2025, I20/R20 Rank IC is −0.0495. Medium-horizon forecasts are least fragile under longer lookbacks, notably I60/R20, but remain below equity-scale Rank IC near 0.05 in related US replications.

3. **Frozen equity weights do not close the gap.**  
   Direct application of US raw, expand and clip checkpoints to the same cryptocurrency out-of-sample keys yields Rank IC of approximately −0.051, −0.041 and −0.051 on I20/R20. Local retrain and frozen transfer therefore agree on primary-cell failure.

## Terminology

| Term | Meaning in this repository |
|------|----------------------------|
| \(I\) | Image lookback length in calendar days; values in \(\{5,20,60\}\) |
| \(R\) | Forecast horizon in calendar days; values in \(\{5,20,60\}\) |
| raw | Standard daily OHLC aggregation |
| expand | Volume-weighted high–low quantiles expanded to contain open and close |
| clip | Volume-weighted high–low band with open and close clipped into the band |
| Rank IC | Mean over formation dates of cross-sectional Spearman correlation between scores and forward returns |
| Primary cell | I20/R20, the conventional monthly-style workhorse in equity applications |
| Direct frozen transfer | Inference with fixed US weights and US train-only normalisation; no gradient updates on cryptocurrency data |

## Boundaries

The package does not claim numerical reproduction of Jiang et al. CRSP tables.  
Cryptocurrency metrics use close-to-close returns and zero transaction costs unless a table states otherwise; delayed VWAP economics are design primitives, not the headline freeze of Studies B and C.  
Expand and clip transfers in Study C are scored on raw cryptocurrency images and are therefore cross-representation unless otherwise labeled.  
Negative results are restricted to Jiang-style daily image CNNs on Binance USDT spot under the stated splits; they do not establish unpredictability of cryptocurrency returns under arbitrary models.

## Document map

| Role | Path |
|------|------|
| Equity methods | [METHODS.md](METHODS.md) |
| Equity interpretation | [INTERPRETATION.md](INTERPRETATION.md) |
| Equity results | [../results/RESULTS.md](../results/RESULTS.md) |
| Crypto retrain methods | [METHODS-crypto.md](METHODS-crypto.md) |
| Crypto retrain interpretation | [INTERPRETATION-crypto.md](INTERPRETATION-crypto.md) |
| Crypto retrain results | [../results/crypto/RESULTS.md](../results/crypto/RESULTS.md) |
| Frozen transfer methods | [METHODS-us-to-crypto-transfer.md](METHODS-us-to-crypto-transfer.md) |
| Frozen transfer interpretation | [INTERPRETATION-us-to-crypto-transfer.md](INTERPRETATION-us-to-crypto-transfer.md) |
| Frozen transfer results | [../results/crypto/transfer/RESULTS.md](../results/crypto/transfer/RESULTS.md) |
| Citations | [../CITATIONS.md](../CITATIONS.md) |
