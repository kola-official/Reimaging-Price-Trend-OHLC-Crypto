# Methods for Study C: frozen US representation arms transferred to cryptocurrency

Scientific overview: [SCIENTIFIC-OVERVIEW.md](SCIENTIFIC-OVERVIEW.md).  
Study A: [METHODS.md](METHODS.md). Study B: [METHODS-crypto.md](METHODS-crypto.md).

## Citations

Primary methodological reference: Jiang, Kelly and Xiu (2023), *The Journal of Finance*, [doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268).  
Equity representation results: [results/RESULTS.md](../results/RESULTS.md).  
Cryptocurrency retrain results: [results/crypto/RESULTS.md](../results/crypto/RESULTS.md).  
Data and code register: [CITATIONS.md](../CITATIONS.md).

This study evaluates zero-shot asset-class transfer. United States equity image-CNN weights trained under Study A representation arms are applied to cryptocurrency out-of-sample images without gradient updates and without re-estimating United States train-only normalisation on cryptocurrency data.

---

## 1. Research question

Study A compares raw, volume-weighted expand and volume-weighted clip bar geometries for US equities. Study B retrains Jiang-style CNNs on Binance USDT spot. Study C asks whether frozen US equity weights from those representation arms retain cross-sectional ranking skill when scored on cryptocurrency spot images.

The experiment is direct frozen transfer. It is neither cryptocurrency retrain nor fine-tuning.

---

## 2. United States source models

| Element | Specification |
|---------|---------------|
| Training protocol | `purged_primary` on hfdata US one-minute equities |
| Host root | `/share/home/user/snliu/price_trends_workspace/outputs/hfdata/purged_primary` |
| Arms | `raw`; `vwpq` reported as expand; `vwpq_clip` reported as clip |
| Primary cell | I20/R20 with five seeds |
| Diagonal extension | I5/R5 and I60/R60 where checkpoints exist |
| Checkpoint schema | `best_checkpoint.pt` containing `model` state dict, `mean`, `std`, `I`, `R`, `seed` |
| Normalisation | Per-seed train-only scalar mean and standard deviation stored with the checkpoint |

Dollar-volume arms are optional and are not required for the primary three-arm report.

---

## 3. Cryptocurrency evaluation sample

| Element | Specification |
|---------|---------------|
| Market | Binance USDT spot |
| Images | Author-exact greyscale OHLC with moving average and volume |
| Primary dataset | `data/crypto/i20_r20_oos` |
| Out-of-sample window | 2022-01-01 to 2025-12-31 |
| Labels and returns | Close-to-close \(R\)-day returns in dataset metadata |
| Formation | Non-overlapping step equal to \(R\) |
| Shared keys | All three arms score the identical cryptocurrency OOS image binary and metadata rows |

### Representation geometry note

Cryptocurrency OOS assets available on the host are raw author-exact images. The raw arm is geometry-matched. Expand and clip US weights are therefore scored on raw cryptocurrency images. That cross-representation transfer is intentional and is labeled in the metrics artifacts as `cross_representation_us_expand_or_clip_weights_on_crypto_raw_images`. Matched cryptocurrency expand or clip image construction would be required for a pure within-representation comparison and is outside this freeze.

---

## 4. Scoring protocol

1. Load each of five US seeds for arm \(a\) and cell \((I,R)\).  
2. Build the corresponding Jiang-style CNN with `build_model(I)`.  
3. Load the frozen state dict with `strict=True`.  
4. Set `eval` mode and disable `requires_grad` on all parameters.  
5. Standardise cryptocurrency images with the **US** seed mean and standard deviation from the checkpoint, never with cryptocurrency train or OOS statistics.  
6. Predict up-probability under `torch.inference_mode` with zero optimizer steps.  
7. Ensemble by equal-weight average across seeds.  
8. Compute Rank IC as the mean over formation dates of the Spearman correlation between ensemble scores and forward returns; report ICIR, AUC and a zero-cost long–short Sharpe proxy for comparison with Study B.

Implementation entry point: `scripts/transfer_us_arms_to_crypto_frozen.py` in the cryptocurrency engineering workspace; snapshot under [src_snapshot/crypto/transfer_us_arms_to_crypto_frozen.py](../src_snapshot/crypto/transfer_us_arms_to_crypto_frozen.py).

---

## 5. Freeze invariants

| Flag | Required value |
|------|----------------|
| `transfer_mode` | `direct_frozen_us_weights` |
| `retrain` | false |
| `fine_tune` | false |
| `us_weights_updated_on_crypto` | false |
| `us_normalization_refit_on_crypto` | false |
| `gradient_updates` | 0 |
| `optimizer_steps` | 0 |

Unit tests of these invariants live with the engineering package and are snapshotted under `src_snapshot/crypto/test_us_to_crypto_transfer_freeze.py`.

---

## 6. Outputs

| Artifact | Path |
|----------|------|
| Primary I20/R20 metrics | [results/crypto/transfer/us_to_crypto_direct_transfer_i20_r20.json](../results/crypto/transfer/us_to_crypto_direct_transfer_i20_r20.json) |
| Primary table | [results/crypto/transfer/us_to_crypto_direct_transfer_i20_r20.csv](../results/crypto/transfer/us_to_crypto_direct_transfer_i20_r20.csv) |
| Diagonal extension | [results/crypto/transfer/us_to_crypto_direct_transfer_diagonal.json](../results/crypto/transfer/us_to_crypto_direct_transfer_diagonal.json) |
| Provenance | [results/crypto/transfer/provenance_i20_r20.json](../results/crypto/transfer/provenance_i20_r20.json) |
| Results narrative | [results/crypto/transfer/RESULTS.md](../results/crypto/transfer/RESULTS.md) |
