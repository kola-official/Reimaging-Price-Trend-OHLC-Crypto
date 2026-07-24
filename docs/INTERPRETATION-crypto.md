# Interpretation of cryptocurrency image-CNN results

This note interprets the nine-cell out-of-sample matrix for cryptocurrency spot retrain. Numerical values are those reported in [results/crypto/](../results/crypto/) from the 2026-07-24 evaluation on dual RTX 3090 hardware. Statements about market structure are interpretive and are not identified causal mechanisms.

---

## 1. Empirical regularities

### 1.1 Main facts

The primary design cell I20/R20 fails. Rank IC equals −0.0495 and AUC equals 0.450. In equity applications this cell is the conventional monthly-style panel; in the cryptocurrency retrain it is the weakest configuration in the grid.

Medium-horizon ranking does not favour I20 inputs. For twenty-day forecasts the strongest Rank IC values are 0.034 for I5/R20 and 0.032 for I60/R20. On the zero-cost long–short Sharpe proxy, I60/R20 leads at 1.36, while I5/R20 is 0.72.

The nine-cell grid is heterogeneous. Several cells are near zero or negative, including I20/R20 and I60/R60. There is no pattern in which all cells are positive and increase monotonically with horizon \(R\).

Magnitudes remain below equity benchmarks from related pipelines. Local US equity I20 ensembles report monthly Rank IC near 0.05 with economically large high-minus-low Sharpes after costs on multi-decade samples. The strongest cryptocurrency Rank IC values are near 0.03 on a short out-of-sample window, and the primary cell is negative.

### 1.2 Rank IC matrix

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | +0.034 | +0.026 |
| I20 | +0.018 | −0.049 | +0.002 |
| I60 | +0.009 | +0.032 | −0.009 |

---

## 2. Longer lookback for medium-horizon forecasts

### 2.1 The I60/R20 configuration

Equity practice often treats I20/R20 as the workhorse pairing of image length and forecast horizon. In cryptocurrency retrain that cell is the worst. By contrast, sixty-day images used to forecast twenty-day returns rank among the highest Rank IC cells, deliver the highest long–short Sharpe proxy in the audit, and rest on seventy-two out-of-sample formation dates rather than the twenty-three dates available at \(R=60\).

When stable cross-sectional structure is present, the network appears to require visual history longer than the forecast horizon. That reading is consistent with path-level features such as multi-week drift and range regimes mattering more than short local motifs. Study A likewise finds that long visual windows are where representation choices move portfolio outcomes most; here the parallel is weaker, because even the best cryptocurrency cell remains a modest ranking edge rather than an equity-scale signal.

I60/R20 is not advanced as a trading recommendation. Transaction costs, delayed VWAP execution and multiplicity across nine cells are not closed in the reported path.

### 2.2 Reversal at I20/R20

Several non-exclusive accounts are consistent with the data. First, twenty-day cryptocurrency charts may be dominated by common shocks and regime noise, so that the CNN overfits in-sample idiosyncrasies and ranks the wrong names out of sample. Second, medium-horizon labels may require either short motifs as in I5 or long context as in I60; equality of \(I\) and \(R\) need not be privileged outside equities. Third, the in-sample window spans only four calendar years, early stopping often terminates within three to five epochs, and validation MCC remains near zero, which is consistent with thin signal even before out-of-sample evaluation.

---

## 3. Comparison with equities

Jiang et al. (2023) document transfer of image CNNs across international equities and across time scales. The present confirmatory change replaces equities with cryptocurrency spot.

| Dimension | US equities in related pipelines | Cryptocurrency spot in this study |
|-----------|----------------------------------|-----------------------------------|
| Cross-section depth | Thousands of names over decades | Top 200 eligible; effective \(N\) often 50–200 |
| History | Multi-decade daily panels | Liquid history concentrated after 2017; in-sample 2018–2021 |
| Session structure | Shared regular trading hours | Continuous UTC days |
| Primary I20/R20 | Positive Rank IC and large high-minus-low performance in local replications | Negative Rank IC |
| Best cells | Strong diagonal economics in Study A | Weak and scattered; best Rank IC near 0.03 |

The study does not obtain a confirmatory replication of Jiang-style image predictability on cryptocurrency spot. Failure of the primary cell and the gap relative to equity Rank IC levels support a negative transfer result: the equity image specification is not automatically portable to this market.

---

## 4. Limited cross-sectional depth

The informal observation that the cryptocurrency book is too small can be stated more precisely along four dimensions.

Decile sorts require at least fifty names, and many formation days sit near that floor. Equity studies sort far deeper books, so estimation noise in rank correlations and decile means is larger here.

Non-overlapping twenty-day formation yields seventy-two out-of-sample dates; sixty-day formation yields twenty-three. Equity out-of-sample windows span decades of weekly or monthly points. Detecting Rank IC of 0.02–0.03 with high confidence is intrinsically difficult under such sparse formation.

Spot USDT instruments share exchange, quote asset and market-wide shocks. If residual idiosyncratic variation is small, cross-sectional image features have limited ranking work even when individual series exhibit trends.

Redenominations, delistings and continuous-session gaps force series splits and blank image columns. Those issues are handled in the pipeline, yet they further reduce clean panel mass relative to CRSP-style equities.

Under this reading, the tradable, clean, point-in-time cross-section is too thin and too short for Jiang-style image CNNs to recover equity-like predictability. The statement concerns fit between method and market; it does not assert that no cryptocurrency signal can exist under any model or horizon.

---

## 5. Scope of claims

The results do not establish strong-form informational efficiency of cryptocurrency markets. They do not imply failure of every learning method on this asset class. They do not establish I60/R20 as a deployable strategy under costs and delayed execution. They do not claim numerical equality with the CRSP-based tables of Jiang et al. (2023).

---

## 6. Synthesis

Holding the Jiang–Kelly–Xiu image CNN fixed and replacing only the universe with Binance USDT spot, the study finds no reliable primary-cell predictability: I20/R20 ranks inversely out of sample. Among medium-horizon forecasts, sixty-day image context at I60/R20 is the most coherent positive cell on portfolio-style metrics and near-best on Rank IC, yet remains far weaker than equity replications. The pattern is consistent with a small, short and highly co-moving cross-section that does not support equity-scale visual trend extraction. The scientific contribution of Study B is therefore a bounded negative result on asset-class transfer, together with a descriptive map of which \((I,R)\) cells remain least fragile.
