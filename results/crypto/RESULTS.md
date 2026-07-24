# Crypto study results (Study B)

**Audit date:** 2026-07-24  
**Host:** `DeadLine` (2× RTX 3090)  
**Machine-readable source:** [`json/crypto_oos_metrics_audit_2026-07-24.json`](json/crypto_oos_metrics_audit_2026-07-24.json)  
**Flat table:** [`tables/crypto_nine_cell_oos.csv`](tables/crypto_nine_cell_oos.csv)

## Evaluation path (read before the table)

| Item | Setting |
|------|---------|
| Scores | Five-seed mean \(P(\mathrm{up})\) from crypto-local retrain |
| Rank IC | Mean cross-sectional Spearman vs close-to-close \(R\)-day return |
| LS Sharpe | Top−bottom decile, equal weight, **0 bp** cost, annualised \(\sqrt{365/R}\) (**proxy**) |
| Fills | Close-to-close (not delayed VWAP) |
| Formation | Non-overlapping, step \(= R\) |
| OOS window | 2022-01-01 → 2025-12-31 |

These figures are **ranking / diagnostic** results for the confirmatory retrain question. They are **not** a claim of net-of-cost tradable alpha.

---

## Nine-cell out-of-sample matrix

| Cell | Rows | IC dates | Rank IC | ICIR | AUC | LS Sharpe* | MaxDD* |
|------|-----:|---------:|--------:|-----:|----:|-----------:|-------:|
| i5_r5 | 56087 | 291 | +0.0137 | 0.158 | 0.504 | +0.23 | −0.48 |
| i5_r20 | 13854 | 72 | **+0.0337** | 0.332 | 0.532 | +0.72 | −0.30 |
| i5_r60 | 4430 | 23 | +0.0265 | 0.269 | 0.546 | −0.23 | −0.59 |
| i20_r5 | 56077 | 291 | +0.0183 | 0.186 | 0.512 | +0.03 | −0.61 |
| **i20_r20** | 13852 | 72 | **−0.0495** | **−0.474** | **0.450** | **−1.52** | **−0.87** |
| i20_r60 | 4430 | 23 | +0.0021 | 0.017 | 0.509 | +0.16 | −0.42 |
| i60_r5 | 55997 | 291 | +0.0092 | 0.101 | 0.506 | −0.09 | −0.68 |
| **i60_r20** | 13832 | 72 | **+0.0323** | **0.359** | 0.503 | **+1.36** | −0.32 |
| i60_r60 | 4424 | 23 | −0.0092 | −0.094 | 0.493 | +0.03 | −0.35 |

\*LS Sharpe / MaxDD use the zero-cost close-to-close proxy defined above.

### Rank IC heatmap (same numbers)

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | **+0.034** | +0.026 |
| I20 | +0.018 | **−0.049** | +0.002 |
| I60 | +0.009 | **+0.032** | −0.009 |

---

## How to read the results

1. **Confirmatory primary cell (I20/R20) fails.**  
   Negative Rank IC and sub-0.5 AUC reject a simple “equity recipe works on crypto” claim for the default monthly-style setting.

2. **Best 20-day forecasts use non-I20 context.**  
   For \(R=20\), **I5** and **I60** images both beat I20 on Rank IC. **I60/R20** additionally shows the strongest LS Sharpe proxy—i.e. *if* one emphasises medium-horizon ranking, **a 60-day visual lookback is the most coherent positive cell**, not the canonical I20 panel.

3. **Still far from equity performance.**  
   Local US equity I20 ensembles report Rank IC ≈ **0.05** with large multi-year H–L Sharpes after costs. Crypto’s best Rank IC (~0.03) is smaller, unstable across the grid, and obtained on a much shorter book. See [docs/INTERPRETATION-crypto.md](../../docs/INTERPRETATION-crypto.md).

4. **R60 cells are statistically fragile.**  
   Only ~23 non-overlapping formation dates; signs can flip with small design changes. Do not over-interpret I5/R60 AUC or single-cell LS signs.

---

## Engineering controls (supporting, not alpha)

| Control | Outcome |
|---------|---------|
| Author renderer pixel parity (I5/I20/I60) | Pass on pinned cases |
| Parameter counts | 155,138 / 708,866 / 2,952,962 exact |
| Five-seed strict load on OOS audit | Pass |
| Shuffled-label IS negative control (I20) | Near-zero Rank IC (engineering workspace) |
| Identity freeze v1 | 7/7 split-at-break |

---

## Files

```text
results/crypto/
  RESULTS.md                          ← this file
  tables/crypto_nine_cell_oos.csv
  json/crypto_oos_metrics_audit_2026-07-24.json
```
