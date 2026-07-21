# Methods

## Citations (read first)

Authoritative lists of **data**, **code**, and **papers** live in the repository root:

- [CITATIONS.md](../CITATIONS.md) — full wording, BibTeX, what is / is not redistributed  
- [NOTICE](../NOTICE) — third-party attribution under Apache-2.0  
- [LICENSE](../LICENSE) — **Apache License 2.0**

Primary paper: Jiang, Kelly & Xiu (2023), *Journal of Finance*, [doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268).  
Primary experiment data: HF Data Library US 1-minute OHLCV ([Hugging Face dataset page](https://huggingface.co/datasets/elkassabgi/hfdatalibrary)); not shipped in this repo.

## Daily bar constructions

### raw

From RTH 1-minute bars:

- open = first valid minute open  
- high = max minute high  
- low = min minute low  
- close = last valid minute close  
- volume = sum of minute volume  

### expand (`vwpq` path id)

1. Compute typical price \(p=(H+L+C)/3\) with volume weights.  
2. Volume-weighted quantiles \(q_{0.05}\), \(q_{0.95}\).  
3. Keep open, close, volume **identical to raw**.  
4. Set  
   \(L=\min(q_{0.05},O,C)\), \(H=\max(q_{0.95},O,C)\)  
   (expand-not-clip).  

Invalid / zero-volume sessions are marked invalid and are not treated as a successful expand representation.

### clip (`vwpq_clip`)

1. Same quantiles as expand.  
2. Set \(L=q_{0.05}\), \(H=q_{0.95}\) **without** expanding for open/close.  
3. Clip  
   \(O'=\mathrm{clip}(O,L,H)\), \(C'=\mathrm{clip}(C,L,H)\).  
4. Volume remains raw.  

### Dollar-volume expand (`vwpq_d`) and clip (`vwpq_d_clip`)

Same geometry rules as share expand / share clip, but weights are **dollar volume**

\[
w_t = p_t V_t,\qquad p_t=\frac{H_t+L_t+C_t}{3}.
\]

Path ids: `vwpq_d` (expand), `vwpq_d_clip` (clip-OC). Protocol freeze: [vwpq-dollar-protocol.md](vwpq-dollar-protocol.md), `configs/protocol_vwpq_dollar.json`.

**Labels, image moving averages, and portfolio open prices always use raw series.** All four representations only change the OHLC geometry fed to the CNN.

Implementation: `src_snapshot/hfdata/vwpq.py`.

## Images and model

- Windows \(I\in\{5,20,60\}\) days; greyscale OHLC + MA panels.  
- Horizons \(R\in\{5,20,60\}\) for labels (raw close-to-close sign / return).  
- Formation frequency follows \(R\) (weekly / monthly / quarterly).  
- CNN architecture aligned with the price-trend image literature used in the local bootstrap codebase.  
- Five seeds; OOS probability = mean across seeds.  

## Sample split and training

- In-sample: **1993–2002**.  
- Out-of-sample: **2003–2025** (exclude 2026).  
- Protocol `purged_primary`: chronological train/validation blocks with purge cut  
  \(\mathrm{val}>\mathrm{train\_max}+R+(2I-2)\).  
- Train-only normalisation statistics.  

## Evaluation

### Ranking

For each formation date with enough names, Spearman correlation between ensemble “up” probability and forward raw return. Arm comparisons use **intersection keys** so both sides share the same (instrument, date) set.

### Economics

- Sort by probability; long top decile / short bottom decile (equal weight).  
- Enter next RTH open; exit after \(R\) sessions at open (or frozen last close proxy).  
- One-way cost **10 bp** on traded notional.  
- Net daily returns aggregated with planned concurrency weights; Sharpe uses \(\sqrt{252}\).  

Three-way Sharpe tables restrict to **raw ∩ expand ∩ clip** keys on the diagonal \((I,R)\in\{(5,5),(20,20),(60,60)\}\).  
Five-way Sharpe tables use the intersection of all arms present for that unit (raw + four representations).

## Scope notes

| Arm | Weight | O/C rule | Rank IC matrix | Economic diagonal |
|-----|--------|----------|----------------|-------------------|
| raw | — | standard | Full 9 \((I,R)\) | Yes |
| share expand (`vwpq`) | \(V\) | lock O/C | Full 9 | Yes |
| share clip (`vwpq_clip`) | \(V\) | clip O/C | Diagonal 3 | Yes |
| dollar expand (`vwpq_d`) | \(pV\) | lock O/C | Diagonal 3 | Yes |
| dollar clip (`vwpq_d_clip`) | \(pV\) | clip O/C | Diagonal 3 | Yes |

Large image binaries and checkpoints are not stored in this GitHub repository.
