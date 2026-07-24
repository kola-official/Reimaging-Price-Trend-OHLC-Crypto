# Re-imagining price-trend OHLC representations and crypto asset-class transfer

**Languages:** [English](README.md) · [中文](README.zh-CN.md)

**Repository:** [Reimaging-Price-Trend-OHLC-Crypto](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto)

This repository reports two empirical studies that share the image-based convolutional design of Jiang, Kelly and Xiu (2023) in *The Journal of Finance* ([doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)). Study A varies the construction of daily equity bars under a fixed learning protocol. Study B holds that protocol fixed and replaces the equity universe with single-exchange cryptocurrency spot markets. Full one-minute archives, image tensors and model checkpoints remain on the experiment host; the repository distributes design specifications, result tables, interpretation notes and compact pure-Python utilities.

| Study | Experimental lever | Research question |
|-------|--------------------|-------------------|
| A. Equity OHLC representations | Daily bar geometry under raw, share-volume and dollar-volume expand and clip rules | Whether representation choices alter out-of-sample equity portfolio performance |
| B. Crypto asset-class transfer | Binance USDT spot cross-section with local retrain | Whether the same daily image specification retains cross-sectional ranking skill outside equities |
| C. Frozen US representation transfer | US raw, expand and clip weights applied to crypto OOS images | Whether equity-trained representation models transfer without retrain |

---

## Abstract

### Study A. Volume- and dollar-weighted OHLC geometry for US equities

Under a shared training and evaluation path from hfdata one-minute bars to greyscale OHLC images and five-seed CNNs, with in-sample years 1993–2002 and out-of-sample years 2003–2025, dollar-volume clip raises mean diagonal net Sharpe relative to raw by approximately 0.18. Expand constructions dominate the I60/R60 cell yet deteriorate I20/R20. Cross-sectional Rank IC differences across arms remain small; portfolio Sharpe is the principal surface on which representation effects appear.

Documentation: [docs/METHODS.md](docs/METHODS.md), [docs/INTERPRETATION.md](docs/INTERPRETATION.md), [results/RESULTS.md](results/RESULTS.md).

### Study B. Cryptocurrency spot retrain

The same grid \(I,R\in\{5,20,60\}\) is retrained on Binance USDT spot with in-sample years 2018–2021 and out-of-sample years 2022–2025. The primary cell I20/R20 yields Rank IC of −0.0495 and AUC of 0.450. For twenty-day horizons, I60/R20 attains Rank IC of 0.032 and the strongest zero-cost long–short Sharpe proxy in the matrix, yet remains well below equity-scale Rank IC levels near 0.05 in related US replications. The pattern is consistent with a shallow, short and highly co-moving cryptocurrency cross-section that does not support equity-like visual trend extraction.

Documentation: [docs/METHODS-crypto.md](docs/METHODS-crypto.md), [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md), [results/crypto/RESULTS.md](results/crypto/RESULTS.md).

### Study C. Frozen US raw, expand and clip transfer

Frozen US equity weights for raw, expand and clip score cryptocurrency OOS images with no gradient updates. On I20/R20 all three arms yield negative Rank IC, and none improves on cryptocurrency-local retrain failure at the same cell.

Documentation: [docs/METHODS-us-to-crypto-transfer.md](docs/METHODS-us-to-crypto-transfer.md), [results/crypto/transfer/RESULTS.md](results/crypto/transfer/RESULTS.md).

---

## Study A. Equity OHLC representations

### Portfolio net Sharpe on the diagonal under a ten-basis-point path

Entry is at the next session open; exit follows the planned open after horizon \(R\). Portfolios are equal-weight high-minus-low deciles. Sharpe ratios use \(\sqrt{252}\).

| Setting | raw | share expand | share clip | dollar expand | dollar clip |
|--------:|----:|-------------:|-----------:|--------------:|------------:|
| I5 / R5 | −0.40 | −0.30 | −0.18 | −0.31 | −0.07 |
| I20 / R20 | 3.07 | 1.36 | 1.89 | 1.42 | 3.13 |
| I60 / R60 | 4.37 | 6.37 | 4.33 | 6.26 | 4.52 |

Mean change in net Sharpe relative to raw across the three diagonal cells:

| Arm | Mean Δ |
|-----|--------:|
| share expand | +0.13 |
| share clip | −0.34 |
| dollar expand | +0.11 |
| dollar clip | +0.18 |

Dollar clip records the highest average improvement and is the only non-raw arm that does not collapse I20/R20. Expand concentrates gains at I60/R60. Horizon-dependent interpretation of expand is developed in [docs/INTERPRETATION.md](docs/INTERPRETATION.md). Complete tables appear in [results/RESULTS.md](results/RESULTS.md).

---

## Study B. Crypto asset-class transfer

### Design

| Element | Specification |
|---------|---------------|
| Market | Binance USDT spot; perpetual futures excluded |
| Data | One-minute klines aggregated to UTC daily OHLC |
| Universe | Point-in-time top 200 by lagged quote volume; identity breaks induce series splits |
| Sample | In-sample 2018–2021; out-of-sample 2022–2025 |
| Grid | \(I,R\in\{5,20,60\}\); formation step equal to \(R\) |
| Model | Jiang-style CNN; five seeds; ensemble mean probability |
| Reported metrics | Close-to-close Rank IC; zero-cost long–short Sharpe as an economic illustration only |

See [docs/METHODS-crypto.md](docs/METHODS-crypto.md), [docs/crypto-protocol.md](docs/crypto-protocol.md) and [configs/crypto_daily_reimaging_v1.yaml](configs/crypto_daily_reimaging_v1.yaml).

### Out-of-sample Rank IC matrix

Evaluation date 2026-07-24 on dual RTX 3090 hardware.

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | +0.034 | +0.026 |
| I20 | +0.018 | −0.049 | +0.002 |
| I60 | +0.009 | +0.032 | −0.009 |

Zero-cost close-to-close long–short Sharpe proxies include 1.36 for I60/R20, 0.72 for I5/R20 and −1.52 for I20/R20. The full matrix is in [results/crypto/RESULTS.md](results/crypto/RESULTS.md) and [results/crypto/tables/crypto_nine_cell_oos.csv](results/crypto/tables/crypto_nine_cell_oos.csv).

### Interpretation

Transfer of the equity specification fails at the primary cell. I20/R20 is the standard monthly-style workhorse in equity applications, yet here Rank IC is negative and classification AUC lies below one half. This is a negative confirmatory finding rather than mild attenuation of a positive signal.

For twenty-day labels, sixty-day image inputs are the most coherent positive configuration. I60/R20 matches near-maximal Rank IC and records the strongest long–short Sharpe proxy in the grid. The network appears to require visual history longer than the forecast horizon when any stable ranking structure is present. Equality of \(I\) and \(R\) is not privileged outside equities.

Even the strongest cryptocurrency cells remain weaker than equity benchmarks. Related US equity I20 ensembles report Rank IC near 0.05 with large multi-year high-minus-low Sharpes after costs. Cryptocurrency best Rank IC is near 0.03, unstable across the nine-cell grid, and estimated from only 72 non-overlapping twenty-day formation dates, with sixty-day formation limited to 23 dates.

A natural interpretation is limited cross-sectional depth. The eligible point-in-time book is capped at two hundred names, liquid history is concentrated after 2017, and instruments share exchange, quote asset and market-wide shocks. The resulting panel is thinner, shorter and more co-moving than equity universes on which Jiang-style image CNNs were developed. The claim is restricted to fit between this method and this market; it does not assert unpredictability of cryptocurrency returns under arbitrary models.

Extended discussion is in [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md).

---

## Study C. Frozen US raw, expand and clip transfer to cryptocurrency

United States equity checkpoints from the `purged_primary` raw, expand and clip arms score cryptocurrency out-of-sample images without gradient updates and without re-fitting United States train-only normalisation on cryptocurrency data. Expand and clip weights are applied to raw cryptocurrency images and are labeled as cross-representation transfer.

### Primary cell I20/R20 Rank IC

| Arm | Rank IC | ICIR | AUC | Rows |
|-----|--------:|-----:|----:|-----:|
| raw | −0.051 | −0.494 | 0.478 | 13852 |
| expand | −0.041 | −0.383 | 0.482 | 13852 |
| clip | −0.051 | −0.494 | 0.473 | 13852 |

Cryptocurrency-local retrain on the same cell records Rank IC of −0.0495. Frozen transfer does not reverse the primary-cell failure. Full tables and provenance: [results/crypto/transfer/RESULTS.md](results/crypto/transfer/RESULTS.md). Methods: [docs/METHODS-us-to-crypto-transfer.md](docs/METHODS-us-to-crypto-transfer.md). Interpretation: [docs/INTERPRETATION-us-to-crypto-transfer.md](docs/INTERPRETATION-us-to-crypto-transfer.md).

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
  METHODS.md
  INTERPRETATION.md
  METHODS-crypto.md
  INTERPRETATION-crypto.md
  crypto-protocol.md
  vwpq-clip-oc-protocol.md
  vwpq-dollar-protocol.md
configs/
  protocol_vwpq_clip_oc.json
  protocol_vwpq_dollar.json
  crypto_daily_reimaging_v1.yaml
  asset_exclusions_v1.json
results/
  RESULTS.md
  tables/
  json/
  crypto/
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
| Crypto minutes | Binance spot one-minute klines on the experiment host | No |
| This repository | Tables, protocols and pure-Python snapshots | Yes, Apache-2.0 |

Full citation wording is in [CITATIONS.md](CITATIONS.md).

---

## Statistical scope

Study A reports a shared monthly-block bootstrap for the expand arm as a secondary diagnostic in `results/json/final_summary.json`. Study B reports descriptive Rank IC, ICIR and zero-cost long–short Sharpe. No claim is made that all nine cryptocurrency cells are jointly positive; the primary I20/R20 cell alone rejects that narrative. The repository emphasises signed, setting-level movement in Study A and bounded transfer failure with a descriptive cell map in Study B.
