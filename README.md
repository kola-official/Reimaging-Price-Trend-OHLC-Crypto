# Re-imagining price-trend OHLC — equities & crypto

**Languages:** [English](README.md) · [中文](README.zh-CN.md)

**Repository:** [`Reimaging-Price-Trend-OHLC-Crypto`](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto)  
*(formerly `Reimaging-Price-Trend-OHLC-reasearch`)*

This repository packages **two related empirical studies** that share the image-CNN design language of Jiang, Kelly & Xiu (2023), *The Journal of Finance* ([doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)):

| Study | Lever | Question |
|-------|--------|----------|
| **A — Equity OHLC representations** | How the **bar is drawn** (raw / volume-weighted expand / clip) | Can representation choices improve US equity image signals? |
| **B — Crypto asset-class transfer** | How the **universe** changes (Binance USDT spot) | Does the same daily image recipe survive outside equities? |

Large artefacts (1-minute archives, image tensors, checkpoints) stay on the compute host and are **not** vendored here. What *is* here: design freezes, result tables, interpretation notes, and small pure-Python snapshots.

---

## Abstract (both studies)

### Study A — volume- and dollar-weighted OHLC geometry (US equities)

Five daily constructions under one training path (hfdata 1-minute → daily bars → greyscale images → five-seed CNNs; IS 1993–2002, OOS 2003–2025). **Dollar clip** raises mean diagonal net Sharpe versus raw by about **+0.18**; **expand** arms dominate **I60/R60** but hurt **I20/R20**. Rank IC gaps stay small—**portfolio Sharpe** carries the representation story.  
→ [Study A highlights](#study-a--equity-ohlc-representations) · [docs/METHODS.md](docs/METHODS.md) · [docs/INTERPRETATION.md](docs/INTERPRETATION.md)

### Study B — crypto spot retrain (asset-class transfer)

Same \(I,R\in\{5,20,60\}\) image CNNs, retrained on **Binance USDT spot** (IS 2018–2021, OOS 2022–2025). The **primary cell I20/R20 fails** (Rank IC **−0.0495**). Among 20-day forecasts, **I60/R20** is the most coherent positive cell (Rank IC **+0.032**, best LS Sharpe proxy), yet **still far weaker than equity replications**—consistent with a **thin, short, highly co-moving crypto book**.  
→ [Study B highlights](#study-b--crypto-asset-class-transfer) · [docs/METHODS-crypto.md](docs/METHODS-crypto.md) · [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md)

---

## Study A — equity OHLC representations

### Five-way portfolio net Sharpe (diagonal, common keys, 10 bp)

Path: next open entry / planned open exit; equal-weight high-minus-low; annualisation \(\sqrt{252}\).

| Setting | raw | share expand | share clip | dollar expand | **dollar clip** |
|--------:|----:|-------------:|-----------:|--------------:|----------------:|
| **I5 / R5** | −0.40 | −0.30 | −0.18 | −0.31 | **−0.07** |
| **I20 / R20** | 3.07 | 1.36 | 1.89 | 1.42 | **3.13** |
| **I60 / R60** | 4.37 | **6.37** | 4.33 | 6.26 | 4.52 |

**Mean Δ net Sharpe vs raw (three diagonal cells)**

| Arm | Mean Δ |
|-----|--------:|
| share expand | +0.13 |
| share clip | −0.34 |
| dollar expand | +0.11 |
| **dollar clip** | **+0.18** |

Full tables: [results/RESULTS.md](results/RESULTS.md). Horizon-dependent expand reading: [docs/INTERPRETATION.md](docs/INTERPRETATION.md).

---

## Study B — crypto asset-class transfer

### Design (concise)

| Item | Choice |
|------|--------|
| Market | Binance **USDT spot** only (no perps in v1) |
| Source | 1-minute klines → UTC daily OHLC |
| Universe | Point-in-time top-200 by lagged quote ADV; identity freeze (split at breaks) |
| IS / OOS | **2018–2021** / **2022–2025** |
| Grid | \(I,R\in\{5,20,60\}\) (nine cells); formation step \(=R\) |
| Model | Jiang-style CNN; five seeds; mean probability |
| Reported path | Close-to-close Rank IC; LS Sharpe is a **0 bp proxy** (not delayed VWAP) |

Methods: [docs/METHODS-crypto.md](docs/METHODS-crypto.md) · Protocol: [docs/crypto-protocol.md](docs/crypto-protocol.md) · Config: [configs/crypto_daily_reimaging_v1.yaml](configs/crypto_daily_reimaging_v1.yaml)

### Nine-cell OOS Rank IC (2026-07-24 CUDA audit)

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| **I5** | +0.014 | **+0.034** | +0.026 |
| **I20** | +0.018 | **−0.049** | +0.002 |
| **I60** | +0.009 | **+0.032** | −0.009 |

Selected economic proxies (0 bp, close-to-close decile LS Sharpe): **I60/R20 ≈ 1.36**, **I5/R20 ≈ 0.72**, **I20/R20 ≈ −1.52**.  
Full table: [results/crypto/RESULTS.md](results/crypto/RESULTS.md) · CSV: [results/crypto/tables/crypto_nine_cell_oos.csv](results/crypto/tables/crypto_nine_cell_oos.csv)

### How to read Study B (interpretation first)

1. **Transfer of the equity recipe fails at the primary cell.**  
   I20/R20 is the natural monthly-style workhorse in equity work; here Rank IC is **negative** and AUC is **below 0.5**. This is a **negative confirmatory result**, not a mild attenuation.

2. **When medium-horizon ranking is least fragile, longer lookback wins.**  
   For **20-day** labels, **60-day images (I60/R20)** match near-best Rank IC and post the **best** LS Sharpe proxy—i.e. the network appears to need a **longer visual history** than the forecast horizon. Canonical I20 context is not privileged.

3. **Even the best crypto cells underperform equity-scale benchmarks.**  
   Related US equity I20 pipelines report Rank IC on the order of **~0.05** with large multi-year H–L Sharpes after costs. Crypto’s best Rank IC (~0.03) is smaller, grid-unstable, and estimated on **72** non-overlapping R20 dates (R60 only **23**).

4. **Working hypothesis: the crypto book is “too small” for this method.**  
   More precisely: a **shallow, short, highly co-moving** point-in-time cross-section (top-200, post-2017 liquidity, shared exchange/quote shocks) does not supply the panel mass that Jiang-style image CNNs exploit in equities. This is a hypothesis about **method × market fit**, not a claim that crypto is unpredictable under every model.

Full write-up: [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md).

---

## Repository layout

```text
README.md / README.zh-CN.md
CITATIONS.md · CITATION.cff · NOTICE · LICENSE (Apache-2.0)
docs/
  METHODS.md                  ← Study A (equity representations)
  INTERPRETATION.md           ← Study A horizon/expand reading
  METHODS-crypto.md           ← Study B design & split
  INTERPRETATION-crypto.md    ← Study B scientific reading
  crypto-protocol.md
  vwpq-*.md                   ← Study A representation protocols
configs/
  protocol_vwpq_*.json        ← Study A
  crypto_daily_reimaging_v1.yaml · asset_exclusions_v1.json
results/
  RESULTS.md · tables/ · json/          ← Study A
  crypto/RESULTS.md · tables/ · json/   ← Study B
src_snapshot/
  hfdata/                     ← expand/clip transforms (Study A)
  crypto/                     ← formation, metrics, execution helpers (Study B)
```

---

## Data & code citations (summary)

| Layer | Source | Redistributed here? |
|-------|--------|---------------------|
| Method paper | Jiang, Kelly & Xiu (2023), *JF* | No (cite only) |
| Equity minutes | HF Data Library US 1m ([Hugging Face](https://huggingface.co/datasets/elkassabgi/hfdatalibrary)) | No |
| Paper’s equities | CRSP via WRDS | No |
| Crypto minutes | Binance spot 1m klines (experiment host inventory) | No |
| This repo | Tables, protocols, small Python snapshots | Yes (Apache-2.0) |

Authoritative wording: [CITATIONS.md](CITATIONS.md).

---

## Inference appendix (secondary)

Study A reports a shared bootstrap for the expand arm as a **diagnostic** (see `results/json/final_summary.json`).  
Study B reports **descriptive** Rank IC / ICIR / proxy Sharpe; it does **not** claim one-sided 5% “all cells positive” confirmation—primary I20/R20 alone rejects that narrative.

Emphasis of this repository remains **signed, setting-level movement** (Study A) and **honest transfer failure + cell map** (Study B).
