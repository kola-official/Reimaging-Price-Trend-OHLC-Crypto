# Re-imagining price-trend OHLC representations and cryptocurrency transfer

**Languages:** [English](README.md) · [中文](README.zh-CN.md)  
**Repository:** [Reimaging-Price-Trend-OHLC-Crypto](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto)

## Abstract

Cross-sectional forecasts from greyscale OHLC images are a standard route for testing visual price-trend signals, following Jiang, Kelly and Xiu (2023) in *The Journal of Finance* ([doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)). Two design choices remain incompletely mapped: how the daily bar is drawn, and whether the equity recipe extends beyond equities.

This repository reports three linked empirical studies under a shared image-CNN family. **Study A** varies United States daily bar geometry under raw, share-volume and dollar-volume expand and clip rules. Dollar-volume clip raises mean diagonal net Sharpe relative to raw by about 0.18; expand constructions dominate I60/R60 yet deteriorate I20/R20, while Rank IC gaps stay small. **Study B** retrains the same \(I,R\in\{5,20,60\}\) grid on Binance USDT spot. The primary cell I20/R20 yields Rank IC −0.0495; the least fragile medium-horizon configuration is I60/R20, still below equity-scale Rank IC near 0.05 in related US replications. **Study C** applies frozen US raw, expand and clip weights to the same cryptocurrency out-of-sample keys without gradient updates. All three arms remain negative on I20/R20 and do not improve on local retrain.

Jointly, the results show that **representation choice moves equity portfolio performance**, whereas **Jiang-style daily image CNNs do not recover equity-like ranking skill on this cryptocurrency spot sample**, under either local retrain or frozen equity transfer. The findings are bounded to the stated markets, splits and evaluation paths; they do not imply unpredictability of cryptocurrency returns under arbitrary models.

Scientific spine: [docs/SCIENTIFIC-OVERVIEW.md](docs/SCIENTIFIC-OVERVIEW.md).

| Study | Intervention | Question |
|-------|--------------|----------|
| A | Equity bar geometry | Do raw, expand and clip constructions alter out-of-sample portfolio performance? |
| B | Cryptocurrency retrain | Does the equity image specification retain ranking skill on Binance USDT spot? |
| C | Frozen US weights | Do equity-trained raw, expand and clip models transfer without retrain? |

Minute archives, image tensors and checkpoints remain on the experiment host. This repository distributes protocols, tables, interpretation and compact pure-Python utilities.

---

## Study A. Equity OHLC representations

Under a shared path from hfdata one-minute bars to greyscale images and five-seed CNNs, in-sample years are 1993–2002 and out-of-sample years are 2003–2025. Labels, moving averages and fills use raw prices; only drawn OHLC geometry differs across arms.

### Diagonal net Sharpe, ten basis points one-way

Portfolios are equal-weight high-minus-low deciles with next-open entry and planned-open exit. Annualisation uses \(\sqrt{252}\).

| Setting | raw | share expand | share clip | dollar expand | dollar clip |
|--------:|----:|-------------:|-----------:|--------------:|------------:|
| I5 / R5 | −0.40 | −0.30 | −0.18 | −0.31 | −0.07 |
| I20 / R20 | 3.07 | 1.36 | 1.89 | 1.42 | 3.13 |
| I60 / R60 | 4.37 | 6.37 | 4.33 | 6.26 | 4.52 |

Mean change versus raw across the three diagonal cells:

| Arm | Mean Δ |
|-----|--------:|
| share expand | +0.13 |
| share clip | −0.34 |
| dollar expand | +0.11 |
| dollar clip | +0.18 |

Dollar clip attains the highest average improvement and is the only non-raw arm that does not collapse I20/R20. Expand concentrates gains at long horizons. Full tables: [results/RESULTS.md](results/RESULTS.md). Methods: [docs/METHODS.md](docs/METHODS.md). Interpretation of horizon-dependent expand effects: [docs/INTERPRETATION.md](docs/INTERPRETATION.md).

---

## Study B. Cryptocurrency spot retrain

The image and model family are held fixed; the universe is Binance USDT spot with point-in-time liquidity filters, identity splits at redenomination breaks, in-sample years 2018–2021 and out-of-sample years 2022–2025. Formation is non-overlapping with step \(R\). Reported ranking metrics use close-to-close returns; zero-cost long–short Sharpe is an economic illustration only.

### Out-of-sample Rank IC

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | +0.034 | +0.026 |
| I20 | +0.018 | −0.049 | +0.002 |
| I60 | +0.009 | +0.032 | −0.009 |

I20/R20, the equity-style primary cell, fails: Rank IC −0.0495 and AUC 0.450. For twenty-day horizons, I60/R20 is the most coherent positive configuration on portfolio-style metrics and near-best on Rank IC, indicating that medium-horizon ranking, when present, benefits from lookback longer than the forecast horizon. Even the strongest cells remain weaker than equity replications and rest on sparse formation calendars.

Methods: [docs/METHODS-crypto.md](docs/METHODS-crypto.md). Results: [results/crypto/RESULTS.md](results/crypto/RESULTS.md). Interpretation: [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md).

---

## Study C. Frozen US raw, expand and clip transfer

United States `purged_primary` checkpoints for raw, expand and clip score the same cryptocurrency out-of-sample keys without gradient updates and without re-fitting United States train-only normalisation on cryptocurrency data. Expand and clip weights are applied to raw cryptocurrency images and are reported as cross-representation transfer.

### Primary cell I20/R20

| Arm | Rank IC | ICIR | AUC | Rows |
|-----|--------:|-----:|----:|-----:|
| raw | −0.051 | −0.494 | 0.478 | 13852 |
| expand | −0.041 | −0.383 | 0.482 | 13852 |
| clip | −0.051 | −0.494 | 0.473 | 13852 |

Cryptocurrency-local retrain on the same cell records Rank IC −0.0495. Frozen transfer does not reverse primary-cell failure. Diagonal I5/R5 and I60/R60 transfers are likewise non-positive for all three arms.

Methods: [docs/METHODS-us-to-crypto-transfer.md](docs/METHODS-us-to-crypto-transfer.md). Results and provenance: [results/crypto/transfer/RESULTS.md](results/crypto/transfer/RESULTS.md). Interpretation: [docs/INTERPRETATION-us-to-crypto-transfer.md](docs/INTERPRETATION-us-to-crypto-transfer.md).

---

## Synthesis

| Study | Principal finding |
|-------|-------------------|
| A | Bar geometry moves US equity portfolio Sharpe; dollar clip is strongest on average; expand is horizon-dependent. |
| B | Local retrain on cryptocurrency spot fails at I20/R20; medium-horizon structure, when present, favours longer lookback but remains weak relative to equities. |
| C | Frozen equity raw, expand and clip weights also fail on the same cryptocurrency keys, reinforcing an asset-class transfer boundary for this method family. |

A structural reading of Studies B and C is limited cross-sectional depth: a thin, short and highly co-moving point-in-time book relative to multi-decade equity panels. That reading concerns fit between Jiang-style image CNNs and this market, not a universal claim about cryptocurrency predictability.

---

## Repository layout

```text
README.md
README.zh-CN.md
CITATIONS.md
CITATION.cff
NOTICE
LICENSE
docs/
  SCIENTIFIC-OVERVIEW.md
  METHODS.md
  INTERPRETATION.md
  METHODS-crypto.md
  INTERPRETATION-crypto.md
  METHODS-us-to-crypto-transfer.md
  INTERPRETATION-us-to-crypto-transfer.md
  crypto-protocol.md
  vwpq-clip-oc-protocol.md
  vwpq-dollar-protocol.md
configs/
results/
  RESULTS.md
  crypto/
  crypto/transfer/
src_snapshot/
  hfdata/
  crypto/
```

---

## Data and code

| Layer | Source | Redistributed |
|-------|--------|---------------|
| Method paper | Jiang, Kelly and Xiu (2023), *Journal of Finance* | No |
| Equity minutes | HF Data Library US one-minute OHLCV | No |
| Equity paper sample | CRSP via WRDS | No |
| Cryptocurrency minutes | Binance spot one-minute klines on the experiment host | No |
| This repository | Tables, protocols and pure-Python snapshots | Yes, Apache-2.0 |

Authoritative wording: [CITATIONS.md](CITATIONS.md).

---

## Statistical scope

Study A emphasises signed, setting-level net Sharpe movement; a shared bootstrap for the expand arm is secondary. Studies B and C report descriptive Rank IC, ICIR and zero-cost long–short Sharpe under close-to-close fills. No claim is made that all cryptocurrency cells are jointly positive. Primary-cell failure in Studies B and C is sufficient to reject simple transfer of the equity monthly-style workhorse to this cryptocurrency sample.
