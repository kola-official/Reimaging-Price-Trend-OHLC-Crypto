# Results for Study C: frozen US raw, expand and clip models on cryptocurrency OOS

**Evaluation date:** 2026-07-24  
**Compute:** dual NVIDIA GeForce RTX 3090  
**Mode:** direct frozen transfer; no US weight updates; no US normalisation re-fit on cryptocurrency  

Machine-readable sources:

- [us_to_crypto_direct_transfer_i20_r20.json](us_to_crypto_direct_transfer_i20_r20.json)
- [us_to_crypto_direct_transfer_i20_r20.csv](us_to_crypto_direct_transfer_i20_r20.csv)
- [us_to_crypto_direct_transfer_diagonal.json](us_to_crypto_direct_transfer_diagonal.json)
- [provenance_i20_r20.json](provenance_i20_r20.json)

Methods: [docs/METHODS-us-to-crypto-transfer.md](../../../docs/METHODS-us-to-crypto-transfer.md).  
Interpretation: [docs/INTERPRETATION-us-to-crypto-transfer.md](../../../docs/INTERPRETATION-us-to-crypto-transfer.md).

---

## Evaluation path

| Element | Specification |
|---------|---------------|
| US arms | raw; expand as `vwpq`; clip as `vwpq_clip` |
| US checkpoints | `purged_primary/{arm}/i20_r20/seed{0–4}/best_checkpoint.pt` |
| Crypto images | Author-exact raw OHLC OOS tensors; identical keys for all arms |
| Scores | Five-seed mean up-probability |
| Rank IC | Mean cross-sectional Spearman correlation with close-to-close \(R\)-day return |
| Costs | Zero in the reported path |
| Geometry match | raw matched; expand and clip are cross-representation on raw crypto images |

---

## Primary cell I20/R20

| Arm | Rows | IC dates | Rank IC | ICIR | AUC | LS Sharpe proxy |
|-----|-----:|---------:|--------:|-----:|----:|----------------:|
| raw | 13852 | 72 | -0.0510 | -0.494 | 0.478 | -1.68 |
| expand | 13852 | 72 | -0.0411 | -0.383 | 0.482 | -1.25 |
| clip | 13852 | 72 | -0.0514 | -0.494 | 0.473 | -1.45 |

All three arms share 13,852 prediction rows on the same formation dates.

### Comparison with cryptocurrency-local retrain on I20/R20

| Source | Rank IC | AUC |
|--------|--------:|----:|
| Crypto-local retrain, Study B | −0.0495 | 0.450 |
| US raw frozen transfer | −0.0510 | 0.478 |
| US expand frozen transfer | −0.0411 | 0.482 |
| US clip frozen transfer | −0.0514 | 0.473 |

Frozen US transfer does not rescue the primary cell. Expand is the least negative of the three transferred arms but remains clearly below zero and does not approach equity-scale Rank IC near 0.05 from related US pipelines.

---

## Diagonal extension

| Cell | raw Rank IC | expand Rank IC | clip Rank IC |
|------|------------:|---------------:|-------------:|
| I5/R5 | -0.0078 | -0.0071 | -0.0103 |
| I20/R20 | -0.0510 | -0.0411 | -0.0514 |
| I60/R60 | -0.0198 | -0.0213 | -0.0179 |

Every diagonal cell is negative for every transferred arm under the reported path.

---

## Principal findings

Direct transfer of frozen US raw, expand and clip models fails to produce positive out-of-sample Rank IC on cryptocurrency spot for the primary I20/R20 cell. The result aligns with Study B retrain failure at the same cell and strengthens the asset-class transfer boundary: neither local retrain nor frozen US equity weights recover equity-like image ranking skill on this cryptocurrency sample.

Representation choice among the three US arms does not overturn the sign of the primary-cell Rank IC. Expand is slightly less negative than raw and clip on I20/R20, but the gap is small relative to the distance from equity benchmarks.

Expand and clip results must be read as cross-representation scores on raw cryptocurrency images. That design is disclosed in the metrics schema and does not claim matched expand or clip cryptocurrency geometry.
