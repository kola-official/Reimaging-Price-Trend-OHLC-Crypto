# Results for Study B: cryptocurrency spot retrain

**Evaluation date:** 2026-07-24  
**Compute host:** dual NVIDIA GeForce RTX 3090  
**Machine-readable source:** [json/crypto_oos_metrics_audit_2026-07-24.json](json/crypto_oos_metrics_audit_2026-07-24.json)  
**Tabular source:** [tables/crypto_nine_cell_oos.csv](tables/crypto_nine_cell_oos.csv)

## Evaluation design

| Element | Specification |
|---------|---------------|
| Scores | Five-seed mean up-probability from cryptocurrency-local retrain |
| Rank IC | Mean cross-sectional Spearman correlation with close-to-close \(R\)-day return |
| Long–short Sharpe | Top-minus-bottom decile, equal weight, zero cost, annualised by \(\sqrt{365/R}\) |
| Fills | Close-to-close |
| Formation | Non-overlapping with step \(R\) |
| Out-of-sample window | 2022-01-01 to 2025-12-31 |

Figures below are ranking diagnostics for the confirmatory retrain question. They are not net-of-cost claims of implementable alpha under delayed execution.

---

## Nine-cell out-of-sample matrix

| Cell | Rows | IC dates | Rank IC | ICIR | AUC | LS Sharpe | MaxDD |
|------|-----:|---------:|--------:|-----:|----:|----------:|------:|
| i5_r5 | 56087 | 291 | +0.0137 | 0.158 | 0.504 | +0.23 | −0.48 |
| i5_r20 | 13854 | 72 | +0.0337 | 0.332 | 0.532 | +0.72 | −0.30 |
| i5_r60 | 4430 | 23 | +0.0265 | 0.269 | 0.546 | −0.23 | −0.59 |
| i20_r5 | 56077 | 291 | +0.0183 | 0.186 | 0.512 | +0.03 | −0.61 |
| i20_r20 | 13852 | 72 | −0.0495 | −0.474 | 0.450 | −1.52 | −0.87 |
| i20_r60 | 4430 | 23 | +0.0021 | 0.017 | 0.509 | +0.16 | −0.42 |
| i60_r5 | 55997 | 291 | +0.0092 | 0.101 | 0.506 | −0.09 | −0.68 |
| i60_r20 | 13832 | 72 | +0.0323 | 0.359 | 0.503 | +1.36 | −0.32 |
| i60_r60 | 4424 | 23 | −0.0092 | −0.094 | 0.493 | +0.03 | −0.35 |

Long–short Sharpe and maximum drawdown use the zero-cost close-to-close path defined above.

### Rank IC summary

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | +0.034 | +0.026 |
| I20 | +0.018 | −0.049 | +0.002 |
| I60 | +0.009 | +0.032 | −0.009 |

---

## Principal findings

The confirmatory primary cell I20/R20 fails. Negative Rank IC and AUC below one half reject the claim that the equity monthly-style specification transfers intact to cryptocurrency spot.

Twenty-day forecasts are strongest under non-I20 image lengths. Both I5 and I60 inputs dominate I20 on Rank IC at \(R=20\). I60/R20 additionally records the strongest long–short Sharpe proxy, so that a sixty-day visual lookback is the most coherent positive medium-horizon cell.

Performance remains far from equity benchmarks. Local US equity I20 ensembles report Rank IC near 0.05 with large multi-year high-minus-low Sharpes after costs. Cryptocurrency best Rank IC is near 0.03, unstable across the grid, and estimated on a much shorter book. Interpretation is developed in [docs/INTERPRETATION-crypto.md](../../docs/INTERPRETATION-crypto.md).

Cells at \(R=60\) rest on only twenty-three non-overlapping formation dates and are statistically fragile; single-cell signs at that horizon should not be over-interpreted.

---

## Engineering controls

| Control | Outcome |
|---------|---------|
| Author renderer pixel parity for I5, I20 and I60 | Pass on pinned cases |
| Parameter counts | 155,138 / 708,866 / 2,952,962 |
| Five-seed strict load during out-of-sample scoring | Pass |
| Shuffled-label in-sample negative control for I20 | Near-zero Rank IC |
| Identity freeze | Seven of seven events handled by split at break |

---

## Files

```text
results/crypto/
  RESULTS.md
  tables/crypto_nine_cell_oos.csv
  json/crypto_oos_metrics_audit_2026-07-24.json
```


---

## Related Study C: frozen US transfer

Zero-shot application of US raw, expand and clip checkpoints to the same cryptocurrency OOS keys is reported in [transfer/RESULTS.md](transfer/RESULTS.md). On I20/R20 all three transferred arms have negative Rank IC and do not improve upon the cryptocurrency-local retrain Rank IC of −0.0495.
