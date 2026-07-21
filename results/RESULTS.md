# Results tables

## 1. Economic path — net Sharpe (primary display)

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

### Interpretation focused on gains

- **expand** delivers a **positive average** economic gap versus raw on the three diagonal settings, driven by a **large I60/R60 gain** and a **modest I5/R5 gain**.  
- **clip** delivers its **clearest gain at I5/R5**, where it is best among the three arms, and **outperforms expand at I20/R20**, while remaining below raw there.  
- Averaging across the three settings, clip does not improve on raw; expand does on the mean gap, with heterogeneous cells.

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
| `json/final_summary.json` | Expand-arm global summary (includes bootstrap fields) |
| `json/three_way_raw_expand_clip.json` | Rank IC + economic bundle |
| `json/three_way_economic_sharpe.json` | Economic path only |
| `终报-hfdata-raw-vs-vwpq-v3.6.md` | Long Chinese expand report |
| `三臂对照-raw-expand-clip.md` | Chinese three-way note |

---

## 5. Optional inference fields (not emphasised)

Stored in `json/final_summary.json` under `H1` / `H2` / `H3` for the expand arm (monthly-block bootstrap, \(B=5000\)).  
Use for audit; headline discussion in this repository centres on **setting-level Sharpe movements**.
