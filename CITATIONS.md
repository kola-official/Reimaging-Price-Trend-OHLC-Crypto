# Data, code, and literature citations

This document records **what we used**, **what we cite**, and **what we do not redistribute**.

**Repository:** [`Reimaging-Price-Trend-OHLC-Crypto`](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto)  
**Studies packaged here:** (A) equity OHLC representation arms; (B) cryptocurrency spot retrain; (C) frozen US raw, expand and clip transfer to cryptocurrency.  
**Scientific spine:** [`docs/SCIENTIFIC-OVERVIEW.md`](docs/SCIENTIFIC-OVERVIEW.md).

---

## 1. Primary literature

### 1.1 Methodological reference paper

The image-based CNN price-trend setting follows the design language of:

> **Jiang, J., Kelly, B., & Xiu, D. (2023).**  
> *(Re-)Imag(in)ing price trends.*  
> *The Journal of Finance*, **78**(6), 3193–3249.  
> **DOI:** [https://doi.org/10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)  
> **Publisher:** [Wiley Online Library](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13268)  
> **SSRN preprint (optional):** [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3756587](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3756587)

**How we use it.**  
We adopt the broad agenda of representing price history as OHLC(+MA/volume) images and learning CNN forecasts of forward returns. **Study A** varies equity bar geometry; **Study B** holds the image recipe fixed and changes the universe to crypto spot. We do **not** claim numerical reproduction of the paper’s CRSP-based Accuracy / Rank IC / Sharpe figures.

**BibTeX**

```bibtex
@article{jiang2023reimagining,
  author  = {Jiang, Jingwen and Kelly, Bryan and Xiu, Dacheng},
  title   = {(Re-)Imag(in)ing Price Trends},
  journal = {The Journal of Finance},
  year    = {2023},
  volume  = {78},
  number  = {6},
  pages   = {3193--3249},
  doi     = {10.1111/jofi.13268},
  url     = {https://doi.org/10.1111/jofi.13268}
}
```

### 1.2 Selected supporting references (context)

These appear in the paper’s intellectual neighbourhood and/or classical technical-analysis / volatility measurement background:

| Reference | Role |
|-----------|------|
| Lo, A. W., Mamaysky, H., & Wang, J. (2000). Foundations of technical analysis. *Journal of Finance*, 55(4), 1705–1765. | Classical technical-analysis empirics |
| Parkinson, M. (1980). The extreme value method for estimating the variance of the rate of return. *Journal of Business*, 53(1), 61–65. | High–low range as volatility information |
| Jegadeesh, N., & Titman, S. (1993). Returns to buying winners and selling losers. *Journal of Finance*, 48(1), 65–91. | Momentum benchmark literature |
| Sullivan, R., Timmermann, A., & White, H. (1999). Data-snooping, technical trading rule performance, and the bootstrap. *Journal of Finance*, 54(5), 1647–1691. | Multiple-testing / technical-rule universe |

Full bibliographic detail is available from the publisher DOIs of each article.

---

## 2. Data sources

### 2.1 Data used in **this** repository’s experiments (hfdata path)

| Item | Detail |
|------|--------|
| **Working name** | HF Data Library / US 1-minute OHLCV (clean parquet panel) |
| **Local compute path (experiment host)** | `/share/home/user/snliu/hfdata_us_1min` |
| **Typical schema** | `datetime`, `Open`, `High`, `Low`, `Close`, `Volume` (plus vendor `source` fields in provenance) |
| **Coverage (study design)** | Bars aggregated to daily; model years **1993–2002** (in-sample) and **2003–2025** (out-of-sample); **2026** excluded from the main design |
| **Public dataset page (upstream collection)** | [Hugging Face: `elkassabgi/hfdatalibrary`](https://huggingface.co/datasets/elkassabgi/hfdatalibrary) — *HF Data Library: High-Frequency U.S. free research-grade OHLCV collection (1-minute and coarser)* |
| **Vendor provenance (local notes)** | Session pre-checks recorded vendor tags consistent with high-frequency equity feeds (e.g. `pitrading` in source columns); exact vendor mix is a property of the downloaded panel |

**Important.**  
Minute bars and full image tensors are **not** uploaded to this GitHub repository. Users must obtain HF Data Library (or equivalent) data under **that dataset’s and vendor’s terms of use**. Our results assume the cleaned 1-minute panel used in the experiment host; they are **conditional on that source series ID system** (ticker-level files), not on a CRSP PERMNO panel.

### 2.2 Data used in the **Jiang–Kelly–Xiu** paper (reference only)

| Item | Detail |
|------|--------|
| **Source** | CRSP daily equity data (NYSE / AMEX / NASDAQ) |
| **Sample window in the paper** | Daily OHLC availability from mid-1992; main analyses commonly described over **1993–2019** |
| **Identifiers** | CRSP **PERMNO** (not tickers) |
| **Access** | Via WRDS / CRSP subscription; **not redistributed here** |

### 2.3 What we derive from raw minutes (Study A)

1. **raw** daily OHLCV (session RTH aggregation).  
2. **expand** daily bars: O/C/V = raw; H/L = volume-weighted quantiles expanded to cover O/C.  
3. **clip** daily bars: H/L = quantile band; O/C clipped into `[L, H]`.  
4. Greyscale OHLC+MA images; labels and portfolio fills from **raw** prices.

### 2.4 Data used in **Study B** (crypto spot)

| Item | Detail |
|------|--------|
| **Market** | Binance **USDT spot** only (perpetual futures excluded from v1) |
| **Local compute path (experiment host)** | `/share/home/user/snliu/crypto_klines/binance_spot_1m` |
| **Engineering workspace** | `/share/home/user/snliu/crypto_reimaging_workspace` |
| **Coverage (study design)** | UTC daily bars; **IS 2018–2021**, **OOS 2022–2025**; 2026 excluded |
| **Content snapshot (host)** | 23,674 files / ~128.9 GB; content-set SHA-256 `bdf6acc40923fce7ee07012487c4256837b2a1819a83029a225c93fc5c3fc558` |
| **Public access** | Users must obtain Binance historical klines under **Binance’s** terms; this repository does **not** redistribute kline archives |

**What we derive (crypto).**  
UTC daily OHLC from 1m bars; point-in-time liquidity universe; greyscale author-exact OHLC+MA images; close-to-close \(R\)-day labels; optional delayed-VWAP execution primitives (not the headline economic freeze of the 2026-07-24 audit table).

**Identity.**  
Seven redenomination / ticker-reuse events are handled by **splitting series at the break** (formal freeze v1); we do not silently rescale OHLC across identity changes.

---

## 3. Code and software repositories

### 3.1 This project

| Item | Detail |
|------|--------|
| **GitHub** | [https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto) |
| **Contents** | Study A/B result tables/JSON, method & interpretation notes, protocol freezes, small pure-Python snapshots |
| **Local engineering workspaces (not this remote)** | Equity: `price-trends-bootstrap` / RTX3090 `price_trends_workspace`. Crypto: `crypto-reimaging-price-trends` / RTX3090 `crypto_reimaging_workspace` |
| **Study C transfer checkpoints** | Host path `price_trends_workspace/outputs/hfdata/purged_primary/{raw,vwpq,vwpq_clip}` scored on crypto OOS images; metrics under `results/crypto/transfer/` |

### 3.2 External open-source code we reference

| Repository | URL | How we use it |
|------------|-----|----------------|
| **ReImagining_Price_Trends** (community / author-style implementation) | [https://github.com/gaoym4321/ReImagining_Price_Trends](https://github.com/gaoym4321/ReImagining_Price_Trends) | Architecture and pipeline orientation for Jiang-style image CNNs; pinned in local config as `author_repository` |
| **Stock_CNN** | [https://github.com/lich99/Stock_CNN](https://github.com/lich99/Stock_CNN) | Lightweight smoke / architecture cross-check; local config `smoke_repository` |

Pinned commits used in the local bootstrap config (for reproducibility of *that* workspace, not necessarily this results-only repo):

- `author_repository` commit: `76efcfe1b0b079212dcb7db760be83aa0f4661fe`  
- `smoke_repository` commit: `415e2acf2a5013afca67e383acd3edc61fced840`  

Source: `price-trends-bootstrap/configs/paper_i20_r20.yaml` (`provenance` block).

**Licence of third-party code.**  
Those repositories keep **their own** licences. Our Apache-2.0 licence covers **this** repository’s original files only. Do not assume their code is Apache-2.0 unless their LICENSE files say so.

### 3.3 Related commercial / academic data platforms (context)

| Name | Role |
|------|------|
| **CRSP** | Data backbone of the published Jiang–Kelly–Xiu study |
| **WRDS** | Typical access path to CRSP |
| **Yahoo! Finance / Google Finance charts** | Motivating OHLC chart aesthetics in the paper (not our data source) |

---

## 4. How to cite **this** repository

If you use our tables or protocol definitions:

```bibtex
@misc{reimaging_ohlc_crypto_2026,
  title        = {Re-imagining Price-Trend {OHLC} Representations and
                  Cryptocurrency Transfer},
  author       = {{Contributors}},
  year         = {2026},
  howpublished = {\url{https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto}},
  note         = {Studies A--C: equity representations, crypto retrain,
                  frozen US transfer; Apache-2.0}
}
```

Always cite **Jiang, Kelly & Xiu (2023)** when discussing the image-CNN price-trend framework.

---

## 5. Licence choice (this repository)

| Choice | **Apache License 2.0** |
|--------|-------------------------|
| File | [`LICENSE`](LICENSE) |
| Notice | [`NOTICE`](NOTICE) |
| Why | Standard for research code releases; explicit patent grant; clear NOTICE/attribution for third-party references; widely understood by academia and industry |

**Not covered by our licence:** CRSP data, HF Data Library dumps, Jiang–Kelly–Xiu paper PDF/figures, or third-party GitHub trees unless copied with their own licence files (we do not copy those trees into this repo).
