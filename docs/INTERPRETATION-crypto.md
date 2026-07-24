# Interpretation of Study B: cryptocurrency image-CNN retrain

Numbers are from [results/crypto/](../results/crypto/), evaluated on 2026-07-24 with dual RTX 3090 hardware. Market-structure statements are interpretive hypotheses, not identified causal mechanisms. Repository spine: [SCIENTIFIC-OVERVIEW.md](SCIENTIFIC-OVERVIEW.md).

---

## 1. Empirical regularities

The primary design cell I20/R20 fails. Rank IC equals −0.0495 and AUC equals 0.450. In equity applications this cell is the conventional monthly-style panel; under cryptocurrency retrain it is the weakest configuration in the grid.

Medium-horizon ranking does not favour I20 inputs. For twenty-day forecasts the strongest Rank IC values are 0.034 for I5/R20 and 0.032 for I60/R20. On the zero-cost long–short Sharpe proxy, I60/R20 leads at 1.36, while I5/R20 is 0.72.

The nine-cell grid is heterogeneous. Several cells are near zero or negative, including I20/R20 and I60/R60. Rank IC does not increase monotonically with horizon \(R\).

Magnitudes remain below equity benchmarks from related pipelines. Local US equity I20 ensembles report monthly Rank IC near 0.05 with economically large high-minus-low Sharpes after costs on multi-decade samples. The strongest cryptocurrency Rank IC values are near 0.03 on a short out-of-sample window, and the primary cell is negative.

### Rank IC matrix

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | +0.034 | +0.026 |
| I20 | +0.018 | −0.049 | +0.002 |
| I60 | +0.009 | +0.032 | −0.009 |

---

## 2. Medium horizons and lookback length

Equity practice often pairs I20 images with R20 labels. Under cryptocurrency retrain that pairing fails. Sixty-day images used to forecast twenty-day returns rank among the highest Rank IC cells, deliver the highest long–short Sharpe proxy, and rest on seventy-two out-of-sample formation dates rather than the twenty-three dates available at \(R=60\).

When stable cross-sectional structure is present, the network appears to require visual history longer than the forecast horizon. That reading is consistent with path-level features such as multi-week drift and range regimes. Study A likewise finds that long visual windows are where representation choices move portfolio outcomes most; the parallel here is weaker, because even the best cryptocurrency cell remains a modest ranking edge rather than an equity-scale signal.

I60/R20 is not a trading recommendation. Transaction costs, delayed VWAP execution and multiplicity across nine cells are not closed in the reported path.

Reversal at I20/R20 admits several non-exclusive accounts: common-shock dominance and regime noise over twenty-day windows; mismatch between medium labels and intermediate lookbacks; and a four-year in-sample window with early stopping and near-zero validation MCC, consistent with thin signal before out-of-sample evaluation.

---

## 3. Comparison with equities

Jiang et al. (2023) document transfer of image CNNs across international equities and time scales. Study B replaces equities with cryptocurrency spot.

| Dimension | US equities in related pipelines | Cryptocurrency spot here |
|-----------|----------------------------------|--------------------------|
| Cross-section depth | Thousands of names over decades | Top 200 eligible; effective \(N\) often 50–200 |
| History | Multi-decade daily panels | Liquid history concentrated after 2017; in-sample 2018–2021 |
| Session structure | Shared regular trading hours | Continuous UTC days |
| Primary I20/R20 | Positive Rank IC and large high-minus-low performance | Negative Rank IC |
| Best cells | Strong diagonal economics in Study A | Weak and scattered; best Rank IC near 0.03 |

The study does not obtain a confirmatory replication of Jiang-style image predictability on cryptocurrency spot. Primary-cell failure and the gap relative to equity Rank IC support a **negative transfer** result for this method family.

---

## 4. Limited cross-sectional depth

A structural reading emphasises panel geometry rather than a slogan about market size.

Decile sorts require at least fifty names, and many formation days sit near that floor, raising estimation noise relative to deep equity books. Non-overlapping twenty-day formation yields seventy-two out-of-sample dates; sixty-day formation yields twenty-three. Detecting Rank IC of 0.02–0.03 with high confidence is intrinsically difficult under such sparse formation. Spot USDT instruments share exchange, quote asset and market-wide shocks, reducing residual idiosyncrasy that cross-sectional image features require. Redenominations, delistings and continuous-session gaps force series splits and blank columns, further thinning clean panel mass.

Under this reading, the tradable, clean, point-in-time cross-section is too thin and too short for Jiang-style image CNNs to recover equity-like predictability. The statement concerns method–market fit, not unpredictability under arbitrary models.

---

## 5. Scope and synthesis

The results do not establish strong-form informational efficiency of cryptocurrency markets. They do not imply failure of every learning method on this asset class. They do not establish I60/R20 as an implementable strategy under costs and delayed execution. They do not claim numerical equality with the CRSP-based tables of Jiang et al. (2023).

**Synthesis.** Holding the Jiang–Kelly–Xiu image CNN fixed and replacing only the universe with Binance USDT spot, Study B finds no reliable primary-cell predictability. Among medium-horizon forecasts, sixty-day image context at I60/R20 is the most coherent positive cell on portfolio-style metrics and near-best on Rank IC, yet remains far weaker than equity replications. Together with Study C, the scientific contribution is a **bounded negative result on asset-class transfer**, with a descriptive map of which \((I,R)\) cells remain least fragile.
