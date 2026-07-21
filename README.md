# Re-imagining price-trend OHLC representations

**Languages:** [English](README.md) · [中文](README.zh-CN.md)

**Repository:** [`Reimaging-Price-Trend-OHLC-reasearch`](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-reasearch)  
**Focus:** Can volume-weighted high–low construction improve CNN-based equity trend signals relative to standard daily OHLC bars?

This repository packages the **empirical results** of a three-arm study on US equities (hfdata 1-minute source → daily bars → candlestick images → CNN ensembles). The narrative emphasises **where representation choices move portfolio performance**, and places formal inference in a secondary role.

---

## Abstract

We compare three daily bar constructions under a shared training and evaluation protocol:

| Arm | What changes in the image |
|-----|---------------------------|
| **raw** | Standard open / high / low / close / volume |
| **expand** | Open, close and volume fixed to raw; high/low from volume-weighted quantiles, **expanded** so that open and close remain inside the range |
| **clip** | High/low from the same quantiles; open/close **clipped** into that band when they fall outside |

Models are image CNNs in the spirit of Jiang, Kelly & Xiu (2023), *The Journal of Finance* ([doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)), trained on 1993–2002 and evaluated on 2003–2025. Labels, moving averages and trade fills remain **raw** prices; only the drawn OHLC geometry differs.

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

### Why might expand help at I60 and hurt at I20?

Expand leaves open and close at raw values but rebuilds the high–low span from volume-weighted quantiles, then expands that span only far enough to contain open and close. On many days this **shortens volume-light extremes** in the drawn range, so the image is less pinned by single thin prints.

A concise working account—consistent with the table, not yet identified by ablation—is **horizon-dependent use of range “texture”**:

| Horizon | Expand − raw (net Sharpe) | Suggested reading |
|---------|---------------------------|-------------------|
| **Long (I60/R60)** | large **gain** (~+2) | Multi-month path features (drift, range regimes) may be easier to learn when extremes no longer dominate vertical scaling; range compression acts like mild visual regularisation. |
| **Intermediate (I20/R20)** | large **loss** (~−1.7) | Monthly panels may still rely on higher-frequency irregularity that raw high–low preserves; softening extremes can discard mid-horizon cues. |
| **Short (I5/R5)** | modest **gain** (~+0.1) | A single extreme day dominates a five-bar chart; mild range cleaning can help, while **clip** (which also moves open/close) helps further on this cell. |

In short: **what behaves like noise for long visual horizons can remain useful texture at intermediate horizons.** Keeping open/close raw while only editing the range (expand) also differs from clip: expand—not clip—drives the I60 Sharpe lift, which suggests long-horizon gains are not “any compression helps,” but rather **range denoising with an intact body**.

Full write-up: [docs/INTERPRETATION.md](docs/INTERPRETATION.md).

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
README.md                 ← English (this file)
README.zh-CN.md           ← Chinese
CITATIONS.md              ← data, code, and paper citations (authoritative)
CITATION.cff              ← GitHub citation metadata
NOTICE                    ← third-party attribution
LICENSE                   ← Apache License 2.0
docs/
  METHODS.md
  INTERPRETATION.md       ← horizon-dependent expand analysis
  vwpq-clip-oc-protocol.md
configs/
  protocol_vwpq_clip_oc.json
results/
  RESULTS.md
  tables/ · json/ · Chinese long reports
src_snapshot/hfdata/      ← pure transforms (expand/clip, NAV helpers)
```

Large training artefacts (image tensors, checkpoints, full 1-minute archives) remain on the compute host and are **not** vendored here.

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

## Data sources

| Layer | Source | Notes |
|-------|--------|--------|
| **This study (minute → daily)** | **HF Data Library** US high-frequency OHLCV (1-minute parquet panel used on the experiment host) | Public dataset page: [Hugging Face `elkassabgi/hfdatalibrary`](https://huggingface.co/datasets/elkassabgi/hfdatalibrary). Local path used in experiments: `/share/home/user/snliu/hfdata_us_1min`. **Not redistributed** in this repo. |
| **Jiang–Kelly–Xiu (2023) paper** | **CRSP** daily US equities (NYSE/AMEX/NASDAQ), typically via WRDS | PERMNO identifiers; paper sample commonly described from the early 1990s through 2019. **Not redistributed** here. |
| **Derived bars** | raw / expand / clip daily OHLCV built in our pipeline | See [docs/METHODS.md](docs/METHODS.md). |

Identifiers in our hfdata path are **source tickers / series files**, not CRSP PERMNOs. Results are conditional on that panel.

Full wording: [CITATIONS.md §2](CITATIONS.md).

---

## Reference code repositories

| Repository | URL | Role |
|------------|-----|------|
| **This project** | [kola-official/Reimaging-Price-Trend-OHLC-reasearch](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-reasearch) | Results, protocols, small transform snapshot |
| **ReImagining_Price_Trends** | [gaoym4321/ReImagining_Price_Trends](https://github.com/gaoym4321/ReImagining_Price_Trends) | Community/author-style implementation used for architecture orientation (pinned commit in local bootstrap config) |
| **Stock_CNN** | [lich99/Stock_CNN](https://github.com/lich99/Stock_CNN) | Lightweight smoke / architecture cross-check |

Third-party repositories retain **their own licences**. See [CITATIONS.md §3](CITATIONS.md) and [NOTICE](NOTICE).

---

## Reference paper

> Jiang, J., Kelly, B., & Xiu, D. (2023). *(Re-)Imag(in)ing price trends.*  
> *The Journal of Finance*, 78(6), 3193–3249.  
> https://doi.org/10.1111/jofi.13268

This study is **representation-focused**: it does **not** claim to reproduce the paper’s absolute Accuracy / Rank IC / Sharpe numbers on official CRSP image archives. It asks whether **alternative high–low constructions** change behaviour under a fixed CNN pipeline on hfdata-derived bars.

BibTeX and secondary literature: [CITATIONS.md](CITATIONS.md).

---

## Licence

| Item | Choice |
|------|--------|
| **Open-source licence** | **[Apache License 2.0](LICENSE)** |
| **Attribution file** | [NOTICE](NOTICE) |
| **Why Apache-2.0** | Clear terms for research code, explicit patent grant, standard NOTICE/attribution practice for citing third-party data and software without redistributing them |

**Not covered by this licence:** CRSP data, HF Data Library dumps, the Journal of Finance article PDF/figures, or the full trees of third-party GitHub projects. Obtain those under their own terms.

---

## How to cite this repository

See [CITATION.cff](CITATION.cff) and the BibTeX block in [CITATIONS.md §4](CITATIONS.md). Always cite **Jiang, Kelly & Xiu (2023)** when discussing the image-CNN price-trend framework.
