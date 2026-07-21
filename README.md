# Re-imagining price-trend OHLC representations

**Repository:** `Reimaging-Price-Trend-ohcl-reasearch`  
**Focus:** Can volume-weighted high–low construction improve CNN-based equity trend signals relative to standard daily OHLC bars?

This repository packages the **empirical results** of a three-arm study on US equities (hfdata 1-minute source → daily bars → candlestick images → CNN ensembles). The narrative below emphasises **where representation choices move portfolio performance**, and places formal inference in a secondary role.

---

## Abstract

We compare three daily bar constructions under a shared training and evaluation protocol:

| Arm | What changes in the image |
|-----|---------------------------|
| **raw** | Standard open / high / low / close / volume |
| **expand** | Open, close and volume fixed to raw; high/low from volume-weighted quantiles, **expanded** so that open and close remain inside the range |
| **clip** | High/low from the same quantiles; open/close **clipped** into that band when they fall outside |

Models are image CNNs in the spirit of *Re-Imag(in)ing Price Trends* (Jiang et al.), trained on 1993–2002 and evaluated on 2003–2025. Labels, moving averages and trade fills remain **raw** prices; only the drawn OHLC geometry differs.

**Main empirical takeaways**

1. **Economic path (10 bp one-way costs, next-open long–short):** on the diagonal image/horizon settings, **expand raises mean net Sharpe versus raw by about +0.13**. The gain is concentrated in the **I60/R60** configuration (**+2.00** net Sharpe) and is also visible at **I5/R5** (**+0.10**).  
2. **clip** improves **I5/R5** net Sharpe relative to both raw and expand (**clip −0.18** vs raw **−0.40** and expand **−0.30**), and improves **I20/R20** versus expand (**+0.53** Sharpe), but **does not** raise the three-setting average versus raw.  
3. Cross-sectional ranking skill (Rank IC) is **mixed** across settings; representation effects are **more visible in the portfolio Sharpe path** than in average Rank IC.

Formal bootstrap diagnostics for the expand arm are included under [results/](results/) for completeness; they are **not** the centre of this report.

---

## Highlights (where performance moves)

### Portfolio net Sharpe (diagonal, common keys, 10 bp)

Path: next open entry / planned open exit (frozen exit proxy when needed); equal-weight high-minus-low deciles; annualisation \(\sqrt{252}\).

| Setting (image days × hold days) | raw | expand | clip | expand − raw | clip − raw |
|----------------------------------:|----:|-------:|-----:|-------------:|-----------:|
| **I5 / R5** (weekly-style) | −0.40 | −0.30 | **−0.18** | **+0.10** | **+0.21** |
| **I20 / R20** (monthly-style) | 3.07 | 1.36 | 1.89 | −1.71 | −1.18 |
| **I60 / R60** (quarterly-style) | 4.37 | **6.37** | 4.33 | **+2.00** | −0.05 |
| **Equal-weight mean of three** | — | — | — | **+0.13** | −0.34 |

**How to read the improvements**

- **expand vs raw:** the **mean** net-Sharpe gap is **positive (+0.13)**. The largest contribution is **I60/R60**, where expand’s net Sharpe exceeds raw by roughly **two full Sharpe units** under this path. I5 also improves. I20 moves against expand, so the mean is a balance of gains and a loss—not a uniform lift.  
- **clip vs raw:** gains are **local**. At **I5/R5**, clip is the **best of the three arms**. At I20, clip sits between raw and expand (better than expand, still below raw). At I60, clip is essentially tied with raw and far below expand.  
- Absolute Sharpe levels can be large under the daily-return construction used here; **prefer gaps between arms** over interpreting a single number as a live trading Sharpe.

### Ranking skill (paired Rank IC gaps, descriptive)

| Contrast (mean of three diagonal settings) | Δ Rank IC |
|--------------------------------------------|----------:|
| expand − raw | −0.0018 |
| clip − raw | −0.0037 |
| clip − expand | −0.0020 |

Representation-driven **rank** shifts are small and, on average, not favourable. The **economic** path is where expand’s I60 improvement and clip’s I5 improvement appear most clearly.

### Full nine-setting Rank IC matrix (expand vs raw)

Nine \((I,R)\) cells were trained for raw and expand (five seeds each). Mean Δ Rank IC across all nine is near zero (~+0.00018). Cell-level signs go both ways (e.g. I20/R20 negative; several I5 cells slightly positive). See `results/tables/unit_rank_ic.csv`.

---

## Experimental design (concise)

| Item | Choice |
|------|--------|
| Universe | US equities from hfdata 1-minute library (~1,391 tickers) |
| In-sample | 1993–2002 |
| Out-of-sample | 2003–2025 (2026 excluded) |
| Model | CNN on fixed-size greyscale OHLC+MA images; five random seeds; mean probability ensemble |
| Training protocol | Time-blocked train/validation with purge gap (`purged_primary`) |
| Primary scientific arm for full matrix | raw vs **expand** |
| Three-way economic comparison | Diagonal only: (5,5), (20,20), (60,60) for raw, expand, and **clip** |
| Execution | Next-session open; 10 bp one-way; raw open prices even when images use clip OHLC |

Method detail: [docs/METHODS.md](docs/METHODS.md).  
Protocol freeze for clip: [docs/vwpq-clip-oc-protocol.md](docs/vwpq-clip-oc-protocol.md).

---

## Repository layout

```text
README.md                 ← this summary
docs/
  METHODS.md              ← construction rules and evaluation path
  vwpq-clip-oc-protocol.md
configs/
  protocol_vwpq_clip_oc.json
results/
  三臂对照-raw-expand-clip.md
  终报-hfdata-raw-vs-vwpq-v3.6.md   ← long Chinese expand report
  final_summary.md / json/…         ← expand-arm machine summary
  tables/                             ← CSV tables for plots and audits
  json/                               ← full machine-readable dumps
src_snapshot/hfdata/                  ← pure transforms (vwpq expand/clip, NAV helpers)
```

Large training artefacts (image tensors, checkpoints) remain on the compute host and are not vendored here.

---

## Inference appendix (secondary)

For the **expand** arm only, a shared monthly-block bootstrap (\(B=5000\)) was reported in the expand-arm summary:

| Estimand | Point estimate | Role in this repo |
|----------|----------------|-------------------|
| Mean Δ Rank IC (9 cells) | ≈ +0.00018 | Near zero; ranking is not the lift story |
| Mean Δ net Sharpe (3 diagonal cells) | ≈ +0.13 | Matches the economic table above |
| One-sided 5% support for θ > 0 | Not claimed | Shown in `results/json/final_summary.json` if needed |

We treat these as **diagnostics**, not as the headline. The repository’s emphasis is the **signed, setting-level movement** in net Sharpe—especially **expand at I60/R60** and **clip at I5/R5**.

---

## 中文摘要

本仓库报告三种日线表示下的 CNN 趋势信号结果：**raw（标准 OHLC）**、**expand（分位高低价外扩、开收不变）**、**clip（分位高低价并裁剪开收）**。

**提升集中在经济路径（10 bps 净夏普）而非平均排序相关：**

- **expand 相对 raw**：对角线三格平均净夏普差约 **+0.13**；其中 **I60/R60 约 +2.0**，**I5/R5 约 +0.10**；I20/R20 为负。  
- **clip 相对 raw**：**I5/R5 三臂中最优**（净夏普 −0.18 vs raw −0.40）；I20 优于 expand 但仍低于 raw；三格平均相对 raw 为负。  
- Rank IC 平均变化接近零或略负；完整九格 expand 矩阵与三臂表见 `results/`。

方法说明见 `docs/METHODS.md`；机器可读数字见 `results/json/` 与 `results/tables/`。

---

## Citation and relation to prior work

This study is **representation-focused**: it does not claim to reproduce the absolute Accuracy / Rank IC / Sharpe numbers of Jiang et al. under official image archives. It asks whether **alternative high–low constructions** change behaviour under a fixed CNN pipeline on hfdata-derived bars.

---

## Licence

Code snapshots in this repository are provided under the MIT Licence (see `LICENSE`). Data access remains subject to the terms of the hfdata source and host environment.
