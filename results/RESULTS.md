# Results for Study A: equity OHLC representations

Results for Study B are in [crypto/RESULTS.md](crypto/RESULTS.md).

## 0. Five-way economic path

Arms: raw, share expand, share clip, dollar expand, dollar clip.  
Share weights use volume \(V\); dollar weights use \(pV\) with typical price \(p=(H+L+C)/3\).  
Path: next-open high-minus-low, ten basis points one-way, annualisation \(\sqrt{252}\).  
Keys: intersection of all arms present for each diagonal unit.

| I | R | raw | share expand | share clip | dollar expand | dollar clip | Δ$exp−raw | Δ$clip−raw |
|--:|--:|----:|-------------:|-----------:|--------------:|------------:|----------:|-----------:|
| 5 | 5 | −0.399 | −0.301 | −0.184 | −0.312 | **−0.072** | +0.087 | **+0.327** |
| 20 | 20 | 3.068 | 1.359 | 1.889 | 1.425 | **3.132** | −1.643 | **+0.065** |
| 60 | 60 | 4.372 | **6.367** | 4.326 | 6.258 | 4.524 | **+1.886** | +0.152 |

**Diagonal means of Δ net Sharpe vs raw**

| Contrast | Mean Δ |
|----------|--------:|
| share expand − raw | +0.128 |
| share clip − raw | −0.337 |
| **dollar expand − raw** | **+0.110** |
| **dollar clip − raw** | **+0.181** |

Source: `tables/five_way_economic_sharpe.csv`, `json/five_way_raw_share_dollar.json`.

### Headline reading

- **Dollar clip** has the **best mean Δ vs raw (+0.18)** among the four representations, with **gains on every diagonal cell** (including I20, where share-volume arms lose heavily).  
- **Dollar expand** tracks share expand closely (I60 still a large gain; I20 still a large loss; mean ≈ +0.11).  
- Share expand remains the **single best I60** Sharpe; dollar expand is nearly as high.  
- Absolute Sharpes can be large under this daily-return construction; **prefer arm gaps**.

### Five-way paired Rank IC (mean of three diagonal units)

| Contrast | Mean Δ Rank IC |
|----------|---------------:|
| share expand − raw | −0.0018 |
| share clip − raw | −0.0037 |
| dollar expand − raw | −0.0020 |
| dollar clip − raw | −0.0004 |

Source: `tables/five_way_paired_rank_ic.csv`. Ranking gaps remain small relative to economic gaps.

---

## 1. Three-way economic path (share-volume only — historical)

**Path:** next-open high–low, 10 bp one-way, \(\sqrt{252}\).  
**Keys:** raw ∩ expand ∩ clip for each diagonal unit.

| I | R | Sharpe raw | Sharpe expand | Sharpe clip | Δ expand−raw | Δ clip−raw | Δ clip−expand |
|--:|--:|-----------:|--------------:|------------:|-------------:|-----------:|--------------:|
| 5 | 5 | −0.399 | −0.301 | **−0.184** | **+0.098** | **+0.215** | +0.117 |
| 20 | 20 | 3.068 | 1.359 | 1.889 | −1.709 | −1.179 | **+0.530** |
| 60 | 60 | 4.372 | **6.367** | 4.326 | **+1.995** | −0.046 | −2.041 |

**Diagonal means of Δ Sharpe**

| Contrast | Mean Δ |
|----------|--------:|
| expand − raw | **+0.128** |
| clip − raw | −0.337 |
| clip − expand | −0.465 |

Source: `tables/three_way_economic_sharpe.csv`, `json/three_way_economic_sharpe.json`.

### Interpretation focused on gains (share volume)

- **expand** delivers a **positive average** economic gap versus raw on the three diagonal settings, driven by a **large I60/R60 gain** and a **modest I5/R5 gain**.  
- **clip** delivers its **clearest gain at I5/R5**, where it is best among the three share-volume arms, and **outperforms expand at I20/R20**, while remaining below raw there.  
- Averaging across the three settings, share clip does not improve on raw; expand does on the mean gap, with heterogeneous cells.

**Horizon reading (expand):** range compression via volume-weighted high–low is consistent with **stabilising long visual paths (I60)** while **discarding mid-horizon texture that raw extremes still carry (I20)**. Dollar weighting does not remove that I20 expand penalty; **dollar clip** does restore I20. See [docs/INTERPRETATION.md](../docs/INTERPRETATION.md).

---

## 2. Ranking path — paired Δ Rank IC (secondary)

| I | R | Δ expand−raw | Δ clip−raw | Δ clip−expand | n_common (vs raw pairs) |
|--:|--:|-------------:|-----------:|--------------:|------------------------:|
| 5 | 5 | +0.00027 | +0.00063 | +0.00020 | 425,670 |
| 20 | 20 | −0.00647 | −0.00904 | −0.00257 | 270,788 |
| 60 | 60 | +0.00087 | −0.00263 | −0.00350 | 89,876 |

Diagonal means: expand−raw **−0.0018**; clip−raw **−0.0037**.

Full nine-cell expand/raw Rank IC: `tables/unit_rank_ic.csv`.

---

## 3. Expand-arm nine-cell Rank IC (raw vs expand)

See `tables/unit_rank_ic.csv` columns `rank_ic_raw`, `rank_ic_vwpq`, `delta_rank_ic`, `n_common`.  
Mean Δ across nine cells ≈ **+0.00018** (near zero relative to economic gaps above).

---

## 4. Machine-readable dumps

| File | Content |
|------|---------|
| `json/five_way_raw_share_dollar.json` | **Five-way** Rank IC + 10 bp Sharpe bundle |
| `tables/five_way_economic_sharpe.csv` | Five-way economic path |
| `tables/five_way_paired_rank_ic.csv` | Five-way paired Rank IC |
| `tables/five_way_unit_rank_ic.csv` | Per-arm Rank IC by unit |
| `json/final_summary.json` | Expand-arm global summary (includes bootstrap fields) |
| `json/three_way_raw_expand_clip.json` | Three-way Rank IC + economic bundle |
| `json/three_way_economic_sharpe.json` | Three-way economic path only |
| `终报-hfdata-raw-vs-vwpq-v3.6.md` | Long Chinese expand report |
| `三臂对照-raw-expand-clip.md` | Chinese three-way note |
| `五臂对照-raw-量权-额权.md` | Chinese five-way note |

---

## 5. Optional inference fields (not emphasised)

Stored in `json/final_summary.json` under `H1` / `H2` / `H3` for the expand arm (monthly-block bootstrap, \(B=5000\)).  
Use for audit; headline discussion in this repository centres on **setting-level Sharpe movements**.
